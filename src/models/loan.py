from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum


class LoanStatus(str, Enum):
    SOLICITADA = "SOLICITADA"
    APROBADA = "APROBADA"
    RECHAZADA = "RECHAZADA"
    ENTREGADA = "ENTREGADA"
    DEVUELTA = "DEVUELTA"
    CANCELADA = "CANCELADA"


@dataclass
class Loan:
    id: str
    user_id: str
    equipment_ids: list[str]
    start_date: date
    return_date: date
    status: LoanStatus = LoanStatus.SOLICITADA
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "equipment_ids": self.equipment_ids,
            "start_date": self.start_date.isoformat(),
            "return_date": self.return_date.isoformat(),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            user_id=data["user_id"],
            equipment_ids=data["equipment_ids"],
            start_date=date.fromisoformat(data["start_date"]),
            return_date=date.fromisoformat(data["return_date"]),
            status=LoanStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
        )