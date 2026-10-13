from typing import Any

from src.core.entities import utc_now
from src.core.repositories.base_sql import BaseSqlRepository
from src.domains.account.subs.auth.entities.credential_reset import CredentialReset
from src.domains.account.subs.auth.repositories.filters import CredentialResetFilter
from src.domains.account.subs.auth.repositories.sql import mappers
from src.domains.account.subs.auth.repositories.sql.orms import CredentialResetOrm


class CredentialResetRepository(
    BaseSqlRepository[CredentialReset, CredentialResetFilter]
):
    model = CredentialResetOrm
    mapper = mappers.CredentialResetMapper
    filter_cls = CredentialResetFilter

    def _apply_filter(self, query: Any, filter: CredentialResetFilter) -> Any:
        if filter.credential_id is not None:
            query = query.where(self.model.credential_id == filter.credential_id)
        if filter.token_hash is not None:
            query = query.where(self.model.token_hash == filter.token_hash)
        if filter.is_valid is True:
            now = utc_now()
            query = query.where(
                self.model.used_at.is_(None), self.model.expires_at > now
            )
        elif filter.is_valid is False:
            now = utc_now()
            query = query.where(
                (self.model.used_at.is_not(None)) | (self.model.expires_at <= now)
            )
        return query
