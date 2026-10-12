from uuid import UUID

from pydantic import BaseModel, Field


class ChapterResponseSchema(BaseModel):
    """Schéma de réponse pour un chapitre."""

    id: UUID
    subject_id: UUID
    title: str
    description: str
    order: int


class ChapterListQuerySchema(BaseModel):
    """Schéma de requête pour lister les chapitres."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    subject_id: UUID | None = None


class ChapterCreateSchema(BaseModel):
    """Schéma pour créer un chapitre."""

    subject_id: UUID
    title: str
    order: int
    description: str = ""


class ChapterUpdateSchema(BaseModel):
    """Schéma pour mettre à jour un chapitre."""

    title: str | None = None
    description: str | None = None
    order: int | None = None
