"""Permission seeding composition root.

Collects permission descriptors defined across all domains and subdomains
and seeds them into the database using PermissionRepository and the Permission entity.
Domains never import the Permission entity across domain boundaries.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from src.domains.account.permissions import PERMISSIONS as ACCOUNT_PERMISSIONS
from src.domains.account.subs.access_controle.entities.permission import Permission
from src.domains.account.subs.access_controle.permissions import (
    PERMISSIONS as ACCESS_CONTROL_PERMISSIONS,
)
from src.domains.account.subs.access_controle.repositories.filters import (
    PermissionFilter,
)
from src.domains.account.subs.access_controle.repositories.sql import (
    PermissionRepository,
)
from src.domains.account.subs.auth.permissions import PERMISSIONS as AUTH_PERMISSIONS
from src.domains.curriculum.permissions import PERMISSIONS as CURRICULUM_PERMISSIONS
from src.domains.library.permissions import PERMISSIONS as LIBRARY_PERMISSIONS

DOMAIN_PERMISSIONS: list[dict[str, str]] = [
    *CURRICULUM_PERMISSIONS,
    *LIBRARY_PERMISSIONS,
    *ACCOUNT_PERMISSIONS,
    *AUTH_PERMISSIONS,
    *ACCESS_CONTROL_PERMISSIONS,
]

DEFAULT_PERMISSIONS: list[Permission] = [
    Permission.create(
        domain=perm["domain"],
        resource=perm["resource"],
        action=perm["action"],
    )
    for perm in DOMAIN_PERMISSIONS
]


def seed_permissions(uow_factory: Callable[[], Any]) -> None:
    """Seed the database with all permissions defined across domains."""
    with uow_factory() as uow:
        perm_repo: PermissionRepository = uow.get_repository(PermissionRepository)
        for perm_def in DOMAIN_PERMISSIONS:
            existing = perm_repo.get(
                PermissionFilter(
                    domain=perm_def["domain"],
                    resource=perm_def["resource"],
                    action=perm_def["action"],
                )
            )
            if not existing:
                new_perm = Permission.create(
                    domain=perm_def["domain"],
                    resource=perm_def["resource"],
                    action=perm_def["action"],
                )
                perm_repo.add(new_perm)
