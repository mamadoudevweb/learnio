from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class ChapterOrm(Base):
    """Modèle SQLAlchemy pour Chapter."""

    __tablename__ = "curriculum_chapters"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    subject_id: Mapped[UUID]
    title: Mapped[str]
    description: Mapped[str]
    order: Mapped[int]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
