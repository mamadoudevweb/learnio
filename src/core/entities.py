"""Entité de base et types fondamentaux pour tous les domaines."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Generic, TypeVar


EntityId = uuid.UUID

ID = TypeVar("ID", bound=EntityId)


def generate_id() -> EntityId:
    """Génère un nouvel identifiant UUID v4."""
    return uuid.uuid4()


def utc_now() -> datetime:
    """Retourne l'instant courant en UTC."""
    return datetime.now(timezone.utc)



@dataclass(frozen=True, kw_only=True)
class DomainEvent:
    """Classe de base pour tous les événements de domaine."""

    timestamp: datetime = field(default_factory=utc_now)



@dataclass(kw_only=True)
class BaseEntity(Generic[ID]):
    """Classe de base commune à toutes les entités du projet.

    Fournit :
    * un identifiant typé ;
    * des horodatages de création / modification ;
    * un registre interne d'événements de domaine.
    """

    id: ID
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    # --- événements de domaine (non persistés) ---
    _events: list[DomainEvent] = field(
        default_factory=list, init=False, repr=False, compare=False
    )

    def register_event(self, event: DomainEvent) -> None:
        """Ajoute un événement de domaine en attente de publication."""
        self._events.append(event)

    def collect_events(self) -> list[DomainEvent]:
        """Retourne puis vide la liste des événements en attente."""
        events = list(self._events)
        self._events.clear()
        return events



T = TypeVar("T")


@dataclass(frozen=True, kw_only=True)
class ServiceResult(Generic[T]):
    """Enveloppe de retour pour toute opération de service réussie."""

    data: T
    meta: dict[str, Any] = field(default_factory=dict)
