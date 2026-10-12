from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class DocumentOrm(Base):
    """Modèle SQLAlchemy pour Document."""

    __tablename__ = "library_documents"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    title: Mapped[str]
    file_path: Mapped[str]
    file_name: Mapped[str]
    file_size_bytes: Mapped[int]
    mime_type: Mapped[str]
    subject_id: Mapped[UUID | None] = mapped_column(nullable=True)
    chapter_id: Mapped[UUID | None] = mapped_column(nullable=True)
    document_type: Mapped[str]
    source: Mapped[str]
    year: Mapped[int | None] = mapped_column(nullable=True)
    extracted_text: Mapped[str | None] = mapped_column(nullable=True)
    is_text_extracted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
