from src.models.user import User, UserRole
from src.repositories.json_repository import JsonRepository


class AuthenticationError(Exception):
    """Error de autenticación."""
    pass


class AuthorizationError(Exception):
    """Error de permisos."""
    pass


class AuthService:
    def __init__(self, user_repository: JsonRepository):
        self.user_repository = user_repository

    def login(self, email: str, password: str) -> User:
        """
        RF-01 / CA-01 / CA-02

        Autentica un usuario mediante correo y contraseña.
        """

        if not email or not password:
            raise AuthenticationError(
                "El correo y la contraseña son obligatorios."
            )

        users = self.user_repository.get_all()

        user = next(
            (
                user
                for user in users
                if user.email.lower() == email.lower()
            ),
            None,
        )

        if user is None:
            raise AuthenticationError(
                "Correo o contraseña incorrectos."
            )

        if not user.enabled:
            raise AuthenticationError(
                "El usuario se encuentra deshabilitado."
            )

        if user.password != password:
            raise AuthenticationError(
                "Correo o contraseña incorrectos."
            )

        return user

    def require_role(
        self,
        user: User,
        required_role: UserRole,
    ) -> None:
        """
        RF-02

        Comprueba que un usuario tenga el rol requerido
        para ejecutar una operación.
        """

        if user is None:
            raise AuthorizationError(
                "Debe iniciar sesión para realizar esta operación."
            )

        if not user.enabled:
            raise AuthorizationError(
                "El usuario se encuentra deshabilitado."
            )

        if user.role != required_role:
            raise AuthorizationError(
                f"La operación requiere el rol {required_role.value}."
            )