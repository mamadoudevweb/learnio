from dataclasses import dataclass

from src.core.repositories.filters import EntityFilter


@dataclass(kw_only=True)
class RoleFilter(EntityFilter):
    name: str | None = None


@dataclass(kw_only=True)
class PermissionFilter(EntityFilter):
    domain: str | None = None
    resource: str | None = None
    action: str | None = None
    triplet: str | None = None  # convenience: "domain:resource:action"
