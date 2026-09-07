from src.models.user import User, UserRole
from src.repositories.json_repository import JsonRepository


class UserService:
    def __init__(self, user_repository: JsonRepository):
        self.user_repository = user_repository

    def create_user(
        self,
        user_id: str,
        name: str,
        email: str,
        password: str,
        role: UserRole,
    ) -> User:
        """
        RF-03 - Registrar usuario.
        """

        if not user_id or not name or not email or not password:
            raise ValueError(
                "Todos los datos obligatorios del usuario deben ser ingresados."
            )

        users = self.user_repository.get_all()

        if any(user.id == user_id for user in users):
            raise ValueError(
                f"Ya existe un usuario con ID {user_id}."
            )

        if any(user.email.lower() == email.lower() for user in users):
            raise ValueError(
                f"Ya existe un usuario con correo {email}."
            )

        user = User(
            id=user_id,
            name=name,
            email=email,
            password=password,
            role=role,
        )

        self.user_repository.add(user)

        return user

    def get_all_users(self) -> list[User]:
        """
        RF-03 - Consultar usuarios.
        """
        return self.user_repository.get_all()

    def get_user_by_id(self, user_id: str) -> User:
        """
        RF-03 - Consultar usuario por ID.
        """

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise ValueError(
                f"No existe un usuario con ID {user_id}."
            )

        return user

    def update_user(
        self,
        user_id: str,
        name: str | None = None,
        email: str | None = None,
        role: UserRole | None = None,
    ) -> User:
        """
        RF-03 - Modificar usuario.
        """

        user = self.get_user_by_id(user_id)

        users = self.user_repository.get_all()

        if email is not None:
            duplicated_email = any(
                existing.email.lower() == email.lower()
                and existing.id != user_id
                for existing in users
            )

            if duplicated_email:
                raise ValueError(
                    f"Ya existe otro usuario con correo {email}."
                )

            user.email = email

        if name is not None:
            user.name = name

        if role is not None:
            user.role = role

        self.user_repository.update(user)

        return user

    def set_user_enabled(
        self,
        user_id: str,
        enabled: bool,
    ) -> User:
        """
        RF-03 - Habilitar o deshabilitar usuario.
        """

        user = self.get_user_by_id(user_id)

        user.enabled = enabled

        self.user_repository.update(user)

        return user