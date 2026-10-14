"""Fabrique d'application Flask."""

from __future__ import annotations

from flask import Flask

from src.app.builder import AppBuilder
from src.core.email import EmailSender


def create_app(
    env: str | None = None,
    email_sender: EmailSender | None = None,
) -> Flask:
    """Crée et configure l'application Flask via AppBuilder."""
    return AppBuilder().with_environment(env).with_email_sender(email_sender).build()


__all__ = ["AppBuilder", "create_app"]
