"""Registre générique des classes de repositories pour l'Unité de Travail.

Ce registre est agnostique de toute technologie de stockage (SQL, NoSQL, mémoire).
Il ne dépend que du contrat abstrait ``BaseRepository``.
"""

from __future__ import annotations

import logging
from typing import Any, Self, overload

from src.core.builder import BaseBuilder
from src.core.errors import RepositoryNotFoundError
from src.core.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class RepositoryRegistry:
    """Registre centralisé pour les classes de repositories.

    Permet d'enregistrer des repositories avec un nom canonique et des alias,
    de journaliser chaque enregistrement, et d'instancier un repository
    conforme à ``BaseRepository`` avec le contexte requis.
    """

    def __init__(self) -> None:
        self._registry: dict[str, type[BaseRepository[Any, Any]]] = {}
        self._normalized_registry: dict[str, type[BaseRepository[Any, Any]]] = {}
        self._canonical_names: set[str] = set()

    @staticmethod
    def _normalize_key(key: str) -> str:
        """Normalise une clé pour une recherche tolérante (minuscules, sans underscore)."""
        normalized = key.lower().replace("_", "")
        if normalized.endswith("repository") and len(normalized) > len("repository"):
            return normalized[: -len("repository")]
        return normalized

    def register(
        self,
        repo_cls: type[BaseRepository[Any, Any]],
        *,
        name: str | None = None,
        aliases: list[str] | None = None,
    ) -> None:
        """Enregistre une classe de repository et journalise l'opération."""
        canonical_name = name or repo_cls.__name__
        self._canonical_names.add(canonical_name)

        keys_to_register = {canonical_name, repo_cls.__name__}
        if aliases:
            keys_to_register.update(aliases)

        for key in keys_to_register:
            self._registry[key] = repo_cls
            norm_key = self._normalize_key(key)
            self._normalized_registry[norm_key] = repo_cls

        logger.info(
            "Repository '%s' enregistré (%s) avec alias : %s",
            canonical_name,
            repo_cls.__name__,
            list(keys_to_register),
        )

    def register_many(
        self,
        repos: (
            dict[str, type[BaseRepository[Any, Any]]]
            | list[type[BaseRepository[Any, Any]]]
        ),
    ) -> None:
        """Enregistre plusieurs repositories en une seule opération."""
        if isinstance(repos, dict):
            for name, repo_cls in repos.items():
                self.register(repo_cls, name=name)
        else:
            for repo_cls in repos:
                self.register(repo_cls)

    def is_registered(self, name_or_cls: str | type[Any]) -> bool:
        """Vérifie si un repository est enregistré."""
        if isinstance(name_or_cls, str):
            if name_or_cls in self._registry:
                return True
            return self._normalize_key(name_or_cls) in self._normalized_registry
        if isinstance(name_or_cls, type):
            if name_or_cls in self._registry.values():
                return True
            return name_or_cls.__name__ in self._registry
        return False

    def registered_names(self) -> list[str]:
        """Retourne la liste des noms canoniques enregistrés."""
        return sorted(self._canonical_names)

    @overload
    def resolve_class[R: BaseRepository[Any, Any]](
        self, name_or_cls: type[R]
    ) -> type[R]: ...

    @overload
    def resolve_class(self, name_or_cls: str) -> type[BaseRepository[Any, Any]]: ...

    def resolve_class[R: BaseRepository[Any, Any]](
        self, name_or_cls: str | type[R]
    ) -> type[R | BaseRepository[Any, Any]]:
        """Résout la classe de repository à partir d'un nom, alias ou de la classe."""
        if isinstance(name_or_cls, str):
            repo_cls = self._registry.get(name_or_cls)
            if repo_cls is None:
                norm_key = self._normalize_key(name_or_cls)
                repo_cls = self._normalized_registry.get(norm_key)
            if repo_cls is None:
                available = ", ".join(self.registered_names()) or "(aucun)"
                raise RepositoryNotFoundError(
                    f"Repository '{name_or_cls}' non enregistré dans le registre. "
                    f"Repositories disponibles : {available}"
                )
            return repo_cls

        if isinstance(name_or_cls, type):
            if name_or_cls in self._registry.values():
                return name_or_cls
            if name_or_cls.__name__ in self._registry:
                return self._registry[name_or_cls.__name__]  # type: ignore[return-value]
            available = ", ".join(self.registered_names()) or "(aucun)"
            raise RepositoryNotFoundError(
                f"Classe de repository '{name_or_cls.__name__}' non enregistrée dans le registre. "
                f"Repositories disponibles : {available}"
            )

        raise TypeError(
            f"Le nom ou type de repository doit être une chaîne ou une classe de repository, "
            f"reçu : {type(name_or_cls).__name__}"
        )

    @overload
    def create[R: BaseRepository[Any, Any]](
        self, name_or_cls: type[R], *args: Any, **kwargs: Any
    ) -> R: ...

    @overload
    def create(
        self, name_or_cls: str, *args: Any, **kwargs: Any
    ) -> BaseRepository[Any, Any]: ...

    def create[R: BaseRepository[Any, Any]](
        self,
        name_or_cls: str | type[R],
        *args: Any,
        **kwargs: Any,
    ) -> R | BaseRepository[Any, Any]:
        """Résout et instancie un repository avec les arguments fournis."""
        repo_cls = self.resolve_class(name_or_cls)
        return repo_cls(*args, **kwargs)

    def to_dict(self) -> dict[str, type[BaseRepository[Any, Any]]]:
        """Retourne un dictionnaire des classes canoniques enregistrées."""
        return {
            name: self._registry[name]
            for name in self._canonical_names
            if name in self._registry
        }

    def clear(self) -> None:
        """Vide le registre (utile pour les tests)."""
        self._registry.clear()
        self._normalized_registry.clear()
        self._canonical_names.clear()


class RepositoryRegistryBuilder(BaseBuilder[RepositoryRegistry]):
    """Builder fluide pour construire et configurer un RepositoryRegistry."""

    def __init__(self, registry: RepositoryRegistry | None = None) -> None:
        self._registry = registry if registry is not None else RepositoryRegistry()
        self._log_step("RepositoryRegistryBuilder initialisé")

    def register(
        self,
        repo_cls: type[BaseRepository[Any, Any]],
        *,
        name: str | None = None,
        aliases: list[str] | None = None,
    ) -> Self:
        """Enregistre une classe de repository avec son nom canonique et ses alias."""
        self._registry.register(repo_cls, name=name, aliases=aliases)
        self._log_step(
            "Repository '%s' ajouté au builder (alias=%s)",
            name or repo_cls.__name__,
            aliases or [],
        )
        return self

    def register_many(
        self,
        repos: (
            dict[str, type[BaseRepository[Any, Any]]]
            | list[type[BaseRepository[Any, Any]]]
        ),
    ) -> Self:
        """Enregistre plusieurs classes de repositories."""
        self._registry.register_many(repos)
        self._log_step(
            "Enregistrement en lot de repositories (%s éléments)", len(repos)
        )
        return self

    def build(self) -> RepositoryRegistry:
        """Finalise et retourne le registre de repositories construit."""
        self._log_step(
            "Construction du RepositoryRegistry terminée avec %d repositories",
            len(self._registry.registered_names()),
        )
        return self._registry
