"""Modèle ORM de base pour SQLAlchemy.

Tous les modèles ORM de domaine héritent de ``Base``.
"""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Classe déclarative de base pour tous les modèles ORM."""

    pass
