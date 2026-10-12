"""Filtre de base pour les requêtes de listing."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(kw_only=True)
class FiltreEntite:
    """Filtre générique supportant la pagination.

    Tous les filtres de domaine héritent de cette classe
    et ajoutent leurs propres critères.
    """

    page: int = 1
    taille_page: int = 20
    tri_par: str | None = None
    ordre_desc: bool = False

    @property
    def offset(self) -> int:
        """Calcule le décalage SQL à partir de la page courante."""
        return (self.page - 1) * self.taille_page
