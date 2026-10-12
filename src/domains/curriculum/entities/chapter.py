from src.core.entities import BaseEntity, EntityId


class Chapter(BaseEntity[EntityId]):
    """Chapitre d'une matière."""

    subject_id: EntityId
    title: str
    description: str = ""
    order: int

    @classmethod
    def create(
        cls, subject_id: EntityId, title: str, order: int, description: str = ""
    ) -> Chapter:
        return cls(
            subject_id=subject_id,
            title=title,
            description=description,
            order=order,
        )
