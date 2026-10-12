from uuid import UUID

from pydantic import BaseModel, Field


class LessonResponseSchema(BaseModel):
    """Schéma de réponse pour une leçon."""

    id: UUID
    chapter_id: UUID
    title: str
    content: str
    order: int


class LessonListQuerySchema(BaseModel):
    """Schéma de requête pour lister les leçons."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    chapter_id: UUID | None = None


class LessonCreateSchema(BaseModel):
    """Schéma pour créer une leçon."""

    chapter_id: UUID
    title: str
    content: str
    order: int


class LessonUpdateSchema(BaseModel):
    """Schéma pour mettre à jour une leçon."""

    title: str | None = None
    content: str | None = None
    order: int | None = None
