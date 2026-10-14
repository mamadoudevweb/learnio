"""Gestionnaires d'événements pour le domaine account.

Réagit aux événements de domaine (par exemple PasswordResetRequested pour l'envoi d'email).
"""

from __future__ import annotations

import logging

from src.core.email import EmailService
from src.core.unit_of_work.sql_uow import subscribe
from src.domains.account.subs.auth.entities.events import PasswordResetRequested

logger = logging.getLogger(__name__)


def handle_password_reset_requested(
    event: PasswordResetRequested,
    email_service: EmailService,
) -> None:
    """Réagit à PasswordResetRequested en envoyant l'email de réinitialisation HTML."""
    if not event.token:
        logger.warning(
            "Événement PasswordResetRequested reçu sans jeton pour %s", event.email
        )
        return

    logger.info(
        "Envoi d'un email de réinitialisation à %s via EmailService", event.email
    )
    email_service.send_password_reset_email(to=event.email, token=event.token)


def register_account_event_handlers(email_service: EmailService) -> None:
    """Enregistre les écouteurs d'événements du domaine account."""
    subscribe(
        PasswordResetRequested,
        lambda event: handle_password_reset_requested(event, email_service),
    )
