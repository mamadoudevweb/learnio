"""Configuration de l'application via pydantic-settings.

Chaque environnement (dev, test, prod) a sa propre sous-classe.
``to_flask_config()`` est la source de vérité unique pour ``app.config``.
"""

from __future__ import annotations

from typing import Any, Self

from pydantic import model_validator
from pydantic_settings import BaseSettings

from src.core.builder import BaseBuilder


class BaseConfig(BaseSettings):
    """Configuration de base, commune à tous les environnements."""

    # --- Application ---
    APP_NAME: str = "learnio"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me-in-production-at-least-32-chars-long"
    JWT_SECRET_KEY: str = "change-me-too-in-production-at-least-32-chars-long"

    # --- Base de données ---
    DATABASE_URL: str = "sqlite:///learnio.db"

    # --- Limitation de débit ---
    RATELIMIT_DEFAULT: str = "200 per hour"

    # --- Stockage fichiers ---
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 25

    # --- Email & Notifications ---
    EMAIL_BACKEND: str = "console"
    EMAIL_FROM: str = "noreply@learnio.app"
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_USE_TLS: bool = True
    SMTP_USE_SSL: bool = False

    # --- Sécurité & Tokens ---
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES: int = 15

    model_config = {
        "env_prefix": "LEARNIO_",
        "env_file": ".env",
        "extra": "ignore",
    }

    def to_flask_config(self) -> dict[str, Any]:
        """Convertit la configuration en dictionnaire Flask."""
        return {
            "DEBUG": self.DEBUG,
            "SECRET_KEY": self.SECRET_KEY,
            "JWT_SECRET_KEY": self.JWT_SECRET_KEY,
            "SQLALCHEMY_DATABASE_URI": self.DATABASE_URL,
            "RATELIMIT_DEFAULT": self.RATELIMIT_DEFAULT,
            "MAX_CONTENT_LENGTH": self.MAX_FILE_SIZE_MB * 1024 * 1024,
            "UPLOAD_DIR": self.UPLOAD_DIR,
            "EMAIL_BACKEND": self.EMAIL_BACKEND,
            "EMAIL_FROM": self.EMAIL_FROM,
            "SMTP_HOST": self.SMTP_HOST,
            "SMTP_PORT": self.SMTP_PORT,
            "SMTP_USER": self.SMTP_USER,
            "SMTP_PASSWORD": self.SMTP_PASSWORD,
            "SMTP_USE_TLS": self.SMTP_USE_TLS,
            "SMTP_USE_SSL": self.SMTP_USE_SSL,
            "PASSWORD_RESET_TOKEN_EXPIRE_MINUTES": self.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES,
        }


class DevelopmentConfig(BaseConfig):
    """Configuration pour le développement local."""

    DEBUG: bool = True
    EMAIL_BACKEND: str = "console"


class TestingConfig(BaseConfig):
    """Configuration pour les tests."""

    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///:memory:"
    SECRET_KEY: str = "test-secret-key-at-least-32-chars-long"
    JWT_SECRET_KEY: str = "test-jwt-secret-key-at-least-32-chars-long"
    EMAIL_BACKEND: str = "memory"


class ProductionConfig(BaseConfig):
    """Configuration de production.

    Les champs sensibles n'ont pas de valeur par défaut :
    l'application échoue au démarrage si les variables
    d'environnement sont manquantes.
    """

    SECRET_KEY: str  # type: ignore[assignment]
    JWT_SECRET_KEY: str  # type: ignore[assignment]
    DATABASE_URL: str  # type: ignore[assignment]
    EMAIL_BACKEND: str = "smtp"
    SMTP_HOST: str = ""
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    @model_validator(mode="after")
    def validate_production_settings(self) -> Self:
        if self.SECRET_KEY == self.JWT_SECRET_KEY:
            raise ValueError("SECRET_KEY et JWT_SECRET_KEY doivent être distincts.")
        if self.EMAIL_BACKEND == "smtp":
            missing = []
            if not self.SMTP_HOST:
                missing.append("SMTP_HOST")
            if not self.SMTP_USER:
                missing.append("SMTP_USER")
            if not self.SMTP_PASSWORD:
                missing.append("SMTP_PASSWORD")
            if missing:
                raise ValueError(
                    f"Les variables SMTP suivantes sont requises en production : {', '.join(missing)}"
                )
        return self


