"""Account domain permissions."""

from __future__ import annotations

from src.domains.account.services.permissions import (
    ACCOUNT_DEFAULT_PERMISSIONS,
    ACCOUNT_PERMISSIONS,
)

PERMISSIONS = ACCOUNT_PERMISSIONS

__all__ = ["ACCOUNT_DEFAULT_PERMISSIONS", "ACCOUNT_PERMISSIONS", "PERMISSIONS"]
