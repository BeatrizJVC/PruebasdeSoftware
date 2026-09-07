from src.models.user import User, UserRole
from src.repositories.json_repository import JsonRepository


def test_persistencia_usuario(tmp_path):
    # TC-19 / RF-18 / CA-12

    file_path = tmp_path / "users.json"

    repository = JsonRepository(
        str(file_path),
        User,
    )

    user = User(
        id="U-001",
        name="Ana",
        email="ana@fablab.cl",
        password="1234",
        role=UserRole.SOLICITANTE,
    )

    repository.add(user)

    # Simula cerrar y volver a abrir la aplicación.
    new_repository = JsonRepository(
        str(file_path),
        User,
    )

    recovered_user = new_repository.get_by_id(
        "U-001"
    )

    assert recovered_user is not None
    assert recovered_user.name == "Ana"
    assert recovered_user.email == "ana@fablab.cl"
    assert recovered_user.role == UserRole.SOLICITANTE