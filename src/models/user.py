from dataclasses import dataclass
from enum import Enum


class UserRole(str, Enum):
    SOLICITANTE = "SOLICITANTE"
    ENCARGADO = "ENCARGADO"


@dataclass
class User:
    id: str
    name: str
    email: str
    password: str
    role: UserRole
    enabled: bool = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role.value,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            password=data["password"],
            role=UserRole(data["role"]),
            enabled=data.get("enabled", True),
        )