from src.domains.auth.entities.role import Role
from src.domains.auth.entities.permission import Permission
from src.domains.auth.repositories.sql import RoleRepository, PermissionRepository
from src.domains.auth.repositories.filters import RoleFilter, PermissionFilter
from typing import Callable


def seed_admin_role(uow_factory: Callable) -> None:
    """Create an admin role that has all permissions.

    This function runs at application start‑up after permissions have been seeded.
    It ensures a role named ``admin`` exists and assigns every existing permission
    to that role.
    """
    with uow_factory() as uow:
        role_repo: RoleRepository = uow.get_repository(RoleRepository)
        perm_repo: PermissionRepository = uow.get_repository(PermissionRepository)

        # Check for existing admin role
        admin_role = role_repo.get(RoleFilter(name="admin"))
        if not admin_role:
            admin_role = Role.create(name="admin", description="Super‑admin role with all permissions")
            role_repo.add(admin_role)
            uow.track(admin_role)

        # Assign all permissions to admin role
        all_permissions = perm_repo.list(PermissionFilter())
        for perm in all_permissions:
            if perm.id not in admin_role.permission_ids:
                admin_role.assign_permission(perm.id)
        role_repo.update(admin_role)
        uow.track(admin_role)
        uow.commit()
