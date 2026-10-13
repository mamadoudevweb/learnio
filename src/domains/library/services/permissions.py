"""Library domain permissions definition."""

from __future__ import annotations

LIBRARY_PERMISSIONS: list[dict[str, str]] = [
    {"domain": "library", "resource": "document", "action": "create"},
    {"domain": "library", "resource": "document", "action": "read"},
    {"domain": "library", "resource": "document", "action": "update"},
    {"domain": "library", "resource": "document", "action": "delete"},
]
