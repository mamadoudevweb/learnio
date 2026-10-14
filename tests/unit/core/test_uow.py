"""Tests unitaires pour l'Unité de Travail et le Registre de Repositories."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.core.entities import BaseEntity, DomainEvent, EntityId
from src.core.errors import RepositoryNotFoundError
from src.core.repositories.base import BaseRepository
from src.core.repositories.base_sql import BaseSqlRepository
from src.core.repositories.filters import EntityFilter
from src.core.unit_of_work import (
    RepositoryRegistry,
    SqlUnitOfWork,
    UnitOfWork,
    clear_subscribers,
    subscribe,
)

# ---------------------------------------------------------------------------
# Dummy classes for testing
# ---------------------------------------------------------------------------


class DummyEntity(BaseEntity[UUID]):
    name: str = "test"


@dataclass
class DummyFilter(EntityFilter):
    pass


class DummyBaseRepository(BaseRepository[DummyEntity, DummyFilter]):
    """Repository abstrait en mémoire ne connaissant rien de SQL."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs

    def get(self, criteria: EntityId | DummyFilter) -> DummyEntity | None:
        return None

    def list(self, filter: DummyFilter) -> list[DummyEntity]:
        return []

    def count(self, filter: DummyFilter) -> int:
        return 0

    def add(self, entity: DummyEntity) -> DummyEntity:
        return entity

    def update(self, entity: DummyEntity) -> DummyEntity:
        return entity

    def delete(self, entity_id: EntityId) -> None:
        pass


class DummySqlRepository(BaseSqlRepository[DummyEntity, DummyFilter]):
    model = MagicMock()
    mapper = MagicMock()
    filter_cls = DummyFilter

    def _apply_filter(self, query: Any, filter: DummyFilter) -> Any:
        return query


# ---------------------------------------------------------------------------
# Tests BaseRepository & BaseSqlRepository inheritance
# ---------------------------------------------------------------------------


def test_base_repository_is_abstract():
    """BaseRepository ne peut pas être instanciée directement."""
    with pytest.raises(TypeError):
        BaseRepository()  # type: ignore[abstract]


def test_base_sql_repository_inherits_from_base_repository():
    """BaseSqlRepository hérite de BaseRepository."""
    assert issubclass(BaseSqlRepository, BaseRepository)


# ---------------------------------------------------------------------------
# Tests UnitOfWork (ABC)
# ---------------------------------------------------------------------------


def test_unit_of_work_is_abstract():
    """UnitOfWork ne peut pas être instanciée directement."""
    with pytest.raises(TypeError):
        UnitOfWork()  # type: ignore[abstract]


def test_sql_uow_inherits_from_unit_of_work():
    """SqlUnitOfWork hérite bien de UnitOfWork."""
    assert issubclass(SqlUnitOfWork, UnitOfWork)


# ---------------------------------------------------------------------------
# Tests RepositoryRegistry
# ---------------------------------------------------------------------------


def test_registry_works_with_generic_base_repository():
    """Le registre fonctionne avec n'importe quel BaseRepository sans dépendre de SQL."""
    registry = RepositoryRegistry()
    registry.register(
        DummyBaseRepository, name="DummyBaseRepository", aliases=["generic_dummy"]
    )

    assert registry.is_registered("generic_dummy")
    instance = registry.create("generic_dummy", "custom_context", option=True)
    assert isinstance(instance, DummyBaseRepository)
    assert instance.args == ("custom_context",)
    assert instance.kwargs == {"option": True}


def test_registry_register_and_create_by_name():
    """Le registre permet d'enregistrer et d'instancier un repository par son nom canonique et ses alias."""
    registry = RepositoryRegistry()
    registry.register(
        DummySqlRepository, name="DummyRepository", aliases=["dummy", "dummy_repo"]
    )

    assert registry.is_registered("DummyRepository")
    assert registry.is_registered("dummy")
    assert registry.is_registered("dummy_repo")
    assert registry.is_registered("DUMMY")  # normalisation insensible à la casse
    assert "DummyRepository" in registry.registered_names()

    session_mock = MagicMock()
    repo_by_name = registry.create("DummyRepository", session_mock)
    assert isinstance(repo_by_name, DummySqlRepository)
    assert repo_by_name._session is session_mock

    repo_by_alias = registry.create("dummy", session_mock)
    assert isinstance(repo_by_alias, DummySqlRepository)


