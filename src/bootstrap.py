from src.models.user import User
from src.models.equipment import Equipment
from src.models.loan import Loan

from src.repositories.json_repository import JsonRepository

from src.services.auth_service import AuthService
from src.services.user_service import UserService
from src.services.equipment_service import EquipmentService
from src.services.loan_service import LoanService


def create_services():
    user_repository = JsonRepository(
        "data/users.json",
        User,
    )

    equipment_repository = JsonRepository(
        "data/equipment.json",
        Equipment,
    )

    loan_repository = JsonRepository(
        "data/loans.json",
        Loan,
    )

    auth_service = AuthService(user_repository)

    user_service = UserService(user_repository)

    equipment_service = EquipmentService(
        equipment_repository
    )

    loan_service = LoanService(
        loan_repository,
        user_repository,
        equipment_repository,
    )

    return {
        "auth": auth_service,
        "users": user_service,
        "equipment": equipment_service,
        "loans": loan_service,
    }