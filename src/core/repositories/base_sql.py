"""Repository SQL générique.

Les repositories de domaine héritent de ``BaseSqlRepository``
et ne font que configurer le modèle ORM, le mapper et le filtre.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.core.entities import BaseEntity, EntityId
from src.core.repositories.filters import EntityFilter

E = TypeVar("E", bound=BaseEntity[Any])
F = TypeVar("F", bound=EntityFilter)


class BaseSqlRepository(ABC, Generic[E, F]):
    """Repository SQL de base, générique sur l'entité et le filtre.

    Sous-classes obligatoires :
    * ``model``      — la classe ORM SQLAlchemy
    * ``mapper``     — module avec ``to_entity()`` / ``to_orm()``
    * ``filter_cls`` — le type de filtre de domaine

    Seule ``_apply_filter()`` doit être implémentée.
    """

    model: type[Any]
    mapper: Any  # module contenant to_entity / to_orm
    filter_cls: type[F]

    def __init__(self, session: Session) -> None:
        self._session = session

    # ------------------------------------------------------------------
    # Lecture
    # ------------------------------------------------------------------

    def get(self, criteria: EntityId | F) -> E | None:
        """Retourne une entité par clé primaire ou par filtre."""
        if isinstance(criteria, UUID):
            orm_obj = self._session.get(self.model, criteria)
            return self.mapper.to_entity(orm_obj) if orm_obj else None

        results = self.list(criteria)
        return results[0] if results else None

    def list(self, filter: F) -> list[E]:
        """Retourne une liste paginée d'entités selon le filtre."""
        query = select(self.model)
        query = self._apply_filter(query, filter)

        if filter.sort_by and hasattr(self.model, filter.sort_by):
            column = getattr(self.model, filter.sort_by)
            query = query.order_by(
                column.desc() if filter.sort_desc else column.asc()
            )

        query = query.offset(filter.offset).limit(filter.page_size)
        results = self._session.execute(query).scalars().all()
        return [self.mapper.to_entity(r) for r in results]

    def count(self, filter: F) -> int:
        """Retourne le nombre total d'entités correspondant au filtre."""
        query = select(func.count()).select_from(self.model)
        query = self._apply_filter(query, filter)
        result = self._session.execute(query).scalar()
        return result or 0

    # ------------------------------------------------------------------
    # Écriture
    # ------------------------------------------------------------------

    def add(self, entity: E) -> E:
        """Persiste une nouvelle entité."""
        orm_obj = self.mapper.to_orm(entity)
        self._session.add(orm_obj)
        self._session.flush()
        return self.mapper.to_entity(orm_obj)

    def update(self, entity: E) -> E:
        """Met à jour une entité existante."""
        orm_obj = self._session.get(self.model, entity.id)
        if orm_obj is None:
            raise ValueError(f"{self.model.__name__} avec id={entity.id} introuvable")
        updated_orm = self.mapper.to_orm(entity)
        self._session.merge(updated_orm)
        self._session.flush()
        return entity

    def delete(self, entity_id: EntityId) -> None:
        """Supprime une entité par son identifiant."""
        orm_obj = self._session.get(self.model, entity_id)
        if orm_obj is not None:
            self._session.delete(orm_obj)
            self._session.flush()

    # ------------------------------------------------------------------
    # Abstrait
    # ------------------------------------------------------------------

    @abstractmethod
    def _apply_filter(self, query: Any, filter: F) -> Any:
        """Applique les critères du filtre à la requête SQLAlchemy.

        Chaque repository de domaine implémente cette méthode.
        """
        ...
