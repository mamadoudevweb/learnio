from uuid import UUID

from pydantic import BaseModel, Field


class SubjectResponseSchema(BaseModel):
    """Schéma de réponse pour une matière."""

    id: UUID
    name: str
    code: str
    is_active: bool


class SubjectListQuerySchema(BaseModel):
    """Schéma de requête pour lister les matières."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    is_active: bool | None = None
    code: str | None = None


class SubjectCreateSchema(BaseModel):
    """Schéma pour créer une matière."""

    name: str
    code: str


class SubjectUpdateSchema(BaseModel):
    """Schéma pour mettre à jour une matière."""

    name: str | None = None
    code: str | None = None
    is_active: bool | None = None
