"""Session entity — belongs to the auth subdomain of account."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from src.core.entities import BaseEntity, EntityId, utc_now
from src.domains.account.auth.entities.events import SessionCreated, SessionRevoked


class Session(BaseEntity[EntityId]):
    """Session utilisateur active identifiée par son jeton cryptographique."""

    account_id: UUID
    token_hash: str
    expires_at: datetime
    ip: str | None = None
    user_agent: str | None = None
    revoked_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        account_id: UUID,
        token_hash: str,
        expires_at: datetime,
        ip: str | None = None,
        user_agent: str | None = None,
    ) -> Session:
        session = cls(
            account_id=account_id,
            token_hash=token_hash,
            expires_at=expires_at,
            ip=ip,
            user_agent=user_agent,
        )
        session.register_event(
            SessionCreated(session_id=session.id, account_id=account_id)
        )
        return session

    def revoke(self) -> None:
        """Révoque la session."""
        self.revoked_at = utc_now()
        self.updated_at = utc_now()
        self.register_event(
            SessionRevoked(session_id=self.id, account_id=self.account_id)
        )

    def is_active(self) -> bool:
        """Vérifie si la session est active et non expirée/révoquée."""
        if self.revoked_at is not None:
            return False
        exp = (
            self.expires_at
            if self.expires_at.tzinfo is not None
            else self.expires_at.replace(tzinfo=UTC)
        )
        return exp > utc_now()
