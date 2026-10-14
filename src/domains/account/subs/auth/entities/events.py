"""Domain events for the auth subdomain of account."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from src.core.entities import DomainEvent


@dataclass(frozen=True, kw_only=True)
class CredentialCreated(DomainEvent):
    """Émis lorsqu'un nouvel identifiant (credential) est créé."""

    credential_id: UUID
    account_id: UUID
    email: str


@dataclass(frozen=True, kw_only=True)
class PasswordChanged(DomainEvent):
    """Émis lorsque le mot de passe d'un utilisateur est modifié."""

    credential_id: UUID
    account_id: UUID


@dataclass(frozen=True, kw_only=True)
class SessionCreated(DomainEvent):
    """Émis lorsqu'une nouvelle session utilisateur est ouverte."""

    session_id: UUID
    account_id: UUID


@dataclass(frozen=True, kw_only=True)
class SessionRevoked(DomainEvent):
    """Émis lorsqu'une session utilisateur est révoquée ou fermée."""

    session_id: UUID
    account_id: UUID


@dataclass(frozen=True, kw_only=True)
class PasswordResetRequested(DomainEvent):
    """Émis lorsqu'une demande de réinitialisation de mot de passe est effectuée."""

    reset_id: UUID
    credential_id: UUID
    email: str
    token: str | None = None


@dataclass(frozen=True, kw_only=True)
class PasswordResetCompleted(DomainEvent):
    """Émis lorsqu'une réinitialisation de mot de passe est finalisée avec succès."""

    reset_id: UUID
    credential_id: UUID
