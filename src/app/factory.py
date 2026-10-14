"""Fabrique d'application Flask."""

from __future__ import annotations

import logging
import os
from functools import partial
from typing import Any

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.docs import register_docs
from src.app.domain_service_builder import build_domain_services
from src.app.permissions_seed import seed_permissions
from src.app.roles_seed import seed_admin_role
from src.app.routes import register_routes
from src.app.uow import REPOSITORY_CLASSES
from src.core.config import load_config
from src.core.database import Base
from src.core.email import EmailService, create_email_sender
from src.core.errors import AppError
from src.core.unit_of_work.sql_uow import SqlUnitOfWork, clear_subscribers
from src.domains.account.event_handlers import register_account_event_handlers

logger = logging.getLogger(__name__)


def create_app(env: str | None = None) -> Flask:
    """Crée et configure l'application Flask."""
    env = env or os.getenv("LEARNIO_ENV", "development")
    config = load_config(env)

    app = Flask(__name__)
    app.config.from_mapping(config.to_flask_config())

    JWTManager(app)

    engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)
    app.extensions["engine"] = engine
    session_factory = sessionmaker(bind=engine)

    if env in ("development", "testing"):
        Base.metadata.create_all(engine)

    uow_factory = partial(
        SqlUnitOfWork,
        session_factory=session_factory,
        repository_classes=REPOSITORY_CLASSES,
    )

    email_sender = create_email_sender(
        backend=app.config.get("EMAIL_BACKEND", "console"),
        from_email=app.config.get("EMAIL_FROM", "noreply@learnio.app"),
        smtp_host=app.config.get("SMTP_HOST", "localhost"),
        smtp_port=app.config.get("SMTP_PORT", 587),
        smtp_user=app.config.get("SMTP_USER", ""),
        smtp_password=app.config.get("SMTP_PASSWORD", ""),
        smtp_use_tls=app.config.get("SMTP_USE_TLS", True),
        smtp_use_ssl=app.config.get("SMTP_USE_SSL", False),
    )
    app.extensions["email_sender"] = email_sender
    email_service = EmailService(sender=email_sender)
    app.extensions["email_service"] = email_service

    # Enregistrement des gestionnaires d'événements
    clear_subscribers()
    register_account_event_handlers(email_service)

    domain_services = build_domain_services(
        uow_factory,
        email_sender=email_sender,
        reset_token_expire_minutes=app.config.get(
            "PASSWORD_RESET_TOKEN_EXPIRE_MINUTES", 15
        ),
    )
    # Seed default permissions and admin role before handling any requests
    seed_permissions(uow_factory)
    seed_admin_role(uow_factory)
    app.extensions["domain_service"] = domain_services

    register_routes(app)
    register_docs(app)

    @app.errorhandler(AppError)
    def handle_app_error(error: AppError) -> tuple[Any, int]:
        logger.warning("AppError [%s]: %s", error.code, error.message)
        return (
            jsonify({"success": False, "error": error.to_dict()}),
            error.status,
        )

    from pydantic import ValidationError as PydanticValidationError

    @app.errorhandler(PydanticValidationError)
    def handle_pydantic_validation_error(
        error: PydanticValidationError,
    ) -> tuple[Any, int]:
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_FAILED",
                        "message": "Erreur de validation des données.",
                        "details": error.errors(),
                    },
                }
            ),
            422,
        )

    @app.errorhandler(422)
    def handle_validation_error(error: Any) -> tuple[Any, int]:
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_FAILED",
                        "message": str(error),
                    },
                }
            ),
            422,
        )

    @app.errorhandler(500)
    def handle_server_error(error: Any) -> tuple[Any, int]:
        logger.exception("Erreur interne du serveur")
        return (
            jsonify(
                {
                    "success": False,
                    "error": {
                        "code": "SERVER_ERROR",
                        "message": "Une erreur interne est survenue.",
                    },
                }
            ),
            500,
        )

    logger.info("Application Learnio créée [env=%s]", env)
    return app
