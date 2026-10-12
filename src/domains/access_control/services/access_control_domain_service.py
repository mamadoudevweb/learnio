from dataclasses import dataclass

from src.domains.access_control.services.permission_service import PermissionService
from src.domains.access_control.services.role_service import RoleService


@dataclass(frozen=True, kw_only=True)
class AccessControlDomainService:
    """Agrège les services RBAC du domaine access_control."""

    role_service: RoleService
    permission_service: PermissionService
