"""Configuration et enregistrement des repositories par domaine.

Ajouter un domaine = enregistrer son repository ici.
Le core ne change jamais.
"""

from __future__ import annotations

from typing import Any

from src.core.repositories.base import BaseRepository
from src.core.unit_of_work.registry import (
    RepositoryRegistry,
    RepositoryRegistryBuilder,
)
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
    """Crée et initialise le registre de repositories avec tous les domaines via le Builder."""
    return (
        RepositoryRegistryBuilder()
        # Domaine Account & sous-domaines
        .register(
            AccountRepository,
            name="AccountRepository",
            aliases=["account", "account_repository"],
        )
        .register(
            CredentialRepository,
            name="CredentialRepository",
            aliases=["credential", "credential_repository"],
        )
        .register(
            SessionRepository,
            name="SessionRepository",
            aliases=["session", "session_repository"],
        )
        .register(
            CredentialResetRepository,
            name="CredentialResetRepository",
            aliases=["credential_reset", "credential_reset_repository"],
        )
        .register(
            RoleRepository,
            name="RoleRepository",
            aliases=["role", "role_repository"],
        )
        .register(
            PermissionRepository,
            name="PermissionRepository",
            aliases=["permission", "permission_repository"],
        )
        # Domaine Curriculum
        .register(
            SubjectRepository,
            name="SubjectRepository",
            aliases=["subject", "subject_repository"],
        )
        .register(
            ChapterRepository,
            name="ChapterRepository",
            aliases=["chapter", "chapter_repository"],
        )
        .register(
            LessonRepository,
            name="LessonRepository",
            aliases=["lesson", "lesson_repository"],
        )
        # Domaine Library
        .register(
            DocumentRepository,
            name="DocumentRepository",
            aliases=["document", "document_repository"],
        )
        .build()
    )


REPOSITORY_REGISTRY: RepositoryRegistry = create_repository_registry()

# Vue dictionnaire pour rétrocompatibilité
REPOSITORY_CLASSES: dict[str, type[BaseRepository[Any, Any]]] = (
    REPOSITORY_REGISTRY.to_dict()
)
