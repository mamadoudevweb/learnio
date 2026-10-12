from typing import Any

from src.core.repositories.base_sql import BaseSqlRepository
from src.domains.access_control.entities.permission import Permission
from src.domains.access_control.repositories.filters import PermissionFilter
from src.domains.access_control.repositories.sql import mappers
from src.domains.access_control.repositories.sql.orms import PermissionOrm


class PermissionRepository(BaseSqlRepository[Permission, PermissionFilter]):
    model = PermissionOrm
    mapper = mappers.PermissionMapper
    filter_cls = PermissionFilter

    def _apply_filter(self, query: Any, filter: PermissionFilter) -> Any:
        if filter.domain is not None:
            query = query.where(self.model.domain == filter.domain.strip().lower())
        if filter.resource is not None:
            query = query.where(self.model.resource == filter.resource.strip().lower())
        if filter.action is not None:
            query = query.where(self.model.action == filter.action.strip().lower())
        if filter.triplet is not None:
            parts = filter.triplet.split(":")
            if len(parts) == 3:
                d, r, a = parts
                query = query.where(
                    self.model.domain == d,
                    self.model.resource == r,
                    self.model.action == a,
                )
        return query
