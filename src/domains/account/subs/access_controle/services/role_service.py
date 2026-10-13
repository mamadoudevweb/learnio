from uuid import UUID

from src.core.entities import ServiceResult
from src.core.services import BaseService, SupportsPermissionCheck
from src.domains.account.subs.access_controle.entities.permission import Permission
from src.domains.account.subs.access_controle.entities.role import Role
from src.domains.account.subs.access_controle.exceptions import (
    PermissionNotFoundError,
    RoleAlreadyExistsError,
    RoleNotFoundError,
)
from src.domains.account.subs.access_controle.repositories.filters import (
    PermissionFilter,
    RoleFilter,
)
from src.domains.account.subs.access_controle.repositories.sql import (
    PermissionRepository,
    RoleRepository,
)


class RoleService(BaseService):
    """Service de gestion des rôles RBAC."""

    def get_role(
        self, actor: SupportsPermissionCheck, role_id: UUID
    ) -> ServiceResult[Role]:
        self._authorize(actor, "account", "role", "read")
        with self._uow_factory() as uow:
            repo = uow.get_repository(RoleRepository)
            role = repo.get(role_id)
            if not role:
                raise RoleNotFoundError(f"Rôle {role_id} introuvable")
            return ServiceResult(data=role)

    def list_roles(
        self, actor: SupportsPermissionCheck, filter: RoleFilter
    ) -> ServiceResult[list[Role]]:
        self._authorize(actor, "account", "role", "read")
        with self._uow_factory() as uow:
            repo = uow.get_repository(RoleRepository)
            roles = repo.list(filter)
            count = repo.count(filter)
            return ServiceResult(data=roles, meta={"total": count})

    def create_role(
        self,
        actor: SupportsPermissionCheck,
        *,
        name: str,
        description: str | None = None,
        permission_ids: list[UUID] | None = None,
    ) -> ServiceResult[Role]:
        self._authorize(actor, "account", "role", "create")
        clean_name = name.strip().lower()
        with self._uow_factory() as uow:
            repo = uow.get_repository(RoleRepository)
            if repo.get(RoleFilter(name=clean_name)):
                raise RoleAlreadyExistsError(f"Le rôle '{clean_name}' existe déjà")
            role = Role.create(
                name=clean_name, description=description, permission_ids=permission_ids
            )
            repo.add(role)
            uow.track(role)
            return ServiceResult(data=role)

    def assign_permission_to_role(
        self, actor: SupportsPermissionCheck, role_id: UUID, permission_id: UUID
    ) -> ServiceResult[Role]:
        self._authorize(actor, "account", "role", "update")
        with self._uow_factory() as uow:
            role_repo = uow.get_repository(RoleRepository)
            perm_repo = uow.get_repository(PermissionRepository)
            role = role_repo.get(role_id)
            if not role:
                raise RoleNotFoundError(f"Rôle {role_id} introuvable")
            if not perm_repo.get(permission_id):
                raise PermissionNotFoundError(f"Permission {permission_id} introuvable")
            role.assign_permission(permission_id)
            role_repo.update(role)
            uow.track(role)
            return ServiceResult(data=role)

    def revoke_permission_from_role(
        self, actor: SupportsPermissionCheck, role_id: UUID, permission_id: UUID
    ) -> ServiceResult[Role]:
        self._authorize(actor, "account", "role", "update")
        with self._uow_factory() as uow:
            role_repo = uow.get_repository(RoleRepository)
            role = role_repo.get(role_id)
            if not role:
                raise RoleNotFoundError(f"Rôle {role_id} introuvable")
            role.revoke_permission(permission_id)
            role_repo.update(role)
            uow.track(role)
            return ServiceResult(data=role)

    def delete_role(
        self, actor: SupportsPermissionCheck, role_id: UUID
    ) -> ServiceResult[None]:
        self._authorize(actor, "account", "role", "delete")
        with self._uow_factory() as uow:
            repo = uow.get_repository(RoleRepository)
            role = repo.get(role_id)
            if not role:
                raise RoleNotFoundError(f"Rôle {role_id} introuvable")
            repo.delete(role.id)
            return ServiceResult(data=None)

    def get_or_create_permission(
        self,
        actor: SupportsPermissionCheck,
        *,
        domain: str,
        resource: str,
        action: str,
    ) -> ServiceResult[Permission]:
        """Récupère une permission existante ou la crée si elle n'existe pas encore."""
        self._authorize(actor, "account", "permission", "create")
        d = domain.strip().lower()
        r = resource.strip().lower()
        a = action.strip().lower()
        with self._uow_factory() as uow:
            perm_repo = uow.get_repository(PermissionRepository)
            existing = perm_repo.get(PermissionFilter(domain=d, resource=r, action=a))
            if existing:
                return ServiceResult(data=existing)
            perm = Permission.create(domain=d, resource=r, action=a)
            perm_repo.add(perm)
            uow.track(perm)
            return ServiceResult(data=perm)
