"""Exceptions for the account domain and its subdomains."""

from src.core.errors import AppError, NotFoundError
from src.domains.account.auth.exceptions import (
    CredentialNotFoundError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    ResetTokenExpiredOrInvalidError,
    SessionExpiredError,
    SessionNotFoundError,
)
from src.domains.account.rbac.exceptions import (
    PermissionAlreadyExistsError,
    PermissionNotFoundError,
    RoleAlreadyExistsError,
    RoleNotFoundError,
)


class AccountNotFoundError(NotFoundError):
    """Compte introuvable (404)."""

    code = "ACCOUNT_NOT_FOUND"


class AccountInactiveError(AppError):
    """Compte inactif ou désactivé (403)."""

    code = "ACCOUNT_INACTIVE"
    status = 403


__all__ = [
    "AccountInactiveError",
    "AccountNotFoundError",
    "CredentialNotFoundError",
    "EmailAlreadyExistsError",
    "InvalidCredentialsError",
    "PermissionAlreadyExistsError",
    "PermissionNotFoundError",
    "ResetTokenExpiredOrInvalidError",
    "RoleAlreadyExistsError",
    "RoleNotFoundError",
    "SessionExpiredError",
    "SessionNotFoundError",
]
