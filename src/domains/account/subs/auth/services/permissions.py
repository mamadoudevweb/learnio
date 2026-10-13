"""Auth subdomain permissions definition."""

from __future__ import annotations

AUTH_PERMISSIONS: list[dict[str, str]] = [
    {"domain": "account", "resource": "session", "action": "create"},
    {"domain": "account", "resource": "session", "action": "read"},
    {"domain": "account", "resource": "session", "action": "delete"},
]
