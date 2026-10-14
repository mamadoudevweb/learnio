"""Hiérarchie d'erreurs applicatives.

Toutes les exceptions métier héritent de ``AppError``.
Chaque sous-classe est auto-enregistrée grâce à ``__init_subclass__``.
"""

from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------
# Registre global (code → classe)
# ---------------------------------------------------------------------------
_ERROR_REGISTRY: dict[str, type[AppError]] = {}


class AppError(Exception):
    """Erreur applicative de base.

    Attributs :
        code     – identifiant machine (ex: ``PROGRAMME_MATIERE_NOT_FOUND``).
        message  – texte lisible destiné à l'utilisateur.
        details  – informations complémentaires (optionnel).
        status   – code HTTP associé (défaut 400).
    """

    code: str = "UNKNOWN_ERROR"
    status: int = 400

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if cls.code != "UNKNOWN_ERROR":
            _ERROR_REGISTRY[cls.code] = cls

    def __init__(
        self,
        message: str | None = None,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message or self.code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Sérialise l'erreur pour l'enveloppe de réponse."""
        result: dict[str, Any] = {
            "code": self.code,
            "message": self.message,
        }
        if self.details:
            result["details"] = self.details
        return result


# ---------------------------------------------------------------------------
# Sous-classes génériques (une par famille de code HTTP)
# ---------------------------------------------------------------------------


class NotFoundError(AppError):
    """Ressource introuvable (404)."""

    code = "RESOURCE_NOT_FOUND"
    status = 404


class ConflictError(AppError):
    """Conflit de données (409)."""

    code = "CONFLICT"
    status = 409


class ValidationError(AppError):
    """Données invalides (422)."""

    code = "VALIDATION_FAILED"
    status = 422


class PermissionDeniedError(AppError):
    """Accès non autorisé (403)."""

    code = "PERMISSION_DENIED"
    status = 403


class RepositoryNotFoundError(AppError):
    """Repository non enregistré dans le registre (500)."""

    code = "REPOSITORY_NOT_FOUND"
    status = 500
