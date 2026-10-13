"""Curriculum domain permissions definition."""

from __future__ import annotations

CURRICULUM_PERMISSIONS: list[dict[str, str]] = [
    {"domain": "curriculum", "resource": "subject", "action": "create"},
    {"domain": "curriculum", "resource": "subject", "action": "read"},
    {"domain": "curriculum", "resource": "subject", "action": "update"},
    {"domain": "curriculum", "resource": "subject", "action": "delete"},
    {"domain": "curriculum", "resource": "chapter", "action": "create"},
    {"domain": "curriculum", "resource": "chapter", "action": "read"},
    {"domain": "curriculum", "resource": "chapter", "action": "update"},
    {"domain": "curriculum", "resource": "chapter", "action": "delete"},
    {"domain": "curriculum", "resource": "lesson", "action": "create"},
    {"domain": "curriculum", "resource": "lesson", "action": "read"},
    {"domain": "curriculum", "resource": "lesson", "action": "update"},
    {"domain": "curriculum", "resource": "lesson", "action": "delete"},
]
