"""Role entity for the rbac subdomain of account."""

from __future__ import annotations

from uuid import UUID

from pydantic import Field

from src.core.entities import BaseEntity, EntityId, utc_now
from src.domains.account.rbac.entities.events import (
    PermissionAssignedToRole,
    PermissionRevokedFromRole,
    RoleCreated,
)


class Role(BaseEntity[EntityId]):
    """Rôle RBAC assignable à des comptes utilisateurs."""

    name: str
    description: str | None = None
    permission_ids: list[UUID] = Field(default_factory=list)

    @classmethod
    def create(
        cls,
        *,
        name: str,
        description: str | None = None,
        permission_ids: list[UUID] | None = None,
    ) -> Role:
        role_name = name.strip().lower()
        role = cls(
            name=role_name,
            description=description,
            permission_ids=list(permission_ids) if permission_ids else [],
        )
        role.register_event(RoleCreated(role_id=role.id, name=role_name))
        return role

    def assign_permission(self, permission_id: UUID) -> None:
        """Assigne une permission au rôle."""
        if permission_id not in self.permission_ids:
            self.permission_ids.append(permission_id)
            self.updated_at = utc_now()
            self.register_event(
                PermissionAssignedToRole(
                    role_id=self.id,
                    permission_id=permission_id,
                )
            )

    def revoke_permission(self, permission_id: UUID) -> None:
        """Révoque une permission du rôle."""
        if permission_id in self.permission_ids:
            self.permission_ids.remove(permission_id)
            self.updated_at = utc_now()
            self.register_event(
                PermissionRevokedFromRole(
                    role_id=self.id,
                    permission_id=permission_id,
                )
            )