CONFIGS: dict[str, type[BaseConfig]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


class ConfigBuilder(BaseBuilder[BaseConfig]):
    """Builder fluide pour construire la configuration de l'application."""

    def __init__(self, env: str = "development") -> None:
        self._env = env
        self._overrides: dict[str, Any] = {}
        self._log_step("ConfigBuilder initialisé pour l'environnement '%s'", env)

    def with_environment(self, env: str) -> Self:
        """Définit l'environnement cible (development, testing, production)."""
        self._env = env
        self._log_step("Environnement configuré : %s", env)
        return self

    def with_debug(self, debug: bool) -> Self:
        """Active ou désactive le mode debug."""
        self._overrides["DEBUG"] = debug
        self._log_step("DEBUG configuré : %s", debug)
        return self

    def with_secret_key(self, secret_key: str) -> Self:
        """Définit la clé secrète Flask."""
        self._overrides["SECRET_KEY"] = secret_key
        self._log_step("SECRET_KEY configuré")
        return self

    def with_jwt_secret_key(self, jwt_secret_key: str) -> Self:
        """Définit la clé secrète JWT."""
        self._overrides["JWT_SECRET_KEY"] = jwt_secret_key
        self._log_step("JWT_SECRET_KEY configuré")
        return self

    def with_database_url(self, database_url: str) -> Self:
        """Définit l'URL de connexion à la base de données."""
        self._overrides["DATABASE_URL"] = database_url
        self._log_step("DATABASE_URL configuré : %s", database_url)
        return self

    def with_rate_limit(self, limit: str) -> Self:
        """Définit la limite de débit par défaut."""
        self._overrides["RATELIMIT_DEFAULT"] = limit
        self._log_step("RATELIMIT_DEFAULT configuré : %s", limit)
        return self

    def with_upload_dir(self, upload_dir: str, max_size_mb: int | None = None) -> Self:
        """Définit le répertoire d'upload et éventuellement la taille maximale en Mo."""
        self._overrides["UPLOAD_DIR"] = upload_dir
        if max_size_mb is not None:
            self._overrides["MAX_FILE_SIZE_MB"] = max_size_mb
        self._log_step(
            "UPLOAD_DIR configuré : %s (max_size_mb=%s)", upload_dir, max_size_mb
        )
        return self

    def with_email(
        self,
        backend: str,
        *,
        from_email: str | None = None,
        smtp_host: str | None = None,
        smtp_port: int | None = None,
        smtp_user: str | None = None,
        smtp_password: str | None = None,
        smtp_use_tls: bool | None = None,
        smtp_use_ssl: bool | None = None,
    ) -> Self:
        """Configure les paramètres d'envoi d'e-mails."""
        self._overrides["EMAIL_BACKEND"] = backend
        if from_email is not None:
            self._overrides["EMAIL_FROM"] = from_email
        if smtp_host is not None:
            self._overrides["SMTP_HOST"] = smtp_host
        if smtp_port is not None:
            self._overrides["SMTP_PORT"] = smtp_port
        if smtp_user is not None:
            self._overrides["SMTP_USER"] = smtp_user
        if smtp_password is not None:
            self._overrides["SMTP_PASSWORD"] = smtp_password
        if smtp_use_tls is not None:
            self._overrides["SMTP_USE_TLS"] = smtp_use_tls
        if smtp_use_ssl is not None:
            self._overrides["SMTP_USE_SSL"] = smtp_use_ssl
        self._log_step("Paramètres email configurés : backend=%s", backend)
        return self

    def with_token_expiry(self, minutes: int) -> Self:
        """Définit la durée d'expiration du token de réinitialisation en minutes."""
        self._overrides["PASSWORD_RESET_TOKEN_EXPIRE_MINUTES"] = minutes
        self._log_step(
            "PASSWORD_RESET_TOKEN_EXPIRE_MINUTES configuré : %s min", minutes
        )
        return self

    def with_override(self, key: str, value: Any) -> Self:
        """Surcharge une clé de configuration quelconque."""
        self._overrides[key] = value
        self._log_step("Surcharge de configuration : %s=%s", key, value)
        return self

    def from_mapping(self, mapping: dict[str, Any]) -> Self:
        """Applique un ensemble de clés / valeurs depuis un dictionnaire."""
        self._overrides.update(mapping)
        self._log_step("Mise à jour depuis un dictionnaire (%d clés)", len(mapping))
        return self

    def build(self) -> BaseConfig:
        """Construit et valide l'instance de configuration appropriée."""
        config_cls = CONFIGS.get(self._env, DevelopmentConfig)
        self._log_step(
            "Construction de la configuration %s avec %d surcharges",
            config_cls.__name__,
            len(self._overrides),
        )
        return config_cls(**self._overrides)


def load_config(env: str = "development") -> BaseConfig:
    """Charge la configuration correspondant à l'environnement demandé."""
    return ConfigBuilder(env).build()
