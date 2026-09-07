import pytest

from src.models.equipment import EquipmentStatus
from src.services.equipment_service import EquipmentService


class FakeEquipmentRepository:
    def __init__(self):
        self.equipment = []

    def get_all(self):
        return self.equipment

    def get_by_id(self, equipment_id):
        return next(
            (
                equipment
                for equipment in self.equipment
                if equipment.id == equipment_id
            ),
            None,
        )

    def add(self, equipment):
        self.equipment.append(equipment)

    def update(self, updated_equipment):
        for index, equipment in enumerate(self.equipment):
            if equipment.id == updated_equipment.id:
                self.equipment[index] = updated_equipment
                return


@pytest.fixture
def equipment_service():
    return EquipmentService(
        FakeEquipmentRepository()
    )


def test_crear_equipo(equipment_service):
    # TC-04
    equipment = equipment_service.create_equipment(
        "EQ-01",
        "Cámara Canon",
        "Audiovisual",
        "Cámara disponible para préstamo.",
    )

    assert equipment.id == "EQ-01"
    assert equipment.status == EquipmentStatus.DISPONIBLE


def test_no_permite_id_duplicado(equipment_service):
    equipment_service.create_equipment(
        "EQ-01",
        "Cámara Canon",
        "Audiovisual",
        "Cámara",
    )

    with pytest.raises(ValueError):
        equipment_service.create_equipment(
            "EQ-01",
            "Otra cámara",
            "Audiovisual",
            "Otro equipo",
        )


def test_equipo_disponible(equipment_service):
    equipment_service.create_equipment(
        "EQ-01",
        "Cámara Canon",
        "Audiovisual",
        "Cámara",
    )

    assert equipment_service.is_available("EQ-01") is True


def test_equipo_en_mantenimiento_no_disponible(
    equipment_service,
):
    # Parte de TC-12
    equipment_service.create_equipment(
        "EQ-04",
        "Notebook",
        "Computación",
        "Notebook del laboratorio",
    )

    equipment_service.change_status(
        "EQ-04",
        EquipmentStatus.MANTENIMIENTO,
    )

    assert equipment_service.is_available("EQ-04") is False


def test_cambiar_estado_a_prestado(
    equipment_service,
):
    equipment_service.create_equipment(
        "EQ-01",
        "Cámara Canon",
        "Audiovisual",
        "Cámara",
    )

    equipment = equipment_service.change_status(
        "EQ-01",
        EquipmentStatus.PRESTADO,
    )

    assert equipment.status == EquipmentStatus.PRESTADO