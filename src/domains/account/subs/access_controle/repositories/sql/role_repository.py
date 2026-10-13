from typing import Any
from uuid import UUID

from sqlalchemy import delete, insert

from src.core.repositories.base_sql import BaseSqlRepository
from src.domains.account.subs.access_controle.entities.role import Role
from src.domains.account.subs.access_controle.repositories.filters import RoleFilter
from src.domains.account.subs.access_controle.repositories.sql import mappers
from src.domains.account.subs.access_controle.repositories.sql.orms import (
    RoleOrm,
    role_permissions,
)


class RoleRepository(BaseSqlRepository[Role, RoleFilter]):
    model = RoleOrm
    mapper = mappers.RoleMapper
    filter_cls = RoleFilter

    def _apply_filter(self, query: Any, filter: RoleFilter) -> Any:
        if filter.name is not None:
            query = query.where(self.model.name == filter.name.strip().lower())
        return query

    def add(self, entity: Role) -> None:
        super().add(entity)
        self._sync_permissions(entity.id, entity.permission_ids)

    def update(self, entity: Role) -> None:
        super().update(entity)
        self._sync_permissions(entity.id, entity.permission_ids)

    def _sync_permissions(self, role_id: UUID, permission_ids: list[UUID]) -> None:
        self._session.execute(
            delete(role_permissions).where(role_permissions.c.role_id == role_id)
        )
        if permission_ids:
            self._session.execute(
                insert(role_permissions),
                [{"role_id": role_id, "permission_id": pid} for pid in permission_ids],
            )
