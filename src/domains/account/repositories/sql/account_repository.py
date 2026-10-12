from typing import Any
from uuid import UUID

from sqlalchemy import delete, insert, or_

from src.core.repositories.base_sql import BaseSqlRepository
from src.domains.account.entities.account import Account
from src.domains.account.repositories.filters import AccountFilter
from src.domains.account.repositories.sql import mappers
from src.domains.account.repositories.sql.orms.account_orm import AccountOrm, account_roles


class AccountRepository(BaseSqlRepository[Account, AccountFilter]):
    model = AccountOrm
    mapper = mappers.AccountMapper
    filter_cls = AccountFilter

    def _apply_filter(self, query: Any, filter: AccountFilter) -> Any:
        if filter.active is not None:
            query = query.where(self.model.active == filter.active)
        if filter.search:
            pattern = f"%{filter.search}%"
            query = query.where(
                or_(
                    self.model.first_name.ilike(pattern),
                    self.model.last_name.ilike(pattern),
                )
            )
        return query

    def add(self, entity: Account) -> None:
        super().add(entity)
        self._sync_roles(entity.id, entity.role_ids)

    def update(self, entity: Account) -> None:
        super().update(entity)
        self._sync_roles(entity.id, entity.role_ids)

    def _sync_roles(self, account_id: UUID, role_ids: list[UUID]) -> None:
        self._session.execute(
            delete(account_roles).where(account_roles.c.account_id == account_id)
        )
        if role_ids:
            self._session.execute(
                insert(account_roles),
                [{"account_id": account_id, "role_id": rid} for rid in role_ids],
            )
