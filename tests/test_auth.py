import pytest  # pyright: ignore[reportMissingImports]

from src.models.user import User, UserRole
from src.services.auth_service import (
    AuthService,
    AuthenticationError,
    AuthorizationError,
)


class FakeUserRepository:
    """
    Repositorio simple utilizado solo durante las pruebas.
    """

    def __init__(self, users):
        self.users = users

    def get_all(self):
        return self.users


@pytest.fixture
def requester():
    return User(
        id="U-01",
        name="Ana Solicitante",
        email="ana@fablab.cl",
        password="1234",
        role=UserRole.SOLICITANTE,
    )


@pytest.fixture
def manager():
    return User(
        id="U-02",
        name="Elena Encargada",
        email="encargada@fablab.cl",
        password="admin123",
        role=UserRole.ENCARGADO,
    )


@pytest.fixture
def auth_service(requester, manager):
    repository = FakeUserRepository(
        [requester, manager]
    )

    return AuthService(repository)


def test_login_correcto(auth_service):
    # TC-01
    user = auth_service.login(
        "ana@fablab.cl",
        "1234",
    )

    assert user.email == "ana@fablab.cl"
    assert user.role == UserRole.SOLICITANTE


def test_login_contrasena_incorrecta(auth_service):
    # TC-02
    with pytest.raises(AuthenticationError):
        auth_service.login(
            "ana@fablab.cl",
            "incorrecta",
        )


def test_solicitante_no_puede_operacion_encargado(
    auth_service,
    requester,
):
    # TC-03
    with pytest.raises(AuthorizationError):
        auth_service.require_role(
            requester,
            UserRole.ENCARGADO,
        )