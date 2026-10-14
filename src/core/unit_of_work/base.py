"""Contrat abstrait pour l'Unité de Travail."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Self, overload

from src.core.entities import BaseEntity
from src.core.repositories.base import BaseRepository


class UnitOfWork(ABC):
    """Classe de base abstraite définissant l'Unité de Travail.

    Gère le cycle de vie de la transaction (contexte manager),
    l'accès aux repositories via un registre, et le suivi des entités
    pour la publication d'événements de domaine post-commit.
    """

    @abstractmethod
    def __enter__(self) -> Self:
        """Démarre la transaction / session."""
        ...

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Valide ou annule la transaction, puis libère les ressources."""
        ...

    @overload
    def get_repository[R: BaseRepository[Any, Any]](
        self, name_or_cls: type[R]
    ) -> R: ...

    @overload
    def get_repository(self, name_or_cls: str) -> BaseRepository[Any, Any]: ...

    @abstractmethod
    def get_repository[R: BaseRepository[Any, Any]](
        self, name_or_cls: str | type[R]
    ) -> R | BaseRepository[Any, Any]:
        """Retourne l'instance du repository demandé par son nom ou sa classe."""
        ...

    @abstractmethod
    def track(self, entity: BaseEntity[Any]) -> None:
        """Marque une entité pour publication de ses événements post-commit."""
        ...


BaseUnitOfWork = UnitOfWork
