from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class LessonOrm(Base):
    """Modèle SQLAlchemy pour Lesson."""

    __tablename__ = "curriculum_lessons"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    chapter_id: Mapped[UUID]
    title: Mapped[str]
    content: Mapped[str]
    order: Mapped[int]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
