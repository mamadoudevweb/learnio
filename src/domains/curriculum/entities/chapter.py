from dataclasses import dataclass

from src.core.entities import BaseEntity, EntityId, generate_id


@dataclass(kw_only=True)
class Chapter(BaseEntity[EntityId]):
    """Chapitre d'une matière."""

    subject_id: EntityId
    title: str
    description: str = ""
    order: int

    @classmethod
    def create(
        cls, subject_id: EntityId, title: str, order: int, description: str = ""
    ) -> "Chapter":
        return cls(
            id=generate_id(),
            subject_id=subject_id,
            title=title,
            description=description,
            order=order,
        )
