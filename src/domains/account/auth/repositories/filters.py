from dataclasses import dataclass
from uuid import UUID

from src.core.repositories.filters import EntityFilter


@dataclass(kw_only=True)
class CredentialFilter(EntityFilter):
    account_id: UUID | None = None
    email: str | None = None


@dataclass(kw_only=True)
class SessionFilter(EntityFilter):
    account_id: UUID | None = None
    token_hash: str | None = None
    is_active: bool | None = None


@dataclass(kw_only=True)
class CredentialResetFilter(EntityFilter):
    credential_id: UUID | None = None
    token_hash: str | None = None
    is_valid: bool | None = None
