"""Tests unitaires pour les Builders (RepositoryRegistryBuilder, DomainServicesBuilder, AppBuilder)."""

from unittest.mock import MagicMock

from flask import Flask

from src.app.builder import AppBuilder
from src.app.domain_service_builder import (
    AccountServicesBuilder,
    CurriculumServicesBuilder,
    DomainServices,
    DomainServicesBuilder,
    LibraryServicesBuilder,
)
from src.core.builder import BaseBuilder
from src.core.config import ConfigBuilder
from src.core.repositories.base import BaseRepository
from src.core.unit_of_work.registry import (
    RepositoryRegistry,
    RepositoryRegistryBuilder,
)
from src.domains.account.services import AccountDomainService, AccountService
from src.domains.curriculum.services import (
    ChapterService,
    CurriculumDomainService,
    LessonService,
    SubjectService,
)
from src.domains.library.services import DocumentService, LibraryDomainService


class DummyRepo(BaseRepository[object, object]):
    """Repository factice pour les tests."""

    def get(self, criteria: object) -> object | None:
        return None

    def list(self, criteria: object | None = None) -> list[object]:
        return []

    def add(self, entity: object) -> None:
        pass

    def update(self, entity: object) -> None:
        pass

    def delete(self, entity: object) -> None:
        pass


class ConcreteBuilder(BaseBuilder[str]):
    """Builder concret pour tester BaseBuilder."""

    def __init__(self) -> None:
        self.step_called = False

    def do_step(self) -> None:
        self._log_step("Exécution de l'étape de test")
        self.step_called = True

    def build(self) -> str:
        self._log_step("Construction de la valeur")
        return "success"


def test_base_builder_logging_outside_and_inside_flask_context():
    # En dehors d'un contexte Flask
    builder = ConcreteBuilder()
    builder.do_step()
    assert builder.step_called is True
    assert builder.build() == "success"

    # Dans un contexte d'application Flask
    app = Flask("test_logger_app")
    with app.app_context():
        in_ctx_builder = ConcreteBuilder()
        in_ctx_builder.do_step()
        assert in_ctx_builder.build() == "success"


def test_repository_registry_builder_fluent_registration():
    builder = RepositoryRegistryBuilder()
    registry = builder.register(
        DummyRepo, name="DummyRepository", aliases=["dummy", "d"]
    ).build()

    assert isinstance(registry, RepositoryRegistry)
    assert registry.is_registered("DummyRepository")
    assert registry.is_registered("dummy")
    assert registry.is_registered("d")
    assert registry.resolve_class("dummy") is DummyRepo


def test_repository_registry_builder_register_many():
    builder = RepositoryRegistryBuilder()
    registry = builder.register_many({"RepoA": DummyRepo, "RepoB": DummyRepo}).build()

    assert registry.is_registered("RepoA")
    assert registry.is_registered("RepoB")


def test_curriculum_services_builder_with_mocks():
    mock_subject = MagicMock(spec=SubjectService)
    mock_chapter = MagicMock(spec=ChapterService)
    mock_lesson = MagicMock(spec=LessonService)

    curriculum = (
        CurriculumServicesBuilder()
        .with_subject_service(mock_subject)
        .with_chapter_service(mock_chapter)
        .with_lesson_service(mock_lesson)
        .build()
    )

    assert isinstance(curriculum, CurriculumDomainService)
    assert curriculum.subject_service is mock_subject
    assert curriculum.chapter_service is mock_chapter
    assert curriculum.lesson_service is mock_lesson


def test_library_services_builder_with_mocks():
    mock_document = MagicMock(spec=DocumentService)

    library = LibraryServicesBuilder().with_document_service(mock_document).build()

    assert isinstance(library, LibraryDomainService)
    assert library.document_service is mock_document


def test_account_services_builder_with_mocks():
    mock_account = MagicMock(spec=AccountService)
    mock_sender = MagicMock()

    account = (
        AccountServicesBuilder()
        .with_account_service(mock_account)
        .with_email_sender(mock_sender)
        .with_reset_token_expiry(45)
        .with_uow_factory(MagicMock())
        .build()
    )

    assert isinstance(account, AccountDomainService)
    assert account.account_service is mock_account


def test_domain_services_builder_with_sub_builders():
    mock_uow = MagicMock()
    curriculum_builder = CurriculumServicesBuilder(mock_uow)
    library_builder = LibraryServicesBuilder(mock_uow)
    account_builder = AccountServicesBuilder(mock_uow)

    domain_services = (
        DomainServicesBuilder(mock_uow)
        .with_curriculum(curriculum_builder)
        .with_library(library_builder)
        .with_account(account_builder)
        .build()
    )

    assert isinstance(domain_services, DomainServices)
    assert isinstance(domain_services.curriculum, CurriculumDomainService)
    assert isinstance(domain_services.library, LibraryDomainService)
    assert isinstance(domain_services.account, AccountDomainService)
    assert domain_services.auth is domain_services.account
    assert domain_services.access_control is domain_services.account


def test_app_builder_creates_flask_app():
    cfg_builder = ConfigBuilder("testing").with_debug(True).with_email("console")
    app = (
        AppBuilder("test_learnio")
        .with_config_builder(cfg_builder)
        .with_seeds(False)
        .with_routes(True)
        .with_docs(True)
        .build()
    )

    assert isinstance(app, Flask)
    assert app.name == "test_learnio"
    assert "engine" in app.extensions
    assert "db" in app.extensions
    assert "sqlalchemy" in app.extensions
    assert "repository_registry" in app.extensions
    assert "domain_service" in app.extensions
    assert "email_sender" in app.extensions
    assert "email_service" in app.extensions
