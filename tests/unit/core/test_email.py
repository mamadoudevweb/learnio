import logging
from unittest.mock import MagicMock, patch

import pytest

from src.core.email import (
    ConsoleEmailSender,
    EmailMessage,
    EmailService,
    InMemoryEmailSender,
    SmtpEmailSender,
    create_email_sender,
)


def test_in_memory_email_sender():
    sender = InMemoryEmailSender()
    assert len(sender.outbox) == 0

    msg = EmailMessage(
        to="user@example.com",
        subject="Test Subject",
        body="Test Body",
        html_body="<p>Test Body</p>",
    )
    sender.send(msg)

    assert len(sender.outbox) == 1
    assert sender.outbox[0].to == "user@example.com"
    assert sender.outbox[0].subject == "Test Subject"
    assert sender.outbox[0].body == "Test Body"
    assert sender.outbox[0].html_body == "<p>Test Body</p>"

    sender.clear()
    assert len(sender.outbox) == 0


def test_console_email_sender(caplog):
    caplog.set_level(logging.INFO)
    sender = ConsoleEmailSender()
    msg = EmailMessage(
        to="user@example.com",
        subject="Console Test",
        body="Hello Console",
    )
    sender.send(msg)
    assert any("Console Test" in record.message for record in caplog.records)


def test_smtp_email_sender_tls():
    sender = SmtpEmailSender(
        host="smtp.test.com",
        port=587,
        user="testuser",
        password="testpassword",
        use_tls=True,
        use_ssl=False,
        from_email="noreply@test.com",
    )
    msg = EmailMessage(
        to="recipient@example.com",
        subject="SMTP TLS Test",
        body="Body Text",
        html_body="<p>HTML Text</p>",
    )

    with patch("smtplib.SMTP") as mock_smtp_cls:
        mock_server = MagicMock()
        mock_smtp_cls.return_value.__enter__.return_value = mock_server

        sender.send(msg)

        mock_smtp_cls.assert_called_once_with("smtp.test.com", 587, timeout=10.0)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("testuser", "testpassword")
        mock_server.send_message.assert_called_once()
        sent_mime = mock_server.send_message.call_args[0][0]
        assert sent_mime["To"] == "recipient@example.com"
        assert sent_mime["From"] == "noreply@test.com"
        assert sent_mime["Subject"] == "SMTP TLS Test"


def test_smtp_email_sender_ssl():
    sender = SmtpEmailSender(
        host="smtp.test.com",
        port=465,
        user="testuser",
        password="testpassword",
        use_tls=False,
        use_ssl=True,
        from_email="noreply@test.com",
    )
    msg = EmailMessage(
        to="recipient@example.com",
        subject="SMTP SSL Test",
        body="Body Text",
    )

    with patch("smtplib.SMTP_SSL") as mock_smtp_ssl_cls:
        mock_server = MagicMock()
        mock_smtp_ssl_cls.return_value.__enter__.return_value = mock_server

        sender.send(msg)

        mock_smtp_ssl_cls.assert_called_once_with("smtp.test.com", 465, timeout=10.0)
        mock_server.login.assert_called_once_with("testuser", "testpassword")
        mock_server.send_message.assert_called_once()


def test_create_email_sender_factory():
    memory = create_email_sender("memory")
    assert isinstance(memory, InMemoryEmailSender)

    in_memory = create_email_sender("in_memory")
    assert isinstance(in_memory, InMemoryEmailSender)

    console = create_email_sender("console")
    assert isinstance(console, ConsoleEmailSender)

    smtp = create_email_sender(
        "smtp",
        smtp_host="mail.example.com",
        smtp_port=25,
        from_email="custom@example.com",
    )
    assert isinstance(smtp, SmtpEmailSender)
    assert smtp.host == "mail.example.com"
    assert smtp.port == 25
    assert smtp.from_email == "custom@example.com"

    with pytest.raises(ValueError, match="Backend email inconnu"):
        create_email_sender("unknown_backend")


def test_email_service_password_reset_rendering():
    sender = InMemoryEmailSender()
    service = EmailService(sender=sender)

    service.send_password_reset_email(to="student@learnio.app", token="SECRET-1234")

    assert len(sender.outbox) == 1
    sent = sender.outbox[0]
    assert sent.to == "student@learnio.app"
    assert "SECRET-1234" in sent.body
    assert sent.html_body is not None
    assert "SECRET-1234" in sent.html_body
    assert "<!DOCTYPE html>" in sent.html_body
    assert sent.metadata["token"] == "SECRET-1234"
