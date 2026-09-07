from src.models.user import User, UserRole
from src.repositories.json_repository import JsonRepository
from src.utils.logger import get_logger


logger = get_logger(__name__)


class AuthenticationError(Exception):
    """Error de autenticación."""
    pass


class AuthorizationError(Exception):
    """Error de autorización o permisos."""
    pass


class AuthService:
    def __init__(
        self,
        user_repository: JsonRepository,
    ):
        self.user_repository = user_repository

    def login(
        self,
        email: str,
        password: str,
    ) -> User:
        """
        RF-01 / CA-01 / CA-02

        Autentica un usuario mediante correo y contraseña.
        """

        if not email or not password:
            logger.warning(
                "Intento de inicio de sesión "
                "con datos incompletos."
            )

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
            logger.warning(
                "Intento de inicio de sesión fallido: "
                "usuario inexistente."
            )

            raise AuthenticationError(
                "Correo o contraseña incorrectos."
            )

        if not user.enabled:
            logger.warning(
                "Intento de acceso de usuario "
                "deshabilitado. Usuario=%s",
                user.id,
            )

            raise AuthenticationError(
                "El usuario se encuentra deshabilitado."
            )

        if user.password != password:
            logger.warning(
                "Intento de inicio de sesión fallido. "
                "Usuario=%s",
                user.id,
            )

            raise AuthenticationError(
                "Correo o contraseña incorrectos."
            )

        logger.info(
            "Inicio de sesión exitoso. "
            "Usuario=%s Rol=%s",
            user.id,
            user.role.value,
        )

        return user

    def require_role(
        self,
        user: User,
        required_role: UserRole,
    ) -> None:
        """
        RF-02

        Comprueba que el usuario tenga el rol requerido
        para ejecutar una operación.
        """

        if user is None:
            logger.warning(
                "Intento de operación sin usuario autenticado."
            )

            raise AuthorizationError(
                "Debe iniciar sesión para realizar esta operación."
            )

        if not user.enabled:
            logger.warning(
                "Usuario deshabilitado intentó ejecutar "
                "una operación. Usuario=%s",
                user.id,
            )

            raise AuthorizationError(
                "El usuario se encuentra deshabilitado."
            )

        if user.role != required_role:
            logger.warning(
                "Acceso denegado por rol. "
                "Usuario=%s RolActual=%s RolRequerido=%s",
                user.id,
                user.role.value,
                required_role.value,
            )

            raise AuthorizationError(
                f"La operación requiere el rol "
                f"{required_role.value}."
            )

        logger.info(
            "Autorización concedida. "
            "Usuario=%s Rol=%s",
            user.id,
            user.role.value,
        )