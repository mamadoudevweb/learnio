from uuid import UUID

from src.core.entities import ServiceResult
from src.core.services import BaseService, SupportsPermissionCheck
from src.domains.access_control.entities.permission import Permission
from src.domains.access_control.exceptions import (
    PermissionAlreadyExistsError,
    PermissionNotFoundError,
)
from src.domains.access_control.repositories.filters import PermissionFilter
from src.domains.access_control.repositories.sql import PermissionRepository


class PermissionService(BaseService):
    """Service de gestion des permissions RBAC."""

    def get_permission(
        self, actor: SupportsPermissionCheck, permission_id: UUID
    ) -> ServiceResult[Permission]:
        self._authorize(actor, "access_control", "permission", "read")
        with self._uow_factory() as uow:
            repo = uow.get_repository(PermissionRepository)
            perm = repo.get(permission_id)
            if not perm:
                raise PermissionNotFoundError(f"Permission {permission_id} introuvable")
            return ServiceResult(data=perm)

    def list_permissions(
        self, actor: SupportsPermissionCheck, filter: PermissionFilter
    ) -> ServiceResult[list[Permission]]:
        self._authorize(actor, "access_control", "permission", "read")
        with self._uow_factory() as uow:
            repo = uow.get_repository(PermissionRepository)
            perms = repo.list(filter)
            count = repo.count(filter)
            return ServiceResult(data=perms, meta={"total": count})

    def get_or_create(
        self,
        actor: SupportsPermissionCheck,
        *,
        domain: str,
        resource: str,
        action: str,
    ) -> ServiceResult[Permission]:
        self._authorize(actor, "access_control", "permission", "create")
        d, r, a = domain.strip().lower(), resource.strip().lower(), action.strip().lower()
        with self._uow_factory() as uow:
            repo = uow.get_repository(PermissionRepository)
            perm = repo.get(PermissionFilter(domain=d, resource=r, action=a))
            if not perm:
                perm = Permission.create(domain=d, resource=r, action=a)
                repo.add(perm)
                uow.track(perm)
            return ServiceResult(data=perm)

    def delete_permission(
        self, actor: SupportsPermissionCheck, permission_id: UUID
    ) -> ServiceResult[None]:
        self._authorize(actor, "access_control", "permission", "delete")
        with self._uow_factory() as uow:
            repo = uow.get_repository(PermissionRepository)
            perm = repo.get(permission_id)
            if not perm:
                raise PermissionNotFoundError(f"Permission {permission_id} introuvable")
            repo.delete(perm.id)
            return ServiceResult(data=None)
