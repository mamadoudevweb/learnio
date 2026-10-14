"""Module de base pour le Builder Pattern.

Fournit la classe abstraite ``BaseBuilder`` avec journalisation intégrée
au système de logging de Flask.
"""

from __future__ import annotations

import logging
import sys
from abc import ABC, abstractmethod
from typing import Any

from flask import current_app, has_app_context
from flask.logging import default_handler


class BaseBuilder[T](ABC):
    """Classe de base générique pour tous les builders.

    Tous les builders du projet dérivent de cette classe pour garantir une interface
    commune et une journalisation homogène via le système de logging Flask.
    """

    @classmethod
    def get_builder_logger(cls) -> logging.Logger:
        """Retourne un logger dédié configuré avec le format et le gestionnaire Flask."""
        logger = logging.getLogger("learnio.builder")
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stderr)
            formatter = (
                default_handler.formatter
                if default_handler.formatter is not None
                else logging.Formatter(
                    "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
                )
            )
            handler.setFormatter(formatter)
            handler.setLevel(logging.INFO)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            logger.propagate = False
        return logger

    @property
    def logger(self) -> logging.Logger:
        """Retourne le logger Flask (current_app.logger) si un contexte d'application existe,

        ou le logger configuré avec le format Flask par défaut.
        """
        if has_app_context():
            app_logger = current_app.logger
            if app_logger.level == logging.NOTSET:
                app_logger.setLevel(logging.INFO)
            return app_logger
        return self.get_builder_logger()

    def _log_step(self, message: str, *args: Any) -> None:
        """Journalise une étape de configuration ou de construction via le système de logging Flask."""
        self.logger.info(message, *args)

    @abstractmethod
    def build(self) -> T:
        """Construit et retourne l'instance cible."""
        ...
