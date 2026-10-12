"""CredentialReset entity — belongs to the auth subdomain of account."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from src.core.entities import BaseEntity, EntityId, utc_now
from src.domains.account.auth.entities.events import (
    PasswordResetCompleted,
    PasswordResetRequested,
)


class CredentialReset(BaseEntity[EntityId]):
    """Demande de réinitialisation de mot de passe à usage unique."""

    credential_id: UUID
    token_hash: str
    expires_at: datetime
    used_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        credential_id: UUID,
        token_hash: str,
        expires_at: datetime,
        email: str,
    ) -> CredentialReset:
        reset = cls(
            credential_id=credential_id,
            token_hash=token_hash,
            expires_at=expires_at,
            used_at=None,
        )
        reset.register_event(
            PasswordResetRequested(
                reset_id=reset.id,
                credential_id=credential_id,
                email=email,
            )
        )
        return reset

    def consume(self) -> None:
        """Consomme le jeton de réinitialisation (usage unique)."""
        self.used_at = utc_now()
        self.updated_at = utc_now()
        self.register_event(
            PasswordResetCompleted(
                reset_id=self.id,
                credential_id=self.credential_id,
            )
        )

    def is_valid(self) -> bool:
        """Indique si la demande est valide (non utilisée et non expirée)."""
        if self.used_at is not None:
            return False
        exp = (
            self.expires_at
            if self.expires_at.tzinfo is not None
            else self.expires_at.replace(tzinfo=UTC)
        )
        return exp > utc_now()
