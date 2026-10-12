from dataclasses import dataclass
from uuid import UUID

from src.core.repositories.filters import EntityFilter


@dataclass(kw_only=True)
class SubjectFilter(EntityFilter):
    """Filtre pour les matières."""

    is_active: bool | None = None
    code: str | None = None


@dataclass(kw_only=True)
class ChapterFilter(EntityFilter):
    """Filtre pour les chapitres."""

    subject_id: UUID | None = None


@dataclass(kw_only=True)
class LessonFilter(EntityFilter):
    """Filtre pour les leçons."""

    chapter_id: UUID | None = None
