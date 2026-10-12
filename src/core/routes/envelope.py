"""Enveloppe de réponse standardisée.

Toute réponse HTTP passe par ``ok()`` ou ``fail()`` — jamais de dict brut.
"""

from __future__ import annotations

from typing import Any

from flask import jsonify
from flask.wrappers import Response

from src.core.errors import AppError


def ok(
    data: Any = None,
    *,
    meta: dict[str, Any] | None = None,
    status: int = 200,
) -> tuple[Response, int]:
    """Construit une réponse de succès."""
    body: dict[str, Any] = {"success": True, "data": data}
    if meta:
        body["meta"] = meta
    return jsonify(body), status


def fail(error: AppError) -> tuple[Response, int]:
    """Construit une réponse d'erreur à partir d'une ``AppError``."""
    body: dict[str, Any] = {
        "success": False,
        "error": error.to_dict(),
    }
    return jsonify(body), error.status
