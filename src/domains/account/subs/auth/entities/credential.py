"""Credential entity — belongs to the auth subdomain of account."""

from __future__ import annotations

from uuid import UUID

from src.core.entities import BaseEntity, EntityId, utc_now
from src.domains.account.subs.auth.entities.events import (
    CredentialCreated,
    PasswordChanged,
)


class Credential(BaseEntity[EntityId]):
    """Informations de connexion (email, mot de passe chiffré)."""

    account_id: UUID
    email: str
    password_hash: str
    email_verified: bool = False

    @classmethod
    def create(
        cls,
        *,
        account_id: UUID,
        email: str,
        password_hash: str,
        email_verified: bool = False,
    ) -> Credential:
        normalized_email = email.strip().lower()
        credential = cls(
            account_id=account_id,
            email=normalized_email,
            password_hash=password_hash,
            email_verified=email_verified,
        )
        credential.register_event(
            CredentialCreated(
                credential_id=credential.id,
                account_id=account_id,
                email=normalized_email,
            )
        )
        return credential

    def change_password(self, new_password_hash: str) -> None:
        """Modifie le mot de passe de l'utilisateur."""
        self.password_hash = new_password_hash
        self.updated_at = utc_now()
        self.register_event(
            PasswordChanged(
                credential_id=self.id,
                account_id=self.account_id,
            )
        )

    def verify_email(self) -> None:
        """Marque l'adresse email comme vérifiée."""
        self.email_verified = True
        self.updated_at = utc_now()
