"""Builder pour l'application Flask Learnio.

Permet une construction modulaire, fluide et hautement configurable de l'application Flask
avec journalisation intégrée de chaque étape de construction via le système de logging Flask.
"""

from __future__ import annotations

import logging
import os
from functools import partial
from typing import Any, Self

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from pydantic import ValidationError as PydanticValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.docs import register_docs
from src.app.domain_service_builder import (
    DomainServices,
    DomainServicesBuilder,
)
from src.app.permissions_seed import seed_permissions
from src.app.roles_seed import seed_admin_role
from src.app.routes import register_routes
from src.app.uow import REPOSITORY_REGISTRY
from src.core.builder import BaseBuilder
from src.core.config import BaseConfig, ConfigBuilder, load_config
from src.core.database import Base
from src.core.email import EmailSender, EmailService, create_email_sender
from src.core.errors import AppError
from src.core.unit_of_work.registry import (
    RepositoryRegistry,
    RepositoryRegistryBuilder,
)
from src.core.unit_of_work.sql_uow import SqlUnitOfWork, clear_subscribers
from src.domains.account.event_handlers import register_account_event_handlers

logger = logging.getLogger(__name__)


class AppBuilder(BaseBuilder[Flask]):
    """Builder pour construire et configurer l'application Flask Learnio."""

    def __init__(self, app_name: str = "learnio") -> None:
        self._app_name = app_name
        self._env: str = os.getenv("LEARNIO_ENV", "development")
        self._config: BaseConfig | None = None
        self._config_builder: ConfigBuilder | None = None
        self._engine: Any | None = None
        self._session_factory: Any | None = None
        self._repository_registry: (
            RepositoryRegistry | RepositoryRegistryBuilder | None
        ) = None
        self._email_sender: EmailSender | None = None
        self._domain_services: DomainServices | DomainServicesBuilder | None = None
        self._enable_jwt: bool = True
        self._enable_seeds: bool = True
        self._enable_routes: bool = True
        self._enable_docs: bool = True
        self._enable_error_handlers: bool = True
        self._enable_event_handlers: bool = True
        self._log_step("AppBuilder initialisé pour l'application '%s'", app_name)

    def with_app_name(self, name: str) -> Self:
        """Définit le nom de l'application Flask."""
        self._app_name = name
        self._log_step("Nom d'application configuré : %s", name)
        return self

    def with_environment(self, env: str | None) -> Self:
        """Définit l'environnement d'exécution (development, testing, production)."""
        if env is not None:
            self._env = env
            self._log_step("Environnement configuré : %s", env)
        return self

    def with_config(self, config: BaseConfig) -> Self:
        """Injecte directement une instance de configuration."""
        self._config = config
        self._log_step("Configuration injectée directement (%s)", type(config).__name__)
        return self

    def with_config_builder(self, builder: ConfigBuilder) -> Self:
        """Injecte un ConfigBuilder pour construire la configuration."""
        self._config_builder = builder
        self._log_step("ConfigBuilder associé à l'AppBuilder")
        return self

    def with_database(self, engine: Any, session_factory: Any | None = None) -> Self:
        """Injecte un moteur SQLAlchemy et éventuellement une fabrique de sessions."""
        self._engine = engine
        self._session_factory = session_factory or sessionmaker(bind=engine)
        self._log_step(
            "Base de données injectée (engine=%s, session_factory=%s)",
            type(engine).__name__,
            type(self._session_factory).__name__,
        )
        return self

    def with_repository_registry(
        self, registry: RepositoryRegistry | RepositoryRegistryBuilder
    ) -> Self:
        """Injecte un RepositoryRegistry ou un RepositoryRegistryBuilder."""
        self._repository_registry = registry
        self._log_step("RepositoryRegistry (ou builder) injecté")
        return self

    def with_email_sender(self, sender: EmailSender | None) -> Self:
        """Injecte un expéditeur d'e-mails personnalisé."""
        self._email_sender = sender
        self._log_step(
            "EmailSender configuré : %s",
            type(sender).__name__ if sender else None,
        )
        return self

    def with_domain_services(
        self, services: DomainServices | DomainServicesBuilder
    ) -> Self:
        """Injecte le conteneur DomainServices ou son builder."""
        self._domain_services = services
        self._log_step("DomainServices (ou builder) injecté")
        return self

    def with_jwt(self, enabled: bool = True) -> Self:
        """Active ou désactive JWTManager."""
        self._enable_jwt = enabled
        self._log_step("Support JWT configuré : %s", enabled)
        return self

    def with_seeds(self, enabled: bool = True) -> Self:
        """Active ou désactive l'initialisation des graines (permissions et rôle admin)."""
        self._enable_seeds = enabled
        self._log_step("Initialisation des graines (seeds) configurée : %s", enabled)
        return self

    def with_routes(self, enabled: bool = True) -> Self:
        """Active ou désactive l'enregistrement des routes HTTP."""
        self._enable_routes = enabled
        self._log_step("Enregistrement des routes configuré : %s", enabled)
        return self

    def with_docs(self, enabled: bool = True) -> Self:
        """Active ou désactive l'enregistrement de la documentation OpenAPI."""
        self._enable_docs = enabled
        self._log_step("Enregistrement OpenAPI configuré : %s", enabled)
        return self

    def with_error_handlers(self, enabled: bool = True) -> Self:
        """Active ou désactive les gestionnaires d'erreurs standard."""
        self._enable_error_handlers = enabled
        self._log_step("Gestionnaires d'erreurs configurés : %s", enabled)
        return self

    def with_event_handlers(self, enabled: bool = True) -> Self:
        """Active ou désactive l'enregistrement des gestionnaires d'événements de domaine."""
        self._enable_event_handlers = enabled
        self._log_step("Gestionnaires d'événements configurés : %s", enabled)
        return self

    def build(self) -> Flask:
        """Construit et configure entièrement l'application Flask."""
        self._log_step(
            "Début de construction de l'application Learnio [env=%s]",
            self._env,
        )

        # 1. Résolution de la configuration
        if self._config is not None:
            config = self._config
        elif self._config_builder is not None:
            config = self._config_builder.build()
        else:
            config = load_config(self._env)
        self._log_step("Configuration chargée (%s)", type(config).__name__)

        # 2. Création de l'application Flask
        app = Flask(self._app_name)
        app.config.from_mapping(config.to_flask_config())
        app.logger.setLevel(logging.DEBUG if app.config.get("DEBUG") else logging.INFO)
        self._log_step(
            "Application Flask '%s' instanciée avec sa configuration",
            self._app_name,
        )

        with app.app_context():
            # 3. JWT Manager
            if self._enable_jwt:
                JWTManager(app)
                self._log_step("JWTManager initialisé")

            # 4. Base de données
            engine = self._engine
            if engine is None:
                engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)
            app.extensions["engine"] = engine

            session_factory = self._session_factory
            if session_factory is None:
                session_factory = sessionmaker(bind=engine)

            if self._env in ("development", "testing"):
                Base.metadata.create_all(engine)
                self._log_step("Base.metadata.create_all exécuté")

            # 5. Registre de repositories
            if isinstance(self._repository_registry, RepositoryRegistry):
                registry = self._repository_registry
            elif isinstance(self._repository_registry, RepositoryRegistryBuilder):
                registry = self._repository_registry.build()
            else:
                registry = REPOSITORY_REGISTRY
            app.extensions["repository_registry"] = registry
            self._log_step(
                "Registre de repositories configuré avec %d repositories",
                len(registry.registered_names()),
            )

            # 6. Fabrique d'Unit of Work
            uow_factory = partial(
                SqlUnitOfWork,
                session_factory=session_factory,
                registry=registry,
            )

            # 7. Services email
            email_sender = self._email_sender
            if email_sender is None:
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
            self._log_step("EmailSender et EmailService configurés")

            # 8. Gestionnaires d'événements
            if self._enable_event_handlers:
                clear_subscribers()
                register_account_event_handlers(email_service)
                self._log_step("Gestionnaires d'événements enregistrés")

            # 9. Services de domaine
            if isinstance(self._domain_services, DomainServices):
                domain_services = self._domain_services
            elif isinstance(self._domain_services, DomainServicesBuilder):
                domain_services = self._domain_services.build()
            else:
                domain_services = (
                    DomainServicesBuilder(uow_factory)
                    .with_email_sender(email_sender)
                    .with_reset_token_expiry(
                        app.config.get("PASSWORD_RESET_TOKEN_EXPIRE_MINUTES", 15)
                    )
                    .build()
                )
            app.extensions["domain_service"] = domain_services
            self._log_step("DomainServices associés à l'application")

            # 10. Graines (Seeds)
            if self._enable_seeds:
                seed_permissions(uow_factory)
                seed_admin_role(uow_factory)
                self._log_step(
                    "Graines de permissions et rôle administrateur initialisées"
                )

            # 11. Routes HTTP
            if self._enable_routes:
                register_routes(app)
                self._log_step("Routes API enregistrées")

            # 12. Documentation OpenAPI
            if self._enable_docs:
                register_docs(app)
                self._log_step("Documentation OpenAPI enregistrée")

            # 13. Gestionnaires d'erreurs
            if self._enable_error_handlers:
                self._register_error_handlers(app)
                self._log_step("Gestionnaires d'erreurs HTTP enregistrés")

            self._log_step(
                "Application Learnio créée avec succès [env=%s]",
                self._env,
            )
        return app

    def _register_error_handlers(self, app: Flask) -> None:
        """Enregistre les gestionnaires d'erreurs standard de l'application."""

        @app.errorhandler(AppError)
        def handle_app_error(error: AppError) -> tuple[Any, int]:
            logger.warning("AppError [%s]: %s", error.code, error.message)
            return (
                jsonify({"success": False, "error": error.to_dict()}),
                error.status,
            )

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
