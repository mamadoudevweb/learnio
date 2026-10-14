"""Unité de travail SQL générique.

Gère la session, le commit/rollback, l'accès aux repositories
via un registre et la publication des événements de domaine après un commit réussi.
L'unité de travail ne connaît aucun domaine ni repository concret.
"""

from __future__ import annotations

import logging
from typing import Any, Self, overload

from sqlalchemy.orm import Session, sessionmaker

from src.core.entities import BaseEntity
from src.core.repositories.base import BaseRepository
from src.core.unit_of_work.base import UnitOfWork
from src.core.unit_of_work.registry import RepositoryRegistry

logger = logging.getLogger(__name__)


_SUBSCRIBERS: dict[type, list[Any]] = {}


def subscribe(event_type: type, handler: Any) -> None:
    """Enregistre un handler pour un type d'événement donné."""
    _SUBSCRIBERS.setdefault(event_type, []).append(handler)


def publish(event: Any) -> None:
    """Publie un événement à tous les handlers abonnés."""
    for handler in _SUBSCRIBERS.get(type(event), []):
        handler(event)


def clear_subscribers() -> None:
    """Vide tous les abonnements enregistrés (utile pour les tests)."""
    _SUBSCRIBERS.clear()


class SqlUnitOfWork(UnitOfWork):
    """Unité de travail SQL, agnostique des domaines et basée sur un registre.

    Utilisation dans un service :

        with self._uow_factory() as uow:
            repo = uow.get_repository("AccountRepository")
            ...
            uow.track(entity)       # pour publier ses événements
    """

    def __init__(
        self,
        session_factory: sessionmaker[Session],
        registry: RepositoryRegistry | None = None,
        repository_classes: (
            dict[str, type[BaseRepository[Any, Any]]]
            | list[type[BaseRepository[Any, Any]]]
            | None
        ) = None,
    ) -> None:
        self._session_factory = session_factory
        self._registry = registry if registry is not None else RepositoryRegistry()
        if repository_classes:
            self._registry.register_many(repository_classes)
        self._session: Session | None = None
        self._repositories: dict[
            type[BaseRepository[Any, Any]], BaseRepository[Any, Any]
        ] = {}
        self._tracked_entities: list[BaseEntity[Any]] = []

    def __enter__(self) -> Self:
        self._session = self._session_factory()
        self._repositories.clear()
        self._tracked_entities.clear()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        assert self._session is not None
        try:
            if exc_type is None:
                self._session.commit()
                self._publish_events()
            else:
                self._session.rollback()
        finally:
            self._session.close()
            self._session = None

    def register_repos(
        self,
        repo_classes: (
            dict[str, type[BaseRepository[Any, Any]]]
            | list[type[BaseRepository[Any, Any]]]
        ),
    ) -> None:
        """Enregistre des classes de repository dans le registre associé."""
        self._registry.register_many(repo_classes)

    @overload
    def get_repository[R: BaseRepository[Any, Any]](
        self, name_or_cls: type[R]
    ) -> R: ...

    @overload
    def get_repository(self, name_or_cls: str) -> BaseRepository[Any, Any]: ...

    def get_repository[R: BaseRepository[Any, Any]](
        self,
        name_or_cls: str | type[R],
    ) -> R | BaseRepository[Any, Any]:
        """Retourne (ou crée) l'instance du repository demandé par son nom ou sa classe."""
        if self._session is None:
            raise RuntimeError(
                "L'Unité de Travail doit être active (au sein d'un bloc `with uow:`) pour accéder aux repositories."
            )

        repo_cls = self._registry.resolve_class(name_or_cls)

        if repo_cls not in self._repositories:
            self._repositories[repo_cls] = repo_cls(self._session)

        return self._repositories[repo_cls]  # type: ignore[return-value]

    def track(self, entity: BaseEntity[Any]) -> None:
        """Marque une entité pour la publication de ses événements au commit."""
        self._tracked_entities.append(entity)

    def _publish_events(self) -> None:
        """Collecte et publie les événements de toutes les entités suivies."""
        for entity in self._tracked_entities:
            for event in entity.collect_events():
                logger.debug("Publication événement : %s", type(event).__name__)
                publish(event)
        self._tracked_entities.clear()
