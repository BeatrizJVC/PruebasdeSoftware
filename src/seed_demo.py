from src.models.user import UserRole
from src.services.user_service import UserService
from src.services.equipment_service import EquipmentService
from src.bootstrap import create_services


def seed_demo_data():
    services = create_services()

    user_service: UserService = services["users"]
    equipment_service: EquipmentService = services["equipment"]

    # --------------------------------------------------
    # Usuarios
    # --------------------------------------------------

    if not user_service.get_all_users():
        user_service.create_user(
            "U-001",
            "Ana Solicitante",
            "ana@fablab.cl",
            "1234",
            UserRole.SOLICITANTE,
        )

        user_service.create_user(
            "U-002",
            "Pedro Solicitante",
            "pedro@fablab.cl",
            "1234",
            UserRole.SOLICITANTE,
        )

        user_service.create_user(
            "U-003",
            "Elena Encargada",
            "encargada@fablab.cl",
            "admin123",
            UserRole.ENCARGADO,
        )

    # --------------------------------------------------
    # Equipos
    # --------------------------------------------------

    if not equipment_service.get_all_equipment():
        equipment_service.create_equipment(
            "EQ-001",
            "Cámara Canon",
            "Audiovisual",
            "Cámara fotográfica del laboratorio.",
        )

        equipment_service.create_equipment(
            "EQ-002",
            "Trípode",
            "Audiovisual",
            "Trípode para cámara.",
        )

        equipment_service.create_equipment(
            "EQ-003",
            "Micrófono",
            "Audio",
            "Micrófono para grabaciones.",
        )

        equipment_service.create_equipment(
            "EQ-004",
            "Notebook",
            "Computación",
            "Notebook para trabajo en laboratorio.",
        )

        equipment_service.create_equipment(
            "EQ-005",
            "Grabadora",
            "Audio",
            "Grabadora portátil.",
        )

    print("Datos de demostración cargados correctamente.")


if __name__ == "__main__":
    seed_demo_data()