"""Domain events for the account domain."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from src.core.entities import DomainEvent


@dataclass(frozen=True, kw_only=True)
class AccountCreated(DomainEvent):
    """Émis lorsqu'un compte utilisateur est créé."""

    account_id: UUID
    first_name: str


@dataclass(frozen=True, kw_only=True)
class AccountUpdated(DomainEvent):
    """Émis lorsque les informations d'un compte sont mises à jour."""

    account_id: UUID


@dataclass(frozen=True, kw_only=True)
class AccountRoleAssigned(DomainEvent):
    """Émis lorsqu'un rôle est attribué à un compte."""

    account_id: UUID
    role_id: UUID


@dataclass(frozen=True, kw_only=True)
class AccountRoleRemoved(DomainEvent):
    """Émis lorsqu'un rôle est retiré d'un compte."""

    account_id: UUID
    role_id: UUID
