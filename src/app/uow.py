"""Dictionnaire des classes de repository par domaine.

Ajouter un domaine = ajouter une entrée ici.
Le core ne change jamais.
"""

from __future__ import annotations

from typing import Any

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
