from dataclasses import dataclass

from src.core.entities import BaseEntity, EntityId, generate_id


@dataclass(kw_only=True)
class Subject(BaseEntity[EntityId]):
    """Matière du programme scolaire."""

    name: str
    code: str
    is_active: bool = True

    @classmethod
    def create(cls, name: str, code: str) -> "Subject":
        return cls(id=generate_id(), name=name, code=code)
