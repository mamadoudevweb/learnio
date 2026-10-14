"""Configuration et enregistrement des repositories par domaine.

Ajouter un domaine = enregistrer son repository ici.
Le core ne change jamais.
"""

from __future__ import annotations

from typing import Any

from src.core.repositories.base import BaseRepository
from src.core.unit_of_work.registry import RepositoryRegistry
from src.domains.account.repositories.sql import AccountRepository
from src.domains.account.subs.access_controle.repositories.sql import (
    PermissionRepository,
    RoleRepository,
)
from src.domains.account.subs.auth.repositories.sql import (
    CredentialRepository,
    CredentialResetRepository,
    SessionRepository,
)
from src.domains.curriculum.repositories.sql import (
    ChapterRepository,
    LessonRepository,
    SubjectRepository,
)
from src.domains.library.repositories.sql import DocumentRepository


def create_repository_registry() -> RepositoryRegistry:
    """Crée et initialise le registre de repositories avec tous les domaines."""
    registry = RepositoryRegistry()

    # Domaine Account & sous-domaines
    registry.register(
        AccountRepository,
        name="AccountRepository",
        aliases=["account", "account_repository"],
    )
    registry.register(
        CredentialRepository,
        name="CredentialRepository",
        aliases=["credential", "credential_repository"],
    )
    registry.register(
        SessionRepository,
        name="SessionRepository",
        aliases=["session", "session_repository"],
    )
    registry.register(
        CredentialResetRepository,
        name="CredentialResetRepository",
        aliases=["credential_reset", "credential_reset_repository"],
    )
    registry.register(
        RoleRepository,
        name="RoleRepository",
        aliases=["role", "role_repository"],
    )
    registry.register(
        PermissionRepository,
        name="PermissionRepository",
        aliases=["permission", "permission_repository"],
    )

    # Domaine Curriculum
    registry.register(
        SubjectRepository,
        name="SubjectRepository",
        aliases=["subject", "subject_repository"],
    )
    registry.register(
        ChapterRepository,
        name="ChapterRepository",
        aliases=["chapter", "chapter_repository"],
    )
    registry.register(
        LessonRepository,
        name="LessonRepository",
        aliases=["lesson", "lesson_repository"],
    )

    # Domaine Library
    registry.register(
        DocumentRepository,
        name="DocumentRepository",
        aliases=["document", "document_repository"],
    )

    return registry


REPOSITORY_REGISTRY: RepositoryRegistry = create_repository_registry()

# Vue dictionnaire pour rétrocompatibilité
REPOSITORY_CLASSES: dict[str, type[BaseRepository[Any, Any]]] = (
    REPOSITORY_REGISTRY.to_dict()
)
