"""Filtre de base pour les requêtes de listing."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(kw_only=True)
class EntityFilter:
    """Filtre générique supportant la pagination.

    Tous les filtres de domaine héritent de cette classe
    et ajoutent leurs propres critères.
    """

    page: int = 1
    page_size: int = 20
    sort_by: str | None = None
    sort_desc: bool = False

    @property
    def offset(self) -> int:
        """Calcule le décalage SQL à partir de la page courante."""
        return (self.page - 1) * self.page_size
