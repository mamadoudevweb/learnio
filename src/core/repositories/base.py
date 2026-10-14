"""Classe de base abstraite pour tous les repositories."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from src.core.entities import BaseEntity, EntityId
from src.core.repositories.filters import EntityFilter


class BaseRepository[E: BaseEntity[Any], F: EntityFilter](ABC):
    """Contrat abstrait pour tous les repositories du système.

    Définit les opérations de base de persistance et de consultation,
    indépendamment de la technologie sous-jacente (SQL, mémoire, NoSQL, etc.).
    """

    @abstractmethod
    def get(self, criteria: EntityId | F) -> E | None:
        """Retourne une entité par son identifiant ou selon un filtre."""
        ...

    @abstractmethod
    def list(self, filter: F) -> list[E]:
        """Retourne la liste paginée d'entités correspondant au filtre."""
        ...

    @abstractmethod
    def count(self, filter: F) -> int:
        """Retourne le nombre total d'entités correspondant au filtre."""
        ...

    @abstractmethod
    def add(self, entity: E) -> E:
        """Persiste une nouvelle entité et la retourne."""
        ...

    @abstractmethod
    def update(self, entity: E) -> E:
        """Met à jour une entité existante et la retourne."""
        ...

    @abstractmethod
    def delete(self, entity_id: EntityId) -> None:
        """Supprime une entité par son identifiant."""
        ...
