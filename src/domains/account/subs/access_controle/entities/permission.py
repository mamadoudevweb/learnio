"""Permission entity for the rbac subdomain of account."""

from __future__ import annotations

from src.core.entities import BaseEntity, EntityId
from src.domains.account.subs.access_controle.entities.events import PermissionCreated


class Permission(BaseEntity[EntityId]):
    """Permission unitaire découpée par domaine, ressource et action."""

    domain: str
    resource: str
    action: str

    @classmethod
    def create(
        cls,
        *,
        domain: str,
        resource: str,
        action: str,
    ) -> Permission:
        d = domain.strip().lower()
        r = resource.strip().lower()
        a = action.strip().lower()
        perm = cls(
            domain=d,
            resource=r,
            action=a,
        )
        perm.register_event(
            PermissionCreated(permission_id=perm.id, triplet=perm.triplet)
        )
        return perm

    @property
    def triplet(self) -> str:
        return f"{self.domain}:{self.resource}:{self.action}"
