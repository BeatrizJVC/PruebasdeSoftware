from datetime import date

from src.models.equipment import EquipmentStatus
from src.models.loan import Loan, LoanStatus
from src.models.user import User, UserRole
from src.repositories.json_repository import JsonRepository
from src.utils.date_utils import (
    is_overdue,
    is_valid_loan_duration,
    is_within_advance_limit,
    periods_overlap,
)


class LoanValidationError(Exception):
    """Error provocado por una regla de negocio del préstamo."""
    pass


class InvalidLoanTransitionError(Exception):
    """Transición de estado no permitida."""
    pass


class LoanService:
    MAX_ACTIVE_EQUIPMENT = 3

    BLOCKING_STATES = {
        LoanStatus.APROBADA,
        LoanStatus.ENTREGADA,
    }

    ACTIVE_STATES = {
        LoanStatus.APROBADA,
        LoanStatus.ENTREGADA,
    }

    def __init__(
        self,
        loan_repository: JsonRepository,
        user_repository: JsonRepository,
        equipment_repository: JsonRepository,
    ):
        self.loan_repository = loan_repository
        self.user_repository = user_repository
        self.equipment_repository = equipment_repository

    # ---------------------------------------------------------
    # Utilidades internas
    # ---------------------------------------------------------

    def _get_loan(self, loan_id: str) -> Loan:
        loan = self.loan_repository.get_by_id(loan_id)

        if loan is None:
            raise ValueError(
                f"No existe una solicitud con ID {loan_id}."
            )

        return loan

    def _get_user(self, user_id: str) -> User:
        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise ValueError(
                f"No existe un usuario con ID {user_id}."
            )

        return user

    def _require_manager(self, user: User) -> None:
        if user.role != UserRole.ENCARGADO:
            raise PermissionError(
                "Esta operación requiere rol ENCARGADO."
            )

        if not user.enabled:
            raise PermissionError(
                "El usuario se encuentra deshabilitado."
            )

    def _require_requester(self, user: User) -> None:
        if user.role != UserRole.SOLICITANTE:
            raise PermissionError(
                "Esta operación requiere rol SOLICITANTE."
            )

        if not user.enabled:
            raise PermissionError(
                "El usuario se encuentra deshabilitado."
            )

    def _generate_loan_id(self) -> str:
        loans = self.loan_repository.get_all()

        numbers = []

        for loan in loans:
            try:
                numbers.append(
                    int(loan.id.split("-")[-1])
                )
            except (ValueError, IndexError):
                continue

        next_number = max(numbers, default=0) + 1

        return f"P-{next_number:03d}"

    # ---------------------------------------------------------
    # Validaciones
    # ---------------------------------------------------------

    def _validate_dates(
        self,
        start_date: date,
        return_date: date,
        current_date: date | None = None,
    ) -> None:
        # RN-11 + RN-02
        if not is_valid_loan_duration(
            start_date,
            return_date,
        ):
            raise LoanValidationError(
                "El período debe ser válido y no superar "
                "2 días hábiles."
            )

        # RN-03
        if not is_within_advance_limit(
            start_date,
            current_date,
        ):
            raise LoanValidationError(
                "La reserva debe comenzar entre hoy "
                "y un máximo de 30 días."
            )

    def _user_has_overdue_loans(
        self,
        user_id: str,
        current_date: date | None = None,
    ) -> bool:
        # RN-05 / RN-12
        loans = self.loan_repository.get_all()

        return any(
            loan.user_id == user_id
            and is_overdue(
                loan.return_date,
                loan.status.value,
                current_date,
            )
            for loan in loans
        )

    def _active_equipment_count(
        self,
        user_id: str,
    ) -> int:
        loans = self.loan_repository.get_all()

        return sum(
            len(loan.equipment_ids)
            for loan in loans
            if loan.user_id == user_id
            and loan.status in self.ACTIVE_STATES
        )

    def _validate_equipment_limit(
        self,
        user_id: str,
        requested_count: int,
    ) -> None:
        # RN-01
        active_count = self._active_equipment_count(
            user_id
        )

        if (
            active_count + requested_count
            > self.MAX_ACTIVE_EQUIPMENT
        ):
            raise LoanValidationError(
                "El solicitante no puede superar "
                "3 equipos asociados a préstamos activos."
            )

    def is_equipment_available(
        self,
        equipment_id: str,
        start_date: date,
        return_date: date,
        excluded_loan_id: str | None = None,
    ) -> bool:
        """
        RN-04 / RN-06 / RF-17
        """

        equipment = self.equipment_repository.get_by_id(
            equipment_id
        )

        if equipment is None:
            raise ValueError(
                f"No existe el equipo {equipment_id}."
            )

        if equipment.status == EquipmentStatus.MANTENIMIENTO:
            return False

        loans = self.loan_repository.get_all()

        for loan in loans:
            if loan.id == excluded_loan_id:
                continue

            if loan.status not in self.BLOCKING_STATES:
                continue

            if equipment_id not in loan.equipment_ids:
                continue

            if periods_overlap(
                start_date,
                return_date,
                loan.start_date,
                loan.return_date,
            ):
                return False

        return True

    def _validate_equipment(
        self,
        equipment_ids: list[str],
        start_date: date,
        return_date: date,
        excluded_loan_id: str | None = None,
    ) -> None:

        if not equipment_ids:
            raise LoanValidationError(
                "Debe seleccionar al menos un equipo."
            )

        if len(set(equipment_ids)) != len(equipment_ids):
            raise LoanValidationError(
                "Una solicitud no puede contener "
                "el mismo equipo más de una vez."
            )

        for equipment_id in equipment_ids:
            if not self.is_equipment_available(
                equipment_id,
                start_date,
                return_date,
                excluded_loan_id,
            ):
                raise LoanValidationError(
                    f"El equipo {equipment_id} no está "
                    "disponible para el período solicitado."
                )

    # ---------------------------------------------------------
    # Crear solicitud
    # ---------------------------------------------------------

    def create_request(
        self,
        user_id: str,
        equipment_ids: list[str],
        start_date: date,
        return_date: date,
        current_date: date | None = None,
    ) -> Loan:
        """
        RF-06
        RN-01, RN-02, RN-03, RN-04,
        RN-05, RN-06 y RN-11.
        """

        user = self._get_user(user_id)

        self._require_requester(user)

        if self._user_has_overdue_loans(
            user_id,
            current_date,
        ):
            raise LoanValidationError(
                "El usuario posee un préstamo atrasado."
            )

        self._validate_dates(
            start_date,
            return_date,
            current_date,
        )

        self._validate_equipment_limit(
            user_id,
            len(equipment_ids),
        )

        self._validate_equipment(
            equipment_ids,
            start_date,
            return_date,
        )

        loan = Loan(
            id=self._generate_loan_id(),
            user_id=user_id,
            equipment_ids=equipment_ids,
            start_date=start_date,
            return_date=return_date,
        )

        self.loan_repository.add(loan)

        return loan

    # ---------------------------------------------------------
    # Aprobar
    # ---------------------------------------------------------

    def approve_request(
        self,
        loan_id: str,
        manager: User,
        current_date: date | None = None,
    ) -> Loan:
        """
        RF-10 / RN-07
        """

        self._require_manager(manager)

        loan = self._get_loan(loan_id)

        if loan.status != LoanStatus.SOLICITADA:
            raise InvalidLoanTransitionError(
                "Solo pueden aprobarse solicitudes "
                "en estado SOLICITADA."
            )

        if self._user_has_overdue_loans(
            loan.user_id,
            current_date,
        ):
            raise LoanValidationError(
                "El solicitante posee préstamos atrasados."
            )

        self._validate_equipment_limit(
            loan.user_id,
            len(loan.equipment_ids),
        )

        # Se vuelve a comprobar la disponibilidad.
        # Otra solicitud pudo haber sido aprobada después.
        self._validate_equipment(
            loan.equipment_ids,
            loan.start_date,
            loan.return_date,
            excluded_loan_id=loan.id,
        )

        loan.status = LoanStatus.APROBADA

        self.loan_repository.update(loan)

        return loan

    # ---------------------------------------------------------
    # Rechazar
    # ---------------------------------------------------------

    def reject_request(
        self,
        loan_id: str,
        manager: User,
    ) -> Loan:

        self._require_manager(manager)

        loan = self._get_loan(loan_id)

        if loan.status != LoanStatus.SOLICITADA:
            raise InvalidLoanTransitionError(
                "Solo pueden rechazarse solicitudes "
                "en estado SOLICITADA."
            )

        loan.status = LoanStatus.RECHAZADA

        self.loan_repository.update(loan)

        return loan

    # ---------------------------------------------------------
    # Cancelar
    # ---------------------------------------------------------

    def cancel_request(
        self,
        loan_id: str,
        requester: User,
    ) -> Loan:
        """
        RF-08 / RN-10
        """

        self._require_requester(requester)

        loan = self._get_loan(loan_id)

        if loan.user_id != requester.id:
            raise PermissionError(
                "Solo puede cancelar sus propias solicitudes."
            )

        if loan.status not in {
            LoanStatus.SOLICITADA,
            LoanStatus.APROBADA,
        }:
            raise InvalidLoanTransitionError(
                "La solicitud ya no puede cancelarse."
            )

        loan.status = LoanStatus.CANCELADA

        self.loan_repository.update(loan)

        return loan

    # ---------------------------------------------------------
    # Entrega
    # ---------------------------------------------------------

    def deliver_loan(
        self,
        loan_id: str,
        manager: User,
    ) -> Loan:
        """
        RF-12 / RN-08
        """

        self._require_manager(manager)

        loan = self._get_loan(loan_id)

        if loan.status != LoanStatus.APROBADA:
            raise InvalidLoanTransitionError(
                "Solo puede entregarse una solicitud APROBADA."
            )

        # Primero validamos todos los equipos.
        equipment_list = []

        for equipment_id in loan.equipment_ids:
            equipment = (
                self.equipment_repository.get_by_id(
                    equipment_id
                )
            )

            if equipment is None:
                raise LoanValidationError(
                    f"No existe el equipo {equipment_id}."
                )

            if (
                equipment.status
                == EquipmentStatus.MANTENIMIENTO
            ):
                raise LoanValidationError(
                    f"El equipo {equipment_id} está "
                    "en mantenimiento."
                )

            equipment_list.append(equipment)

        loan.status = LoanStatus.ENTREGADA
        self.loan_repository.update(loan)

        for equipment in equipment_list:
            equipment.status = EquipmentStatus.PRESTADO
            self.equipment_repository.update(equipment)

        return loan

    # ---------------------------------------------------------
    # Devolución
    # ---------------------------------------------------------

    def return_loan(
        self,
        loan_id: str,
        manager: User,
    ) -> Loan:
        """
        RF-13 / RN-09
        """

        self._require_manager(manager)

        loan = self._get_loan(loan_id)

        if loan.status != LoanStatus.ENTREGADA:
            raise InvalidLoanTransitionError(
                "Solo puede devolverse un préstamo ENTREGADO."
            )

        equipment_list = []

        for equipment_id in loan.equipment_ids:
            equipment = (
                self.equipment_repository.get_by_id(
                    equipment_id
                )
            )

            if equipment is None:
                raise LoanValidationError(
                    f"No existe el equipo {equipment_id}."
                )

            equipment_list.append(equipment)

        loan.status = LoanStatus.DEVUELTA
        self.loan_repository.update(loan)

        for equipment in equipment_list:
            equipment.status = EquipmentStatus.DISPONIBLE
            self.equipment_repository.update(equipment)

        return loan

    # ---------------------------------------------------------
    # Consultas
    # ---------------------------------------------------------

    def get_user_requests(
        self,
        user_id: str,
    ) -> list[Loan]:
        return [
            loan
            for loan in self.loan_repository.get_all()
            if loan.user_id == user_id
        ]

    def get_pending_requests(self) -> list[Loan]:
        return [
            loan
            for loan in self.loan_repository.get_all()
            if loan.status == LoanStatus.SOLICITADA
        ]

    def get_future_loans(
        self,
        current_date: date | None = None,
    ) -> list[Loan]:

        if current_date is None:
            current_date = date.today()

        return [
            loan
            for loan in self.loan_repository.get_all()
            if loan.status == LoanStatus.APROBADA
            and loan.start_date > current_date
        ]

    def get_current_loans(
        self,
        current_date: date | None = None,
    ) -> list[Loan]:

        if current_date is None:
            current_date = date.today()

        return [
            loan
            for loan in self.loan_repository.get_all()
            if loan.status == LoanStatus.ENTREGADA
            and loan.return_date >= current_date
        ]

    def get_overdue_loans(
        self,
        current_date: date | None = None,
    ) -> list[Loan]:

        return [
            loan
            for loan in self.loan_repository.get_all()
            if is_overdue(
                loan.return_date,
                loan.status.value,
                current_date,
            )
        ]