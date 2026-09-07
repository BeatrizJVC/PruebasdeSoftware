from dataclasses import dataclass
from enum import Enum


class EquipmentStatus(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    PRESTADO = "PRESTADO"
    MANTENIMIENTO = "MANTENIMIENTO"


@dataclass
class Equipment:
    id: str
    name: str
    category: str
    description: str
    status: EquipmentStatus = EquipmentStatus.DISPONIBLE

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            name=data["name"],
            category=data["category"],
            description=data["description"],
            status=EquipmentStatus(data["status"]),
        )