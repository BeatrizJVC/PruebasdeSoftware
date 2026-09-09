import pytest

from src.models.user import UserRole
from src.services.user_service import UserService


class FakeUserRepository:
    def __init__(self):
        self.users = []

    def get_all(self):
        return self.users

    def get_by_id(self, user_id):
        return next(
            (user for user in self.users if user.id == user_id),
            None,
        )

    def add(self, user):
        self.users.append(user)

    def update(self, updated_user):
        for index, user in enumerate(self.users):
            if user.id == updated_user.id:
                self.users[index] = updated_user
                return


@pytest.fixture
def user_service():
    return UserService(FakeUserRepository())


def test_crear_usuario(user_service):
    user = user_service.create_user(
        "U-01",
        "Ana",
        "ana@fablab.cl",
        "1234",
        UserRole.SOLICITANTE,
    )

    assert user.id == "U-01"
    assert user.enabled is True


def test_no_permite_correo_duplicado(user_service):
    user_service.create_user(
        "U-01",
        "Ana",
        "ana@fablab.cl",
        "1234",
        UserRole.SOLICITANTE,
    )

    with pytest.raises(ValueError):
        user_service.create_user(
            "U-02",
            "Pedro",
            "ana@fablab.cl",
            "5678",
            UserRole.SOLICITANTE,
        )


def test_deshabilitar_usuario(user_service):
    user_service.create_user(
        "U-01",
        "Ana",
        "ana@fablab.cl",
        "1234",
        UserRole.SOLICITANTE,
    )

    user = user_service.set_user_enabled(
        "U-01",
        False,
    )

    assert user.enabled is False