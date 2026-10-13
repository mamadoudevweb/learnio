"""Security and actor resolution infrastructure."""

from __future__ import annotations

from flask_jwt_extended import get_jwt, get_jwt_identity


class JwtActor:
    """Actor resolved from JWT identity and claims, satisfying SupportsPermissionCheck."""

    def __init__(
        self, user_id: str | None = None, permissions: set[str] | None = None
    ) -> None:
        self.user_id = str(user_id) if user_id is not None else "anonymous"
        self.permissions = permissions or {"*"}

    def has_permission(self, permission: str) -> bool:
        return "*" in self.permissions or permission in self.permissions


def get_current_actor() -> JwtActor:
    """Resolve the current authenticated actor from Flask-JWT-Extended context."""
    try:
        claims = get_jwt()
        perms = set(claims.get("permissions", [])) if "permissions" in claims else None
    except (RuntimeError, ValueError, KeyError):
        perms = None
    return JwtActor(get_jwt_identity(), permissions=perms)


__all__ = ["JwtActor", "get_current_actor"]
