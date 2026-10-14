"""Modèle ORM de base pour SQLAlchemy et extension Flask-SQLAlchemy.

Tous les modèles ORM de domaine héritent de ``Base``.
L'instance ``db`` fournit l'intégration native avec Flask-SQLAlchemy.
"""

from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Classe déclarative de base pour tous les modèles ORM."""


db: SQLAlchemy = SQLAlchemy(model_class=Base)
