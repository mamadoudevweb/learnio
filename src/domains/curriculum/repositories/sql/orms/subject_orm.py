from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class SubjectOrm(Base):
    """Modèle SQLAlchemy pour Subject."""

    __tablename__ = "curriculum_subjects"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    code: Mapped[str]
    is_active: Mapped[bool]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
