"""Configuration de l'application via pydantic-settings.

Chaque environnement (dev, test, prod) a sa propre sous-classe.
``to_flask_config()`` est la source de vérité unique pour ``app.config``.
"""

from __future__ import annotations

from typing import Any, Self

from pydantic import model_validator
from pydantic_settings import BaseSettings


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

    model_config = {"env_prefix": "LEARNIO_", "env_file": ".env"}

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


def load_config(env: str = "development") -> BaseConfig:
    """Charge la configuration correspondant à l'environnement demandé."""
    cls = CONFIGS.get(env, DevelopmentConfig)
    return cls()
