"""Constructeur des services de domaine avec le Builder Pattern.

Fournit des builders individuels pour chaque domaine (Curriculum, Library, Account)
et un builder d'agrégation ``DomainServicesBuilder`` avec journalisation intégrée.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

from src.core.builder import BaseBuilder
from src.core.email import EmailSender
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


class CurriculumServicesBuilder(BaseBuilder[CurriculumDomainService]):
    """Builder pour les services du domaine Curriculum."""

    def __init__(self, uow_factory: Any | None = None) -> None:
        self._uow_factory = uow_factory
        self._subject_service: SubjectService | None = None
        self._chapter_service: ChapterService | None = None
        self._lesson_service: LessonService | None = None
        self._log_step("CurriculumServicesBuilder initialisé")

    def with_uow_factory(self, uow_factory: Any) -> Self:
        """Définit la fabrique d'unités de travail."""
        self._uow_factory = uow_factory
        self._log_step("Curriculum: uow_factory configuré")
        return self

    def with_subject_service(self, service: SubjectService) -> Self:
        """Injecte une instance personnalisée de SubjectService."""
        self._subject_service = service
        self._log_step("Curriculum: SubjectService injecté")
        return self

    def with_chapter_service(self, service: ChapterService) -> Self:
        """Injecte une instance personnalisée de ChapterService."""
        self._chapter_service = service
        self._log_step("Curriculum: ChapterService injecté")
        return self

    def with_lesson_service(self, service: LessonService) -> Self:
        """Injecte une instance personnalisée de LessonService."""
        self._lesson_service = service
        self._log_step("Curriculum: LessonService injecté")
        return self

    def build(self) -> CurriculumDomainService:
        """Construit le CurriculumDomainService."""
        self._log_step("Construction de CurriculumDomainService")
        subject = self._subject_service or SubjectService(self._uow_factory)
        chapter = self._chapter_service or ChapterService(self._uow_factory)
        lesson = self._lesson_service or LessonService(self._uow_factory)
        return CurriculumDomainService(
            subject_service=subject,
            chapter_service=chapter,
            lesson_service=lesson,
        )


class LibraryServicesBuilder(BaseBuilder[LibraryDomainService]):
    """Builder pour les services du domaine Library."""

    def __init__(self, uow_factory: Any | None = None) -> None:
        self._uow_factory = uow_factory
        self._document_service: DocumentService | None = None
        self._log_step("LibraryServicesBuilder initialisé")

    def with_uow_factory(self, uow_factory: Any) -> Self:
        """Définit la fabrique d'unités de travail."""
        self._uow_factory = uow_factory
        self._log_step("Library: uow_factory configuré")
        return self

    def with_document_service(self, service: DocumentService) -> Self:
        """Injecte une instance personnalisée de DocumentService."""
        self._document_service = service
        self._log_step("Library: DocumentService injecté")
        return self

    def build(self) -> LibraryDomainService:
        """Construit le LibraryDomainService."""
        self._log_step("Construction de LibraryDomainService")
        document = self._document_service or DocumentService(self._uow_factory)
        return LibraryDomainService(document_service=document)


class AccountServicesBuilder(BaseBuilder[AccountDomainService]):
    """Builder pour les services du domaine Account."""

    def __init__(self, uow_factory: Any | None = None) -> None:
        self._uow_factory = uow_factory
        self._email_sender: EmailSender | None = None
        self._reset_token_expire_minutes: int = 15
        self._account_service: AccountService | None = None
        self._authentication_service: AuthenticationService | None = None
        self._role_service: RoleService | None = None
        self._permission_service: PermissionService | None = None
        self._log_step("AccountServicesBuilder initialisé")

    def with_uow_factory(self, uow_factory: Any) -> Self:
        """Définit la fabrique d'unités de travail."""
        self._uow_factory = uow_factory
        self._log_step("Account: uow_factory configuré")
        return self

    def with_email_sender(self, sender: EmailSender | None) -> Self:
        """Définit l'expéditeur d'e-mails pour l'authentification."""
        self._email_sender = sender
        self._log_step("Account: email_sender configuré")
        return self

    def with_reset_token_expiry(self, minutes: int) -> Self:
        """Définit la durée d'expiration du jeton de réinitialisation de mot de passe."""
        self._reset_token_expire_minutes = minutes
        self._log_step("Account: reset_token_expire_minutes configuré (%d)", minutes)
        return self

    def with_account_service(self, service: AccountService) -> Self:
        """Injecte une instance personnalisée de AccountService."""
        self._account_service = service
        self._log_step("Account: AccountService injecté")
        return self

    def with_authentication_service(self, service: AuthenticationService) -> Self:
        """Injecte une instance personnalisée de AuthenticationService."""
        self._authentication_service = service
        self._log_step("Account: AuthenticationService injecté")
        return self

    def with_role_service(self, service: RoleService) -> Self:
        """Injecte une instance personnalisée de RoleService."""
        self._role_service = service
        self._log_step("Account: RoleService injecté")
        return self

    def with_permission_service(self, service: PermissionService) -> Self:
        """Injecte une instance personnalisée de PermissionService."""
        self._permission_service = service
        self._log_step("Account: PermissionService injecté")
        return self

    def build(self) -> AccountDomainService:
        """Construit le AccountDomainService."""
        self._log_step("Construction de AccountDomainService")
        account = self._account_service or AccountService(self._uow_factory)
        auth = self._authentication_service or AuthenticationService(
            self._uow_factory,
            email_sender=self._email_sender,
            reset_token_expire_minutes=self._reset_token_expire_minutes,
        )
        role = self._role_service or RoleService(self._uow_factory)
        permission = self._permission_service or PermissionService(self._uow_factory)
        return AccountDomainService(
            account_service=account,
            authentication_service=auth,
            role_service=role,
            permission_service=permission,
        )


