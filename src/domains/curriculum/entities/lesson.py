from dataclasses import dataclass

from src.core.entities import BaseEntity, EntityId, generate_id


@dataclass(kw_only=True)
class Lesson(BaseEntity[EntityId]):
    """Leçon structurée appartenant à un chapitre."""

    chapter_id: EntityId
    title: str
    content: str
    order: int

    @classmethod
    def create(
        cls, chapter_id: EntityId, title: str, content: str, order: int
    ) -> "Lesson":
        return cls(
            id=generate_id(),
            chapter_id=chapter_id,
            title=title,
            content=content,
            order=order,
        )
