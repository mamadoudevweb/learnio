"""Unité de travail SQL générique.

Gère la session, le commit/rollback et la publication
des événements de domaine après un commit réussi.
Le dictionnaire ``REPOSITORY_CLASSES`` est injecté depuis
``app/uow.py`` — le core ne connaît aucun domaine.
"""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy.orm import Session, sessionmaker

from src.core.entities import BaseEntity

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Bus d'événements simplifié (synchrone, in-process)
# ---------------------------------------------------------------------------
_SUBSCRIBERS: dict[type, list[Any]] = {}


def subscribe(event_type: type, handler: Any) -> None:
    """Enregistre un handler pour un type d'événement donné."""
    _SUBSCRIBERS.setdefault(event_type, []).append(handler)


def publish(event: Any) -> None:
    """Publie un événement à tous les handlers abonnés."""
    for handler in _SUBSCRIBERS.get(type(event), []):
        handler(event)


# ---------------------------------------------------------------------------
# Unité de travail
# ---------------------------------------------------------------------------


class SqlUnitOfWork:
    """Unité de travail SQL, agnostique des domaines.

    Utilisation dans un service :

        with self._uow_factory() as uow:
            repo = uow.get_repository(SubjectRepository)
            ...
            uow.track(entity)       # pour publier ses événements
    """

    def __init__(
        self,
        session_factory: sessionmaker[Session],
        repository_classes: dict[str, type[Any]],
    ) -> None:
        self._session_factory = session_factory
        self._repository_classes = repository_classes
        self._session: Session | None = None
        self._repositories: dict[str, Any] = {}
        self._tracked_entities: list[BaseEntity[Any]] = []

    # --- Context manager ---

    def __enter__(self) -> SqlUnitOfWork:
        self._session = self._session_factory()
        self._repositories.clear()
        self._tracked_entities.clear()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
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

    # --- API publique ---

    def get_repository(self, repository_cls: type[Any]) -> Any:
        """Retourne (ou crée) l'instance du repository demandé."""
        name = repository_cls.__name__
        if name not in self._repositories:
            assert self._session is not None
            self._repositories[name] = repository_cls(self._session)
        return self._repositories[name]

    def track(self, entity: BaseEntity[Any]) -> None:
        """Marque une entité pour la publication de ses événements au commit."""
        self._tracked_entities.append(entity)

    # --- Interne ---

    def _publish_events(self) -> None:
        """Collecte et publie les événements de toutes les entités suivies."""
        for entity in self._tracked_entities:
            for event in entity.collect_events():
                logger.debug("Publication événement : %s", type(event).__name__)
                publish(event)
        self._tracked_entities.clear()
