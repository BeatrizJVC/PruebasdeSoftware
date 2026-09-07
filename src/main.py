from datetime import date
from getpass import getpass

from src.bootstrap import create_services
from src.models.equipment import EquipmentStatus
from src.services.auth_service import AuthenticationError
from src.services.loan_service import (
    InvalidLoanTransitionError,
    LoanValidationError,
)
from src.seed_demo import seed_demo_data
from src.utils.logger import (
    configure_logging,
    get_logger,
    init_sentry,
    report_exception,
)


logger = get_logger(__name__)


# ============================================================
# UTILIDADES
# ============================================================

def pause():
    input("\nPresiona ENTER para continuar...")


def read_date(message: str) -> date:
    while True:
        value = input(f"{message} [AAAA-MM-DD]: ").strip()

        try:
            return date.fromisoformat(value)

        except ValueError:
            print(
                "Fecha inválida. "
                "Ejemplo válido: 2026-09-15"
            )


def show_equipment(equipment_list):
    if not equipment_list:
        print("No existen equipos registrados.")
        return

    print("\n--- EQUIPOS ---")

    for equipment in equipment_list:
        print(
            f"{equipment.id} | "
            f"{equipment.name} | "
            f"{equipment.category} | "
            f"{equipment.status.value}"
        )


def show_loans(loans):
    if not loans:
        print("No existen préstamos o solicitudes.")
        return

    print("\n--- SOLICITUDES / PRÉSTAMOS ---")

    for loan in loans:
        print(
            f"{loan.id} | "
            f"Usuario: {loan.user_id} | "
            f"Equipos: {', '.join(loan.equipment_ids)} | "
            f"{loan.start_date} → {loan.return_date} | "
            f"{loan.status.value}"
        )


# ============================================================
# MENÚ SOLICITANTE
# ============================================================

def requester_menu(user, services):
    equipment_service = services["equipment"]
    loan_service = services["loans"]

    while True:
        print("\n==============================")
        print(" MENÚ SOLICITANTE")
        print("==============================")
        print("1. Consultar equipos")
        print("2. Crear solicitud")
        print("3. Consultar mis solicitudes")
        print("4. Cancelar solicitud")
        print("0. Cerrar sesión")

        option = input(
            "\nSeleccione una opción: "
        ).strip()

        try:
            if option == "1":
                show_equipment(
                    equipment_service.get_all_equipment()
                )

            elif option == "2":
                show_equipment(
                    equipment_service.get_all_equipment()
                )

                equipment_input = input(
                    "\nIngrese los IDs de los equipos "
                    "separados por coma: "
                )

                equipment_ids = [
                    item.strip()
                    for item in equipment_input.split(",")
                    if item.strip()
                ]

                start_date = read_date(
                    "Fecha de inicio"
                )

                return_date = read_date(
                    "Fecha de devolución"
                )

                loan = loan_service.create_request(
                    user.id,
                    equipment_ids,
                    start_date,
                    return_date,
                )

                print(
                    f"\nSolicitud {loan.id} "
                    f"creada correctamente."
                )

            elif option == "3":
                show_loans(
                    loan_service.get_user_requests(
                        user.id
                    )
                )

            elif option == "4":
                show_loans(
                    loan_service.get_user_requests(
                        user.id
                    )
                )

                loan_id = input(
                    "\nID de la solicitud a cancelar: "
                ).strip()

                loan = loan_service.cancel_request(
                    loan_id,
                    user,
                )

                print(
                    f"Solicitud {loan.id} cancelada."
                )

            elif option == "0":
                logger.info(
                    "Cierre de sesión. Usuario=%s",
                    user.id,
                )

                print("Sesión cerrada.")
                return

            else:
                print("Opción inválida.")

        except (
            ValueError,
            PermissionError,
            LoanValidationError,
            InvalidLoanTransitionError,
        ) as error:
            print(f"\nError: {error}")

        pause()


# ============================================================
# GESTIÓN DE EQUIPOS - ENCARGADO
# ============================================================

def equipment_management_menu(services):
    equipment_service = services["equipment"]

    while True:
        print("\n--- GESTIÓN DE EQUIPOS ---")
        print("1. Consultar equipos")
        print("2. Registrar equipo")
        print("3. Cambiar estado")
        print("0. Volver")

        option = input("Opción: ").strip()

        try:
            if option == "1":
                show_equipment(
                    equipment_service.get_all_equipment()
                )

            elif option == "2":
                equipment_id = input(
                    "ID: "
                ).strip()

                name = input(
                    "Nombre: "
                ).strip()

                category = input(
                    "Categoría: "
                ).strip()

                description = input(
                    "Descripción: "
                ).strip()

                equipment_service.create_equipment(
                    equipment_id,
                    name,
                    category,
                    description,
                )

                print(
                    "Equipo registrado correctamente."
                )

            elif option == "3":
                show_equipment(
                    equipment_service.get_all_equipment()
                )

                equipment_id = input(
                    "ID del equipo: "
                ).strip()

                print("\nEstados:")
                print("1. DISPONIBLE")
                print("2. PRESTADO")
                print("3. MANTENIMIENTO")

                state_option = input(
                    "Seleccione estado: "
                ).strip()

                states = {
                    "1": EquipmentStatus.DISPONIBLE,
                    "2": EquipmentStatus.PRESTADO,
                    "3": EquipmentStatus.MANTENIMIENTO,
                }

                if state_option not in states:
                    print("Estado inválido.")
                    continue

                equipment_service.change_status(
                    equipment_id,
                    states[state_option],
                )

                print("Estado actualizado.")

            elif option == "0":
                return

            else:
                print("Opción inválida.")

        except ValueError as error:
            print(f"Error: {error}")

        pause()


