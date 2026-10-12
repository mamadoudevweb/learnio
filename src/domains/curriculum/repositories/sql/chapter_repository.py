from typing import Any

from src.core.repositories.base_sql import BaseSqlRepository
from src.domains.curriculum.entities import Chapter
from src.domains.curriculum.repositories.filters import ChapterFilter
from src.domains.curriculum.repositories.sql import mappers
from src.domains.curriculum.repositories.sql.orms import ChapterOrm


class ChapterRepository(BaseSqlRepository[Chapter, ChapterFilter]):
    """Dépôt SQL pour les chapitres."""

    model = ChapterOrm
    mapper = mappers.ChapterMapper
    filter_cls = ChapterFilter

    def _apply_filter(self, query: Any, filter: ChapterFilter) -> Any:
        if filter.subject_id is not None:
            query = query.where(self.model.subject_id == filter.subject_id)
        return query
