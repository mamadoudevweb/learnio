"""Access control subdomain permissions definition."""

from __future__ import annotations

ACCESS_CONTROL_PERMISSIONS: list[dict[str, str]] = [
    {"domain": "account", "resource": "role", "action": "create"},
    {"domain": "account", "resource": "role", "action": "read"},
    {"domain": "account", "resource": "role", "action": "update"},
    {"domain": "account", "resource": "role", "action": "delete"},
    {"domain": "account", "resource": "permission", "action": "create"},
    {"domain": "account", "resource": "permission", "action": "read"},
    {"domain": "account", "resource": "permission", "action": "delete"},
]
