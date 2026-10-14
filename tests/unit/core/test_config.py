import pytest
from pydantic import ValidationError

from src.core.config import (
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
    load_config,
)

TestingConfig.__test__ = False


def test_development_config_defaults():
    config = load_config("development")
    assert isinstance(config, DevelopmentConfig)
    assert config.DEBUG is True
    assert config.EMAIL_BACKEND == "console"
    assert config.EMAIL_FROM == "noreply@learnio.app"
    assert config.SMTP_HOST == "localhost"
    assert config.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES == 15

    flask_cfg = config.to_flask_config()
    assert flask_cfg["DEBUG"] is True
    assert flask_cfg["EMAIL_BACKEND"] == "console"
    assert flask_cfg["SMTP_HOST"] == "localhost"
    assert flask_cfg["SMTP_PORT"] == 587
    assert flask_cfg["EMAIL_FROM"] == "noreply@learnio.app"
    assert flask_cfg["PASSWORD_RESET_TOKEN_EXPIRE_MINUTES"] == 15
    assert "SECRET_KEY" in flask_cfg
    assert "JWT_SECRET_KEY" in flask_cfg


def test_testing_config_defaults():
    config = load_config("testing")
    assert isinstance(config, TestingConfig)
    assert config.DEBUG is True
    assert config.DATABASE_URL == "sqlite:///:memory:"
    assert config.EMAIL_BACKEND == "memory"
    assert config.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES == 15

    flask_cfg = config.to_flask_config()
    assert flask_cfg["EMAIL_BACKEND"] == "memory"
    assert flask_cfg["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"


def test_production_config_missing_required_fields():
    with pytest.raises(ValidationError):
        # Missing SECRET_KEY, JWT_SECRET_KEY, DATABASE_URL
        ProductionConfig()


def test_production_config_identical_secrets_raises_error():
    secret = "a" * 32
    with pytest.raises(
        ValueError, match="SECRET_KEY et JWT_SECRET_KEY doivent être distincts"
    ):
        ProductionConfig(
            SECRET_KEY=secret,
            JWT_SECRET_KEY=secret,
            DATABASE_URL="postgresql://user:pass@localhost:5432/learnio",
            EMAIL_BACKEND="console",
        )


def test_production_config_smtp_missing_host_raises_error():
    with pytest.raises(
        ValueError, match="Les variables SMTP suivantes sont requises en production"
    ):
        ProductionConfig(
            SECRET_KEY="s" * 32,
            JWT_SECRET_KEY="j" * 32,
            DATABASE_URL="postgresql://user:pass@localhost:5432/learnio",
            EMAIL_BACKEND="smtp",
            SMTP_HOST="",
            SMTP_USER="user",
            SMTP_PASSWORD="password",
        )


def test_production_config_smtp_valid():
    config = ProductionConfig(
        SECRET_KEY="s" * 32,
        JWT_SECRET_KEY="j" * 32,
        DATABASE_URL="postgresql://user:pass@localhost:5432/learnio",
        EMAIL_BACKEND="smtp",
        SMTP_HOST="smtp.example.com",
        SMTP_PORT=465,
        SMTP_USER="user@example.com",
        SMTP_PASSWORD="secretpassword",
        SMTP_USE_SSL=True,
    )
    assert config.EMAIL_BACKEND == "smtp"
    assert config.SMTP_HOST == "smtp.example.com"
    assert config.SMTP_USER == "user@example.com"
    assert config.SMTP_PASSWORD == "secretpassword"
    assert config.SMTP_USE_SSL is True

    flask_cfg = config.to_flask_config()
    assert flask_cfg["SMTP_HOST"] == "smtp.example.com"
    assert flask_cfg["EMAIL_BACKEND"] == "smtp"
