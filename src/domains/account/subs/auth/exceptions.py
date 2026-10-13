"""Exceptions for the auth subdomain of account."""

from src.core.errors import AppError, ConflictError, NotFoundError, ValidationError


class InvalidCredentialsError(AppError):
    """Identifiants de connexion erronés (401)."""

    code = "AUTH_INVALID_CREDENTIALS"
    status = 401


class EmailAlreadyExistsError(ConflictError):
    """Email déjà utilisé lors de l'enregistrement (409)."""

    code = "AUTH_EMAIL_ALREADY_EXISTS"


class ResetTokenExpiredOrInvalidError(ValidationError):
    """Jeton de réinitialisation invalide ou expiré (422)."""

    code = "AUTH_RESET_TOKEN_EXPIRED_OR_INVALID"


class SessionExpiredError(AppError):
    """Session expirée (401)."""

    code = "AUTH_SESSION_EXPIRED"
    status = 401


class SessionNotFoundError(NotFoundError):
    """Session introuvable (404)."""

    code = "AUTH_SESSION_NOT_FOUND"


class CredentialNotFoundError(NotFoundError):
    """Identifiant introuvable (404)."""

    code = "AUTH_CREDENTIAL_NOT_FOUND"
