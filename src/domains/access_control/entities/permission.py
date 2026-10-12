"""Role and Permission entities for the access_control bounded-context."""
from pydantic import Field
from uuid import UUID

from src.core.entities import BaseEntity, EntityId, utc_now


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
    ) -> "Permission":
        return cls(
            domain=domain.strip().lower(),
            resource=resource.strip().lower(),
            action=action.strip().lower(),
        )

    @property
    def triplet(self) -> str:
        return f"{self.domain}:{self.resource}:{self.action}"
