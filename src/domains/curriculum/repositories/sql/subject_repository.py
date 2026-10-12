from typing import Any

from src.core.repositories.base_sql import BaseSqlRepository
from src.domains.curriculum.entities import Subject
from src.domains.curriculum.repositories.filters import SubjectFilter
from src.domains.curriculum.repositories.sql import mappers
from src.domains.curriculum.repositories.sql.orms import SubjectOrm


class SubjectRepository(BaseSqlRepository[Subject, SubjectFilter]):
    """Dépôt SQL pour les matières."""

    model = SubjectOrm
    mapper = mappers.SubjectMapper
    filter_cls = SubjectFilter

    def _apply_filter(self, query: Any, filter: SubjectFilter) -> Any:
        if filter.is_active is not None:
            query = query.where(self.model.is_active == filter.is_active)
        if filter.code is not None:
            query = query.where(self.model.code == filter.code)
        return query