class DomainServicesBuilder(BaseBuilder[DomainServices]):
    """Builder fluide global pour la composition des services de domaine."""

    def __init__(self, uow_factory: Any | None = None) -> None:
        self._uow_factory = uow_factory
        self._email_sender: EmailSender | None = None
        self._reset_token_expire_minutes: int = 15
        self._curriculum: CurriculumDomainService | CurriculumServicesBuilder | None = (
            None
        )
        self._library: LibraryDomainService | LibraryServicesBuilder | None = None
        self._account: AccountDomainService | AccountServicesBuilder | None = None
        self._log_step("DomainServicesBuilder initialisé")

    def with_uow_factory(self, uow_factory: Any) -> Self:
        """Définit la fabrique d'unités de travail."""
        self._uow_factory = uow_factory
        self._log_step("DomainServices: uow_factory configuré")
        return self

    def with_email_sender(self, sender: EmailSender | None) -> Self:
        """Définit l'expéditeur d'e-mails pour les services concernés."""
        self._email_sender = sender
        self._log_step("DomainServices: email_sender configuré")
        return self

    def with_reset_token_expiry(self, minutes: int) -> Self:
        """Définit la durée d'expiration des tokens de réinitialisation."""
        self._reset_token_expire_minutes = minutes
        self._log_step(
            "DomainServices: reset_token_expire_minutes configuré (%d)", minutes
        )
        return self

    def with_curriculum(
        self, service: CurriculumDomainService | CurriculumServicesBuilder
    ) -> Self:
        """Injecte une instance ou un builder pour le domaine Curriculum."""
        self._curriculum = service
        self._log_step("DomainServices: Curriculum configuré")
        return self

    def with_library(
        self, service: LibraryDomainService | LibraryServicesBuilder
    ) -> Self:
        """Injecte une instance ou un builder pour le domaine Library."""
        self._library = service
        self._log_step("DomainServices: Library configuré")
        return self

    def with_account(
        self, service: AccountDomainService | AccountServicesBuilder
    ) -> Self:
        """Injecte une instance ou un builder pour le domaine Account."""
        self._account = service
        self._log_step("DomainServices: Account configuré")
        return self

    def build(self) -> DomainServices:
        """Construit le conteneur complet DomainServices."""
        self._log_step("Construction de l'ensemble DomainServices")

        # Résolution Curriculum
        if isinstance(self._curriculum, CurriculumDomainService):
            curriculum = self._curriculum
        elif isinstance(self._curriculum, CurriculumServicesBuilder):
            curriculum = self._curriculum.build()
        else:
            curriculum = CurriculumServicesBuilder(self._uow_factory).build()

        # Résolution Library
        if isinstance(self._library, LibraryDomainService):
            library = self._library
        elif isinstance(self._library, LibraryServicesBuilder):
            library = self._library.build()
        else:
            library = LibraryServicesBuilder(self._uow_factory).build()

        # Résolution Account
        if isinstance(self._account, AccountDomainService):
            account = self._account
        elif isinstance(self._account, AccountServicesBuilder):
            account = self._account.build()
        else:
            account = (
                AccountServicesBuilder(self._uow_factory)
                .with_email_sender(self._email_sender)
                .with_reset_token_expiry(self._reset_token_expire_minutes)
                .build()
            )

        return DomainServices(
            curriculum=curriculum,
            library=library,
            account=account,
        )


def build_domain_services(
    uow_factory: Any,
    email_sender: EmailSender | None = None,
    reset_token_expire_minutes: int = 15,
) -> DomainServices:
    """Construit et retourne le conteneur de services de domaine via DomainServicesBuilder."""
    return (
        DomainServicesBuilder(uow_factory)
        .with_email_sender(email_sender)
        .with_reset_token_expiry(reset_token_expire_minutes)
        .build()
    )


__all__ = [
    "AccountServicesBuilder",
    "CurriculumServicesBuilder",
    "DomainServices",
    "DomainServicesBuilder",
    "LibraryServicesBuilder",
    "build_domain_services",
]
