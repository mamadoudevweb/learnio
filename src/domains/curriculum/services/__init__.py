from dataclasses import dataclass

from src.domains.curriculum.services.chapter_service import ChapterService
from src.domains.curriculum.services.lesson_service import LessonService
from src.domains.curriculum.services.permissions import CURRICULUM_PERMISSIONS
from src.domains.curriculum.services.subject_service import SubjectService


@dataclass(kw_only=True)
class CurriculumDomainService:
    """Façade des services du domaine curriculum."""

    subject_service: SubjectService
    chapter_service: ChapterService
    lesson_service: LessonService


__all__ = [
    "CURRICULUM_PERMISSIONS",
    "ChapterService",
    "CurriculumDomainService",
    "LessonService",
    "SubjectService",
]
