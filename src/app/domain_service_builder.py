"""Constructeur des services de domaine.

Instancie chaque service de domaine avec la fabrique d'unités de travail.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.domains.account.services import AccountDomainService, AccountService
from src.domains.account.subs.access_controle.services import (
    PermissionService,
    RoleService,
)
from src.domains.account.subs.auth.services import AuthenticationService
from src.domains.curriculum.services import CurriculumDomainService
from src.domains.curriculum.services.chapter_service import ChapterService
from src.domains.curriculum.services.lesson_service import LessonService
from src.domains.curriculum.services.subject_service import SubjectService
from src.domains.library.services import DocumentService, LibraryDomainService


@dataclass
class DomainServices:
    """Conteneur de tous les services de domaine de l'application."""

    curriculum: CurriculumDomainService
    library: LibraryDomainService
    account: AccountDomainService

    @property
    def auth(self) -> AccountDomainService:
        """Alias pour le sous-domaine auth au sein du domaine account."""
        return self.account

    @property
    def access_control(self) -> AccountDomainService:
        """Alias pour le sous-domaine rbac au sein du domaine account."""
        return self.account


from src.core.email import EmailSender


def build_domain_services(
    uow_factory: Any,
    email_sender: EmailSender | None = None,
    reset_token_expire_minutes: int = 15,
) -> DomainServices:
    """Construit et retourne le conteneur de services de domaine."""
    curriculum = CurriculumDomainService(
        subject_service=SubjectService(uow_factory),
        chapter_service=ChapterService(uow_factory),
        lesson_service=LessonService(uow_factory),
    )
    library = LibraryDomainService(
        document_service=DocumentService(uow_factory),
    )
    account = AccountDomainService(
        account_service=AccountService(uow_factory),
        authentication_service=AuthenticationService(
            uow_factory,
            email_sender=email_sender,
            reset_token_expire_minutes=reset_token_expire_minutes,
        ),
        role_service=RoleService(uow_factory),
        permission_service=PermissionService(uow_factory),
    )
    return DomainServices(curriculum=curriculum, library=library, account=account)
