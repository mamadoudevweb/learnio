"""Exceptions du domaine curriculum."""

from src.core.errors import ConflictError, NotFoundError


class SubjectNotFoundError(NotFoundError):
    """Levée quand la matière n'existe pas."""
    code = "CURRICULUM_SUBJECT_NOT_FOUND"


class ChapterNotFoundError(NotFoundError):
    """Levée quand le chapitre n'existe pas."""
    code = "CURRICULUM_CHAPTER_NOT_FOUND"


class LessonNotFoundError(NotFoundError):
    """Levée quand la leçon n'existe pas."""
    code = "CURRICULUM_LESSON_NOT_FOUND"
