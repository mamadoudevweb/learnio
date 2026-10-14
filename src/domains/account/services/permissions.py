"""Account domain permissions definition."""

from __future__ import annotations

ACCOUNT_PERMISSIONS: list[dict[str, str]] = [
    {"domain": "account", "resource": "account", "action": "create"},
    {"domain": "account", "resource": "account", "action": "read"},
    {"domain": "account", "resource": "account", "action": "update"},
    {"domain": "account", "resource": "account", "action": "delete"},
]

ACCOUNT_DEFAULT_PERMISSIONS = ACCOUNT_PERMISSIONS
