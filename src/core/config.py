"""Configuration de l'application via pydantic-settings.

Chaque environnement (dev, test, prod) a sa propre sous-classe.
``to_flask_config()`` est la source de vérité unique pour ``app.config``.
"""

from __future__ import annotations

from typing import Any

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
        }


class DevelopmentConfig(BaseConfig):
    """Configuration pour le développement local."""

    DEBUG: bool = True


class TestingConfig(BaseConfig):
    """Configuration pour les tests."""

    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///:memory:"
    SECRET_KEY: str = "test-secret-key-at-least-32-chars-long"
    JWT_SECRET_KEY: str = "test-jwt-secret-key-at-least-32-chars-long"


class ProductionConfig(BaseConfig):
    """Configuration de production.

    Les champs sensibles n'ont pas de valeur par défaut :
    l'application échoue au démarrage si les variables
    d'environnement sont manquantes.
    """

    SECRET_KEY: str  # type: ignore[assignment]
    JWT_SECRET_KEY: str  # type: ignore[assignment]
    DATABASE_URL: str  # type: ignore[assignment]


CONFIGS: dict[str, type[BaseConfig]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def load_config(env: str = "development") -> BaseConfig:
    """Charge la configuration correspondant à l'environnement demandé."""
    cls = CONFIGS.get(env, DevelopmentConfig)
    return cls()
