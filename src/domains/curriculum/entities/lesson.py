from src.core.entities import BaseEntity, EntityId


class Lesson(BaseEntity[EntityId]):
    """Leçon structurée appartenant à un chapitre."""

    chapter_id: EntityId
    title: str
    content: str
    order: int

    @classmethod
    def create(
        cls, chapter_id: EntityId, title: str, content: str, order: int
    ) -> Lesson:
        return cls(
            chapter_id=chapter_id,
            title=title,
            content=content,
            order=order,
        )
