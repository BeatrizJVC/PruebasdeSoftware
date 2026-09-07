from src.models.equipment import Equipment, EquipmentStatus
from src.repositories.json_repository import JsonRepository


class EquipmentService:
    def __init__(self, equipment_repository: JsonRepository):
        self.equipment_repository = equipment_repository

    def create_equipment(
        self,
        equipment_id: str,
        name: str,
        category: str,
        description: str,
    ) -> Equipment:
        """
        RF-04 - Registrar equipo.
        """

        if not equipment_id or not name or not category:
            raise ValueError(
                "ID, nombre y categoría son obligatorios."
            )

        existing = self.equipment_repository.get_by_id(equipment_id)

        if existing is not None:
            raise ValueError(
                f"Ya existe un equipo con ID {equipment_id}."
            )

        equipment = Equipment(
            id=equipment_id,
            name=name,
            category=category,
            description=description,
            status=EquipmentStatus.DISPONIBLE,
        )

        self.equipment_repository.add(equipment)

        return equipment

    def get_all_equipment(self) -> list[Equipment]:
        """
        RF-04 / RF-05 - Consultar equipos.
        """
        return self.equipment_repository.get_all()

    def get_equipment_by_id(
        self,
        equipment_id: str,
    ) -> Equipment:
        equipment = self.equipment_repository.get_by_id(
            equipment_id
        )

        if equipment is None:
            raise ValueError(
                f"No existe un equipo con ID {equipment_id}."
            )

        return equipment

    def update_equipment(
        self,
        equipment_id: str,
        name: str | None = None,
        category: str | None = None,
        description: str | None = None,
    ) -> Equipment:
        """
        RF-04 - Modificar equipo.
        """

        equipment = self.get_equipment_by_id(equipment_id)

        if name is not None:
            equipment.name = name

        if category is not None:
            equipment.category = category

        if description is not None:
            equipment.description = description

        self.equipment_repository.update(equipment)

        return equipment

    def change_status(
        self,
        equipment_id: str,
        status: EquipmentStatus,
    ) -> Equipment:
        """
        RF-04 - Cambiar estado del equipo.
        """

        equipment = self.get_equipment_by_id(equipment_id)

        equipment.status = status

        self.equipment_repository.update(equipment)

        return equipment

    def is_available(
        self,
        equipment_id: str,
    ) -> bool:
        """
        RF-05 / RN-06

        Comprueba únicamente la disponibilidad básica
        según el estado actual del equipo.

        Los conflictos por fechas serán comprobados
        posteriormente por LoanService.
        """

        equipment = self.get_equipment_by_id(equipment_id)

        return equipment.status == EquipmentStatus.DISPONIBLE