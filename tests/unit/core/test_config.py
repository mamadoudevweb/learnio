import pytest
from pydantic import ValidationError

from src.core.config import (
    ConfigBuilder,
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


def test_production_config_gmail_autodetect():
    config = ProductionConfig(
        SECRET_KEY="s" * 32,
        JWT_SECRET_KEY="j" * 32,
        DATABASE_URL="postgresql://user:pass@localhost:5432/learnio",
        EMAIL_BACKEND="smtp",
        SMTP_USER="dev@gmail.com",
        SMTP_PASSWORD="secretpassword",
    )
    assert config.SMTP_HOST == "smtp.gmail.com"


def test_production_config_from_env_without_prefix(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "s" * 32)
    monkeypatch.setenv("JWT_SECRET_KEY", "j" * 32)
    monkeypatch.setenv("DATABASE_URL", "postgresql://db.render.com:5432/learnio")
    monkeypatch.setenv("SMTP_USER", "user@gmail.com")
    monkeypatch.setenv("SMTP_PASSWORD", "app_password_here")

    config = ProductionConfig()
    assert config.SECRET_KEY == "s" * 32
    assert config.JWT_SECRET_KEY == "j" * 32
    assert config.DATABASE_URL == "postgresql://db.render.com:5432/learnio"
    assert config.SMTP_HOST == "smtp.gmail.com"
    assert config.SMTP_USER == "user@gmail.com"


def test_config_builder_development():
    config = (
        ConfigBuilder("development")
        .with_debug(False)
        .with_database_url("sqlite:///custom.db")
        .with_rate_limit("500 per hour")
        .with_token_expiry(30)
        .with_upload_dir("custom_uploads", max_size_mb=50)
        .build()
    )
    assert isinstance(config, DevelopmentConfig)
    assert config.DEBUG is False
    assert config.DATABASE_URL == "sqlite:///custom.db"
    assert config.RATELIMIT_DEFAULT == "500 per hour"
    assert config.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES == 30
    assert config.UPLOAD_DIR == "custom_uploads"
    assert config.MAX_FILE_SIZE_MB == 50


def test_config_builder_production():
    config = (
        ConfigBuilder("production")
        .with_secret_key("s" * 32)
        .with_jwt_secret_key("j" * 32)
        .with_database_url("postgresql://user:pass@localhost:5432/learnio")
        .with_email(
            backend="smtp",
            from_email="admin@learnio.app",
            smtp_host="smtp.learnio.app",
            smtp_port=587,
            smtp_user="admin",
            smtp_password="password",
            smtp_use_tls=True,
        )
        .build()
    )
    assert isinstance(config, ProductionConfig)
    assert config.SECRET_KEY == "s" * 32
    assert config.JWT_SECRET_KEY == "j" * 32
    assert config.EMAIL_BACKEND == "smtp"
    assert config.SMTP_HOST == "smtp.learnio.app"


def test_config_builder_from_mapping_and_overrides():
    builder = ConfigBuilder("testing").from_mapping({"UPLOAD_DIR": "test_uploads"})
    builder.with_override("DEBUG", False)
    builder.with_environment("development")
    config = builder.build()
    assert isinstance(config, DevelopmentConfig)
    assert config.UPLOAD_DIR == "test_uploads"
    assert config.DEBUG is False
