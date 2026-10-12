"""Domain events for the rbac subdomain of account."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from src.core.entities import DomainEvent


@dataclass(frozen=True, kw_only=True)
class RoleCreated(DomainEvent):
    """Émis lorsqu'un rôle RBAC est créé."""

    role_id: UUID
    name: str


@dataclass(frozen=True, kw_only=True)
class RoleUpdated(DomainEvent):
    """Émis lorsqu'un rôle RBAC est mis à jour."""

    role_id: UUID


@dataclass(frozen=True, kw_only=True)
class RoleDeleted(DomainEvent):
    """Émis lorsqu'un rôle RBAC est supprimé."""

    role_id: UUID


@dataclass(frozen=True, kw_only=True)
class PermissionAssignedToRole(DomainEvent):
    """Émis lorsqu'une permission est attribuée à un rôle."""

    role_id: UUID
    permission_id: UUID


@dataclass(frozen=True, kw_only=True)
class PermissionRevokedFromRole(DomainEvent):
    """Émis lorsqu'une permission est retirée d'un rôle."""

    role_id: UUID
    permission_id: UUID


@dataclass(frozen=True, kw_only=True)
class PermissionCreated(DomainEvent):
    """Émis lorsqu'une permission est créée."""

    permission_id: UUID
    triplet: str
