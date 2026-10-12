from typing import Any

from src.core.repositories.base_sql import BaseSqlRepository
from src.domains.account.auth.entities.credential import Credential
from src.domains.account.auth.repositories.filters import CredentialFilter
from src.domains.account.auth.repositories.sql import mappers
from src.domains.account.auth.repositories.sql.orms import CredentialOrm


class CredentialRepository(BaseSqlRepository[Credential, CredentialFilter]):
    model = CredentialOrm
    mapper = mappers.CredentialMapper
    filter_cls = CredentialFilter

    def _apply_filter(self, query: Any, filter: CredentialFilter) -> Any:
        if filter.account_id is not None:
            query = query.where(self.model.account_id == filter.account_id)
        if filter.email is not None:
            query = query.where(self.model.email == filter.email.strip().lower())
        return query
