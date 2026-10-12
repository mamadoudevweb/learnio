from src.domains.auth.entities.permission import Permission
from src.domains.auth.repositories.sql import PermissionRepository
from src.domains.auth.repositories.filters import PermissionFilter
from typing import List

# Define default permissions required across the system
DEFAULT_PERMISSIONS: List[Permission] = [
    # Auth domain permissions
    Permission.create(domain="auth", resource="account", action="create"),
    Permission.create(domain="auth", resource="account", action="read"),
    Permission.create(domain="auth", resource="account", action="update"),
    Permission.create(domain="auth", resource="account", action="delete"),
    Permission.create(domain="auth", resource="session", action="create"),
    Permission.create(domain="auth", resource="session", action="read"),
    Permission.create(domain="auth", resource="session", action="delete"),
    Permission.create(domain="auth", resource="role", action="create"),
    Permission.create(domain="auth", resource="role", action="read"),
    Permission.create(domain="auth", resource="role", action="update"),
    Permission.create(domain="auth", resource="role", action="delete"),
    Permission.create(domain="auth", resource="permission", action="create"),
    Permission.create(domain="auth", resource="permission", action="read"),
    Permission.create(domain="auth", resource="permission", action="delete"),
]


def seed_permissions(uow_factory: callable) -> None:
    """Seed the Permission table with DEFAULT_PERMISSIONS.

    This should be invoked during application start‑up, before any request
    handling. It uses a UnitOfWork to ensure atomicity.
    """
    with uow_factory() as uow:
        perm_repo: PermissionRepository = uow.get_repository(PermissionRepository)
        for perm in DEFAULT_PERMISSIONS:
            # Check if permission already exists based on the unique triplet
            existing = perm_repo.get(
                PermissionFilter(domain=perm.domain, resource=perm.resource, action=perm.action)
            )
            if not existing:
                perm_repo.add(perm)
        # Commit any new permissions
        uow.commit()