# ============================================================
# GESTIÓN DE USUARIOS - ENCARGADO
# ============================================================

def user_management_menu(services):
    user_service = services["users"]

    while True:
        print("\n--- GESTIÓN DE USUARIOS ---")
        print("1. Consultar usuarios")
        print("2. Deshabilitar usuario")
        print("3. Habilitar usuario")
        print("0. Volver")

        option = input("Opción: ").strip()

        try:
            if option == "1":
                users = user_service.get_all_users()

                if not users:
                    print(
                        "No existen usuarios registrados."
                    )

                for user in users:
                    state = (
                        "HABILITADO"
                        if user.enabled
                        else "DESHABILITADO"
                    )

                    print(
                        f"{user.id} | "
                        f"{user.name} | "
                        f"{user.email} | "
                        f"{user.role.value} | "
                        f"{state}"
                    )

            elif option in {"2", "3"}:
                user_id = input(
                    "ID del usuario: "
                ).strip()

                enabled = option == "3"

                user_service.set_user_enabled(
                    user_id,
                    enabled,
                )

                print("Usuario actualizado.")

            elif option == "0":
                return

            else:
                print("Opción inválida.")

        except ValueError as error:
            print(f"Error: {error}")

        pause()


# ============================================================
# MENÚ ENCARGADO
# ============================================================

def manager_menu(user, services):
    loan_service = services["loans"]

    while True:
        print("\n==============================")
        print(" MENÚ ENCARGADO")
        print("==============================")
        print("1. Gestión de usuarios")
        print("2. Gestión de equipos")
        print("3. Ver solicitudes pendientes")
        print("4. Aprobar solicitud")
        print("5. Rechazar solicitud")
        print("6. Registrar entrega")
        print("7. Registrar devolución")
        print("8. Ver préstamos vigentes")
        print("9. Ver préstamos futuros")
        print("10. Ver préstamos atrasados")
        print("0. Cerrar sesión")

        option = input(
            "\nSeleccione una opción: "
        ).strip()

        try:
            if option == "1":
                user_management_menu(
                    services
                )

            elif option == "2":
                equipment_management_menu(
                    services
                )

            elif option == "3":
                show_loans(
                    loan_service.get_pending_requests()
                )

            elif option == "4":
                show_loans(
                    loan_service.get_pending_requests()
                )

                loan_id = input(
                    "\nID a aprobar: "
                ).strip()

                loan_service.approve_request(
                    loan_id,
                    user,
                )

                print("Solicitud aprobada.")

            elif option == "5":
                show_loans(
                    loan_service.get_pending_requests()
                )

                loan_id = input(
                    "\nID a rechazar: "
                ).strip()

                loan_service.reject_request(
                    loan_id,
                    user,
                )

                print("Solicitud rechazada.")

            elif option == "6":
                loan_id = input(
                    "ID del préstamo a entregar: "
                ).strip()

                loan_service.deliver_loan(
                    loan_id,
                    user,
                )

                print("Entrega registrada.")

            elif option == "7":
                loan_id = input(
                    "ID del préstamo a devolver: "
                ).strip()

                loan_service.return_loan(
                    loan_id,
                    user,
                )

                print("Devolución registrada.")

            elif option == "8":
                show_loans(
                    loan_service.get_current_loans()
                )

            elif option == "9":
                show_loans(
                    loan_service.get_future_loans()
                )

            elif option == "10":
                show_loans(
                    loan_service.get_overdue_loans()
                )

            elif option == "0":
                logger.info(
                    "Cierre de sesión. Usuario=%s",
                    user.id,
                )

                print("Sesión cerrada.")
                return

            else:
                print("Opción inválida.")

        except (
            ValueError,
            PermissionError,
            LoanValidationError,
            InvalidLoanTransitionError,
        ) as error:
            print(f"\nError: {error}")

        pause()


# ============================================================
# LOGIN / APLICACIÓN
# ============================================================

def main():
    # Configuración de logs y Sentry
    configure_logging()
    init_sentry()

    logger.info(
        "Aplicación iniciada."
    )

    # Carga los datos iniciales
    seed_demo_data()

    # Inicializa servicios
    services = create_services()
    auth_service = services["auth"]

    while True:
        print("\n====================================")
        print(" FABLAB - SISTEMA DE PRÉSTAMOS")
        print("====================================")
        print("1. Iniciar sesión")
        print("0. Salir")

        option = input(
            "\nSeleccione una opción: "
        ).strip()

        if option == "0":
            logger.info(
                "Aplicación finalizada por el usuario."
            )

            print(
                "Aplicación finalizada."
            )

            break

        if option != "1":
            print("Opción inválida.")
            continue

        email = input(
            "Correo: "
        ).strip()

        password = getpass(
            "Contraseña: "
        )

        try:
            user = auth_service.login(
                email,
                password,
            )

            print(
                f"\nBienvenido/a, {user.name}."
            )

            if user.role.value == "SOLICITANTE":
                requester_menu(
                    user,
                    services,
                )

            else:
                manager_menu(
                    user,
                    services,
                )

        except AuthenticationError as error:
            print(
                f"\nError: {error}"
            )


# ============================================================
# PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    try:
        main()

    except Exception as error:
        # Garantiza que el logger exista incluso si el
        # error ocurrió durante el inicio de la aplicación.
        configure_logging()

        logger.exception(
            "Error inesperado no controlado."
        )

        report_exception(
            error
        )

        print(
            "\nOcurrió un error inesperado. "
            "El incidente fue registrado."
        )