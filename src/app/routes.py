"""Enregistrement des blueprints de tous les domaines."""

from __future__ import annotations

from flask import Flask, jsonify

from src.domains.account.auth.routes.v1 import auth_bp
from src.domains.account.rbac.routes.v1 import permission_bp, role_bp
from src.domains.account.routes.v1 import account_bp
from src.domains.curriculum.routes.v1.chapter_routes import chapter_bp
from src.domains.curriculum.routes.v1.lesson_routes import lesson_bp
from src.domains.curriculum.routes.v1.subject_routes import subject_bp
from src.domains.library.routes.v1.document_routes import document_bp


def register_routes(app: Flask) -> None:
    """Enregistre tous les blueprints de domaine sur l'application Flask."""

    @app.get("/api/v1/health")
    def health_check() -> tuple[object, int]:
        """Expose a lightweight unauthenticated liveness check."""
        return jsonify({"status": "ok"}), 200

    app.register_blueprint(subject_bp)
    app.register_blueprint(chapter_bp)
    app.register_blueprint(lesson_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(permission_bp)
