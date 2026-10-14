"""Email abstractions and in-memory outbox implementation for core infrastructure.

Core never imports from domains.
"""

from __future__ import annotations

import logging
import smtplib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class EmailMessage:
    """Représente un message email sortant."""

    to: str
    subject: str
    body: str
    html_body: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class EmailSender(ABC):
    """Classe de base abstraite pour l'envoi d'emails.

    Toutes les implémentations concrètes (InMemory, Console, SMTP)
    héritent de cette classe.
    """

    def __init__(self) -> None:
        self._outbox: list[EmailMessage] = []

    @property
    def outbox(self) -> list[EmailMessage]:
        """Retourne la liste des messages enregistrés dans la boîte d'envoi."""
        return self._outbox

    def clear(self) -> None:
        """Vide la boîte d'envoi."""
        self._outbox.clear()

    def _record(self, message: EmailMessage) -> None:
        """Enregistre le message dans la boîte d'envoi pour suivi et testabilité."""
        self._outbox.append(message)

    @abstractmethod
    def send(self, message: EmailMessage) -> None:
        """Envoie un message email."""
        ...


BaseEmailSender = EmailSender


class ConsoleEmailSender(EmailSender):
    """Expéditeur affichant les emails dans la console ou les logs."""

    def send(self, message: EmailMessage) -> None:
        """Affiche le message dans les logs."""
        logger.info(
            "Envoi d'un email à %s (Sujet : %s) :\n%s",
            message.to,
            message.subject,
            message.body,
        )
        self._record(message)


class SmtpEmailSender(EmailSender):
    """Expéditeur d'emails via le protocole SMTP."""

    def __init__(
        self,
        *,
        host: str = "localhost",
        port: int = 587,
        user: str = "",
        password: str = "",
        use_tls: bool = True,
        use_ssl: bool = False,
        from_email: str = "noreply@learnio.app",
        timeout: float = 10.0,
    ) -> None:
        super().__init__()
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._use_tls = use_tls
        self._use_ssl = use_ssl
        self._from_email = from_email
        self._timeout = timeout

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def from_email(self) -> str:
        return self._from_email

    def send(self, message: EmailMessage) -> None:
        """Envoie le message email via le serveur SMTP configuré."""
        self._record(message)
        msg = MIMEMultipart("alternative")
        msg["Subject"] = message.subject
        msg["From"] = self._from_email
        msg["To"] = message.to

        part_text = MIMEText(message.body, "plain", "utf-8")
        msg.attach(part_text)

        if message.html_body:
            part_html = MIMEText(message.html_body, "html", "utf-8")
            msg.attach(part_html)

        if self._use_ssl:
            with smtplib.SMTP_SSL(
                self._host, self._port, timeout=self._timeout
            ) as server:
                if self._user and self._password:
                    server.login(self._user, self._password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(
                self._host, self._port, timeout=self._timeout
            ) as server:
                if self._use_tls:
                    server.starttls()
                if self._user and self._password:
                    server.login(self._user, self._password)
                server.send_message(msg)

        logger.info(
            "Email envoyé via SMTP à %s (Sujet: %s)",
            message.to,
            message.subject,
        )


def create_email_sender(
    backend: str = "console",
    *,
    from_email: str = "noreply@learnio.app",
    smtp_host: str = "localhost",
    smtp_port: int = 587,
    smtp_user: str = "",
    smtp_password: str = "",
    smtp_use_tls: bool = True,
    smtp_use_ssl: bool = False,
    timeout: float = 10.0,
) -> EmailSender:
    """Instancie un expéditeur d'emails selon le backend demandé."""
    backend_key = backend.lower().strip()
    if backend_key == "console":
        return ConsoleEmailSender()
    if backend_key == "smtp":
        return SmtpEmailSender(
            host=smtp_host,
            port=smtp_port,
            user=smtp_user,
            password=smtp_password,
            use_tls=smtp_use_tls,
            use_ssl=smtp_use_ssl,
            from_email=from_email,
            timeout=timeout,
        )
    raise ValueError(f"Backend email inconnu : '{backend}'")


class EmailService:
    """Service d'envoi d'emails utilisant des templates Jinja."""

    def __init__(
        self,
        sender: EmailSender,
        templates_dir: Path | str | None = None,
    ) -> None:
        self._sender = sender
        if templates_dir is None:
            self._templates_dir = (
                Path(__file__).resolve().parent / "templates" / "emails"
            )
        else:
            self._templates_dir = Path(templates_dir)

        self._jinja_env = Environment(
            loader=FileSystemLoader(self._templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )

    @property
    def sender(self) -> EmailSender:
        """Expéditeur d'emails sous-jacent."""
        return self._sender

    @property
    def templates_dir(self) -> Path:
        """Dossier racine des templates Jinja."""
        return self._templates_dir

    def render_template(self, template_name: str, **context: Any) -> str:
        """Rend un template Jinja avec le contexte fourni."""
        template = self._jinja_env.get_template(template_name)
        return template.render(**context)

    def send_email(
        self,
        to: str,
        subject: str,
        html_body: str,
        text_body: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Envoie un email avec corps HTML et texte brut."""
        message = EmailMessage(
            to=to,
            subject=subject,
            body=text_body or html_body,
            html_body=html_body,
            metadata=metadata or {},
        )
        self._sender.send(message)

    def send_password_reset_email(
        self,
        to: str,
        token: str,
    ) -> None:
        """Rend le template Jinja et envoie l'email contenant le code à usage unique."""
        html_content = self.render_template(
            "password_reset.html",
            email=to,
            token=token,
        )
        text_content = self.render_template(
            "password_reset.txt",
            email=to,
            token=token,
        )

        message = EmailMessage(
            to=to,
            subject="Votre code de réinitialisation de mot de passe",
            body=text_content,
            html_body=html_content,
            metadata={"token": token},
        )
        self._sender.send(message)
