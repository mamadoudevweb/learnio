from pydantic import Field
from uuid import UUID

from src.core.entities import BaseEntity, EntityId, utc_now


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
    ) -> "Role":
        return cls(
            name=name.strip().lower(),
            description=description,
            permission_ids=list(permission_ids) if permission_ids else [],
        )

    def assign_permission(self, permission_id: UUID) -> None:
        if permission_id not in self.permission_ids:
            self.permission_ids.append(permission_id)
            self.updated_at = utc_now()

    def revoke_permission(self, permission_id: UUID) -> None:
        if permission_id in self.permission_ids:
            self.permission_ids.remove(permission_id)
            self.updated_at = utc_now()
