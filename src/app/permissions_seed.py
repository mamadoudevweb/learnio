from collections.abc import Callable

from src.domains.account.rbac.entities.permission import Permission
from src.domains.account.rbac.repositories.filters import PermissionFilter
from src.domains.account.rbac.repositories.sql import PermissionRepository

# Define default permissions required across the system
DEFAULT_PERMISSIONS: list[Permission] = [
    # Account & Auth domain permissions
    Permission.create(domain="account", resource="account", action="create"),
    Permission.create(domain="account", resource="account", action="read"),
    Permission.create(domain="account", resource="account", action="update"),
    Permission.create(domain="account", resource="account", action="delete"),
    Permission.create(domain="account", resource="session", action="create"),
    Permission.create(domain="account", resource="session", action="read"),
    Permission.create(domain="account", resource="session", action="delete"),
    Permission.create(domain="account", resource="role", action="create"),
    Permission.create(domain="account", resource="role", action="read"),
    Permission.create(domain="account", resource="role", action="update"),
    Permission.create(domain="account", resource="role", action="delete"),
    Permission.create(domain="account", resource="permission", action="create"),
    Permission.create(domain="account", resource="permission", action="read"),
    Permission.create(domain="account", resource="permission", action="delete"),
]


def seed_permissions(uow_factory: Callable) -> None:
    """Seed the Permission table with DEFAULT_PERMISSIONS."""
    with uow_factory() as uow:
        perm_repo: PermissionRepository = uow.get_repository(PermissionRepository)
        for perm in DEFAULT_PERMISSIONS:
            existing = perm_repo.get(
                PermissionFilter(
                    domain=perm.domain, resource=perm.resource, action=perm.action
                )
            )
            if not existing:
                perm_repo.add(perm)
