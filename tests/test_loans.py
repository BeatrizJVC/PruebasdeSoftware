import pytest
from datetime import date

from src.models.equipment import Equipment, EquipmentStatus
from src.models.loan import Loan, LoanStatus
from src.models.user import User, UserRole
from src.services.loan_service import (
    LoanService,
    LoanValidationError,
    InvalidLoanTransitionError,
)


class FakeRepository:
    def __init__(self, items=None):
        self.items = items or []

    def get_all(self):
        return self.items

    def get_by_id(self, object_id):
        return next(
            (
                item
                for item in self.items
                if item.id == object_id
            ),
            None,
        )

    def add(self, item):
        self.items.append(item)

    def update(self, updated_item):
        for index, item in enumerate(self.items):
            if item.id == updated_item.id:
                self.items[index] = updated_item
                return


@pytest.fixture
def requester():
    return User(
        id="U-01",
        name="Ana",
        email="ana@fablab.cl",
        password="1234",
        role=UserRole.SOLICITANTE,
    )


@pytest.fixture
def manager():
    return User(
        id="U-02",
        name="Elena",
        email="encargada@fablab.cl",
        password="admin",
        role=UserRole.ENCARGADO,
    )


@pytest.fixture
def equipment():
    return [
        Equipment(
            id="EQ-01",
            name="Cámara",
            category="Audiovisual",
            description="Cámara",
        ),
        Equipment(
            id="EQ-02",
            name="Trípode",
            category="Audiovisual",
            description="Trípode",
        ),
        Equipment(
            id="EQ-03",
            name="Micrófono",
            category="Audio",
            description="Micrófono",
        ),
        Equipment(
            id="EQ-04",
            name="Notebook",
            category="Computación",
            description="Notebook",
            status=EquipmentStatus.MANTENIMIENTO,
        ),
    ]


@pytest.fixture
def loan_service(requester, manager, equipment):
    return LoanService(
        FakeRepository(),
        FakeRepository([requester, manager]),
        FakeRepository(equipment),
    )


def test_crear_solicitud_valida(loan_service):
    # TC-05
    loan = loan_service.create_request(
        "U-01",
        ["EQ-01"],
        date(2026, 9, 7),
        date(2026, 9, 9),
        current_date=date(2026, 9, 6),
    )

    assert loan.status == LoanStatus.SOLICITADA
    assert loan.id == "P-001"


def test_solicitar_equipo_en_mantenimiento(
    loan_service,
):
    # TC-12
    with pytest.raises(LoanValidationError):
        loan_service.create_request(
            "U-01",
            ["EQ-04"],
            date(2026, 9, 7),
            date(2026, 9, 9),
            current_date=date(2026, 9, 6),
        )


def test_maximo_tres_equipos(
    loan_service,
    manager,
):
    # TC-06
    loan = loan_service.create_request(
        "U-01",
        ["EQ-01", "EQ-02", "EQ-03"],
        date(2026, 9, 7),
        date(2026, 9, 9),
        current_date=date(2026, 9, 6),
    )

    loan_service.approve_request(
        loan.id,
        manager,
        current_date=date(2026, 9, 6),
    )

    assert loan.status == LoanStatus.APROBADA


def test_no_supera_tres_equipos(
    loan_service,
    manager,
):
    # TC-07
    loan = loan_service.create_request(
        "U-01",
        ["EQ-01", "EQ-02", "EQ-03"],
        date(2026, 9, 7),
        date(2026, 9, 9),
        current_date=date(2026, 9, 6),
    )

    loan_service.approve_request(
        loan.id,
        manager,
        current_date=date(2026, 9, 6),
    )

    with pytest.raises(LoanValidationError):
        loan_service.create_request(
            "U-01",
            ["EQ-01"],
            date(2026, 9, 10),
            date(2026, 9, 11),
            current_date=date(2026, 9, 6),
        )


def test_dos_solicitudes_pueden_existir_antes_de_aprobar(
    loan_service,
):
    first = loan_service.create_request(
        "U-01",
        ["EQ-01"],
        date(2026, 9, 7),
        date(2026, 9, 9),
        current_date=date(2026, 9, 6),
    )

    second = loan_service.create_request(
        "U-01",
        ["EQ-01"],
        date(2026, 9, 8),
        date(2026, 9, 9),
        current_date=date(2026, 9, 6),
    )

    assert first.status == LoanStatus.SOLICITADA
    assert second.status == LoanStatus.SOLICITADA


def test_no_aprobar_solicitud_superpuesta(
    loan_service,
    manager,
):
    # TC-14
    first = loan_service.create_request(
        "U-01",
        ["EQ-01"],
        date(2026, 9, 7),
        date(2026, 9, 9),
        current_date=date(2026, 9, 6),
    )

    second = loan_service.create_request(
        "U-01",
        ["EQ-01"],
        date(2026, 9, 8),
        date(2026, 9, 9),
        current_date=date(2026, 9, 6),
    )

    loan_service.approve_request(
        first.id,
        manager,
        current_date=date(2026, 9, 6),
    )

    with pytest.raises(LoanValidationError):
        loan_service.approve_request(
            second.id,
            manager,
            current_date=date(2026, 9, 6),
        )


def test_cancelar_solicitud_aprobada(
    loan_service,
    requester,
    manager,
):
    # TC-15
    loan = loan_service.create_request(
        "U-01",
        ["EQ-01"],
        date(2026, 9, 7),
        date(2026, 9, 9),
        current_date=date(2026, 9, 6),
    )

    loan_service.approve_request(
        loan.id,
        manager,
        current_date=date(2026, 9, 6),
    )

    loan_service.cancel_request(
        loan.id,
        requester,
    )

    assert loan.status == LoanStatus.CANCELADA


def test_entrega_y_devolucion(
    loan_service,
    manager,
):
    # TC-17 + TC-18
    loan = loan_service.create_request(
        "U-01",
        ["EQ-01"],
        date(2026, 9, 7),
        date(2026, 9, 9),
        current_date=date(2026, 9, 6),
    )

    loan_service.approve_request(
        loan.id,
        manager,
        current_date=date(2026, 9, 6),
    )

    loan_service.deliver_loan(
        loan.id,
        manager,
    )

    assert loan.status == LoanStatus.ENTREGADA

    loan_service.return_loan(
        loan.id,
        manager,
    )

    assert loan.status == LoanStatus.DEVUELTA


def test_no_cancelar_prestamo_entregado(
    loan_service,
    requester,
    manager,
):
    # TC-16
    loan = loan_service.create_request(
        "U-01",
        ["EQ-01"],
        date(2026, 9, 7),
        date(2026, 9, 9),
        current_date=date(2026, 9, 6),
    )

    loan_service.approve_request(
        loan.id,
        manager,
        current_date=date(2026, 9, 6),
    )

    loan_service.deliver_loan(
        loan.id,
        manager,
    )

    with pytest.raises(
        InvalidLoanTransitionError
    ):
        loan_service.cancel_request(
            loan.id,
            requester,
        )