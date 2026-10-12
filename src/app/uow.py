"""Dictionnaire des classes de repository par domaine.

Ajouter un domaine = ajouter une entrée ici.
Le core ne change jamais.
"""

from __future__ import annotations

from typing import Any

from src.domains.auth.repositories.sql import (
    AccountRepository,
    CredentialRepository,
    CredentialResetRepository,
    PermissionRepository,
    RoleRepository,
    SessionRepository,
)
from src.domains.curriculum.repositories.sql import (
    ChapterRepository,
    LessonRepository,
    SubjectRepository,
)
from src.domains.library.repositories.sql import DocumentRepository

# Sera rempli au fur et à mesure de l'ajout des domaines.
# Format : {"RepositoryName": RepositoryClass}
REPOSITORY_CLASSES: dict[str, type[Any]] = {
    "SubjectRepository": SubjectRepository,
    "ChapterRepository": ChapterRepository,
    "LessonRepository": LessonRepository,
    "DocumentRepository": DocumentRepository,
    "AccountRepository": AccountRepository,
    "CredentialRepository": CredentialRepository,
    "SessionRepository": SessionRepository,
    "CredentialResetRepository": CredentialResetRepository,
    "RoleRepository": RoleRepository,
    "PermissionRepository": PermissionRepository,
}
