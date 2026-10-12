"""Enregistrement des blueprints de tous les domaines.

Sera enrichi à chaque nouveau domaine.
"""

from __future__ import annotations

from flask import Flask

from src.domains.curriculum.routes.v1.chapter_routes import chapter_bp
from src.domains.curriculum.routes.v1.lesson_routes import lesson_bp
from src.domains.curriculum.routes.v1.subject_routes import subject_bp


def register_routes(app: Flask) -> None:
    """Enregistre tous les blueprints de domaine sur l'application Flask."""
    app.register_blueprint(subject_bp)
    app.register_blueprint(chapter_bp)
    app.register_blueprint(lesson_bp)
