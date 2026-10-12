"""Entité de base et types fondamentaux pour tous les domaines.

BaseEntity utilise Pydantic v2 (BaseModel) pour :
  * la validation automatique des champs à la construction,
  * la sérialisation (model_dump / model_dump_json),
  * la compatibilité directe avec ConfigDict(from_attributes=True) dans les schémas.

DomainEvent et ServiceResult restent des dataclasses gelées (valeurs immuables).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr


EntityId = uuid.UUID

ID = TypeVar("ID", bound=EntityId)


def generate_id() -> EntityId:
    """Génère un nouvel identifiant UUID v4."""
    return uuid.uuid4()


def utc_now() -> datetime:
    """Retourne l'instant courant en UTC."""
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Domain event base (frozen dataclass — pure value object)
# ---------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class DomainEvent:
    """Classe de base pour tous les événements de domaine."""

    timestamp: datetime = field(default_factory=utc_now)


# ---------------------------------------------------------------------------
# Base entity (Pydantic v2 BaseModel)
# ---------------------------------------------------------------------------

class BaseEntity(BaseModel, Generic[ID]):
    """Classe de base commune à toutes les entités du projet.

    Fournit :
    * un identifiant typé UUID ;
    * des horodatages de création / modification ;
    * un registre interne d'événements de domaine (non persisté, non sérialisé).
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: ID = Field(default_factory=generate_id)  # type: ignore[assignment]
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    # Private — excluded from serialisation and schema
    _events: list[DomainEvent] = PrivateAttr(default_factory=list)

    def register_event(self, event: DomainEvent) -> None:
        """Ajoute un événement de domaine en attente de publication."""
        self._events.append(event)

    def collect_events(self) -> list[DomainEvent]:
        """Retourne puis vide la liste des événements en attente."""
        events = list(self._events)
        self._events.clear()
        return events


# ---------------------------------------------------------------------------
# Service result (frozen dataclass — pure value object)
# ---------------------------------------------------------------------------

T = TypeVar("T")


@dataclass(frozen=True, kw_only=True)
class ServiceResult(Generic[T]):
    """Enveloppe de retour pour toute opération de service réussie."""

    data: T
    meta: dict[str, Any] = field(default_factory=dict)