def test_registry_register_and_create_by_class():
    """Le registre permet d'instancier un repository à partir de sa classe."""
    registry = RepositoryRegistry()
    registry.register(DummySqlRepository)

    assert registry.is_registered(DummySqlRepository)

    session_mock = MagicMock()
    repo = registry.create(DummySqlRepository, session_mock)
    assert isinstance(repo, DummySqlRepository)


def test_registry_unregistered_raises_repository_not_found_error():
    """Tenter d'accéder à un repository non enregistré lève RepositoryNotFoundError."""
    registry = RepositoryRegistry()
    session_mock = MagicMock()

    with pytest.raises(RepositoryNotFoundError) as exc_info:
        registry.create("NonExistentRepository", session_mock)

    assert exc_info.value.code == "REPOSITORY_NOT_FOUND"
    assert exc_info.value.status == 500
    assert "NonExistentRepository" in str(exc_info.value)

    with pytest.raises(RepositoryNotFoundError):
        registry.create(DummySqlRepository, session_mock)


def test_registry_logs_registration(caplog):
    """L'enregistrement d'un repository est consigné dans les logs avec logger.info."""
    registry = RepositoryRegistry()
    with caplog.at_level(logging.INFO):
        registry.register(DummySqlRepository, name="DummyRepository", aliases=["dummy"])

    assert "DummyRepository" in caplog.text
    assert "DummySqlRepository" in caplog.text


def test_registry_register_many():
    """register_many enregistre correctement un dictionnaire ou une liste."""
    registry = RepositoryRegistry()
    registry.register_many({"CustomDummy": DummySqlRepository})

    assert registry.is_registered("CustomDummy")


# ---------------------------------------------------------------------------
# Tests SqlUnitOfWork
# ---------------------------------------------------------------------------


def test_sql_uow_caches_repository_per_session():
    """SqlUnitOfWork met en cache les instances de repository durant la session active."""
    registry = RepositoryRegistry()
    registry.register(DummySqlRepository, name="DummyRepository", aliases=["dummy"])

    session_mock = MagicMock()
    uow = SqlUnitOfWork(session_factory=lambda: session_mock, registry=registry)

    with uow:
        repo1 = uow.get_repository("DummyRepository")
        repo2 = uow.get_repository("dummy")
        repo3 = uow.get_repository(DummySqlRepository)

        assert repo1 is repo2
        assert repo2 is repo3


def test_sql_uow_outside_context_raises_runtime_error():
    """get_repository hors du bloc `with uow:` lève RuntimeError."""
    registry = RepositoryRegistry()
    registry.register(DummySqlRepository)
    uow = SqlUnitOfWork(session_factory=lambda: MagicMock(), registry=registry)

    with pytest.raises(RuntimeError, match="L'Unité de Travail doit être active"):
        uow.get_repository("DummyRepository")


def test_sql_uow_register_repos_delegates_to_registry():
    """La méthode register_repos enregistre correctement dans le registre interne."""
    registry = RepositoryRegistry()
    uow = SqlUnitOfWork(session_factory=lambda: MagicMock(), registry=registry)

    uow.register_repos({"DynamicDummy": DummySqlRepository})
    assert registry.is_registered("DynamicDummy")


def test_sql_uow_commit_and_events():
    """Un commit réussi publie les événements des entités suivies."""
    clear_subscribers()
    events_received: list[Any] = []

    @dataclass(frozen=True, kw_only=True)
    class DummyEvent(DomainEvent):
        entity_id: UUID

    subscribe(DummyEvent, lambda evt: events_received.append(evt))

    session_mock = MagicMock()
    uow = SqlUnitOfWork(session_factory=lambda: session_mock)

    entity = DummyEntity()
    entity.register_event(DummyEvent(entity_id=entity.id))

    with uow:
        uow.track(entity)

    session_mock.commit.assert_called_once()
    assert len(events_received) == 1
    assert events_received[0].entity_id == entity.id

    clear_subscribers()


def test_sql_uow_rollback_on_exception():
    """En cas d'exception, un rollback est effectué et aucun événement n'est publié."""
    clear_subscribers()
    events_received: list[Any] = []

    @dataclass(frozen=True, kw_only=True)
    class DummyEvent(DomainEvent):
        entity_id: UUID

    subscribe(DummyEvent, lambda evt: events_received.append(evt))

    session_mock = MagicMock()
    uow = SqlUnitOfWork(session_factory=lambda: session_mock)

    entity = DummyEntity()
    entity.register_event(DummyEvent(entity_id=entity.id))

    with pytest.raises(ValueError, match="Boom"), uow:
        uow.track(entity)
        raise ValueError("Boom")

    session_mock.rollback.assert_called_once()
    assert len(events_received) == 0

    clear_subscribers()
