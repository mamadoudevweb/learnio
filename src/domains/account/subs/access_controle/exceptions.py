"""Exceptions for the rbac subdomain of account."""

from src.core.errors import ConflictError, NotFoundError


class RoleNotFoundError(NotFoundError):
    """Rôle introuvable (404)."""

    code = "RBAC_ROLE_NOT_FOUND"


class RoleAlreadyExistsError(ConflictError):
    """Rôle déjà existant (409)."""

    code = "RBAC_ROLE_ALREADY_EXISTS"


class PermissionNotFoundError(NotFoundError):
    """Permission introuvable (404)."""

    code = "RBAC_PERMISSION_NOT_FOUND"


class PermissionAlreadyExistsError(ConflictError):
    """Permission déjà existante (409)."""

    code = "RBAC_PERMISSION_ALREADY_EXISTS"
