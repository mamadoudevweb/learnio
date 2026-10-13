from typing import Any

from src.core.entities import utc_now
from src.core.repositories.base_sql import BaseSqlRepository
from src.domains.account.subs.auth.entities.session import Session
from src.domains.account.subs.auth.repositories.filters import SessionFilter
from src.domains.account.subs.auth.repositories.sql import mappers
from src.domains.account.subs.auth.repositories.sql.orms import SessionOrm


class SessionRepository(BaseSqlRepository[Session, SessionFilter]):
    model = SessionOrm
    mapper = mappers.SessionMapper
    filter_cls = SessionFilter

    def _apply_filter(self, query: Any, filter: SessionFilter) -> Any:
        if filter.account_id is not None:
            query = query.where(self.model.account_id == filter.account_id)
        if filter.token_hash is not None:
            query = query.where(self.model.token_hash == filter.token_hash)
        if filter.is_active is True:
            now = utc_now()
            query = query.where(
                self.model.revoked_at.is_(None), self.model.expires_at > now
            )
        elif filter.is_active is False:
            now = utc_now()
            query = query.where(
                (self.model.revoked_at.is_not(None)) | (self.model.expires_at <= now)
            )
        return query
