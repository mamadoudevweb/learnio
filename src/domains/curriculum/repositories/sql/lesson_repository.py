from typing import Any

from src.core.repositories.base_sql import BaseSqlRepository
from src.domains.curriculum.entities import Lesson
from src.domains.curriculum.repositories.filters import LessonFilter
from src.domains.curriculum.repositories.sql import mappers
from src.domains.curriculum.repositories.sql.orms import LessonOrm


class LessonRepository(BaseSqlRepository[Lesson, LessonFilter]):
    """Dépôt SQL pour les leçons."""

    model = LessonOrm
    mapper = mappers.LessonMapper
    filter_cls = LessonFilter

    def _apply_filter(self, query: Any, filter: LessonFilter) -> Any:
        if filter.chapter_id is not None:
            query = query.where(self.model.chapter_id == filter.chapter_id)
        return query
