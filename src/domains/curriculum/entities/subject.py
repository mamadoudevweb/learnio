from src.core.entities import BaseEntity, EntityId


class Subject(BaseEntity[EntityId]):
    """Matière du programme scolaire."""

    name: str
    code: str
    is_active: bool = True

    @classmethod
    def create(cls, name: str, code: str) -> Subject:
        return cls(name=name, code=code)
