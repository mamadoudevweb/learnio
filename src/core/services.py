"""Protocole d'autorisation et service de base."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class SupportsPermissionCheck(Protocol):
    """Protocole que tout objet « acteur » doit satisfaire."""

    def has_permission(self, permission: str) -> bool: ...


class BaseService:
    """Classe de base pour tous les services de domaine.

    Fournit :
    * ``_uow_factory`` — fabrique d'unités de travail injectée au constructeur ;
    * ``_authorize``    — vérification d'autorisation.
    """

    def __init__(self, uow_factory: Any) -> None:
        self._uow_factory = uow_factory

    # ------------------------------------------------------------------
    def _authorize(
        self,
        actor: SupportsPermissionCheck,
        domain: str,
        entity: str,
        action: str,
    ) -> None:
        """Lève ``PermissionDeniedError`` si l'acteur n'est pas autorisé."""
        permission = f"{domain}:{entity}:{action}"
        if not actor.has_permission(permission):
            from src.core.errors import PermissionDeniedError

            raise PermissionDeniedError(
                f"Permission refusée : {permission}",
                details={"required_permission": permission},
            )
