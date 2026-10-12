from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.domains.library.entities.enums import DocumentSource, DocumentType


class DocumentCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    file_path: str = Field(..., min_length=1)
    file_name: str = Field(..., min_length=1)
    file_size_bytes: int = Field(..., gt=0)
    mime_type: str = Field(default="application/pdf")
    subject_id: UUID | None = None
    chapter_id: UUID | None = None
    document_type: DocumentType = DocumentType.OTHER
    source: DocumentSource = DocumentSource.USER
    year: int | None = Field(default=None, ge=1990, le=2100)
    extracted_text: str | None = None


class DocumentUpdateSchema(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    subject_id: UUID | None = None
    chapter_id: UUID | None = None
    document_type: DocumentType | None = None
    year: int | None = Field(default=None, ge=1990, le=2100)
    extracted_text: str | None = None


class DocumentListQuerySchema(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    subject_id: UUID | None = None
    chapter_id: UUID | None = None
    document_type: DocumentType | None = None
    source: DocumentSource | None = None
    year: int | None = None
    search: str | None = None


class DocumentResponseSchema(BaseModel):
    id: UUID
    title: str
    file_path: str
    file_name: str
    file_size_bytes: int
    mime_type: str
    subject_id: UUID | None = None
    chapter_id: UUID | None = None
    document_type: str
    source: str
    year: int | None = None
    extracted_text: str | None = None
    is_text_extracted: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
