"""Exceptions du domaine library."""

from src.core.errors import ConflictError, NotFoundError, ValidationError


class DocumentNotFoundError(NotFoundError):
    """Levée quand le document n'existe pas."""

    code = "LIBRARY_DOCUMENT_NOT_FOUND"


class DocumentUploadError(ValidationError):
    """Levée quand un document fourni est invalide."""

    code = "LIBRARY_DOCUMENT_UPLOAD_INVALID"


class DocumentConflictError(ConflictError):
    """Levée en cas de conflit avec un document existant."""

    code = "LIBRARY_DOCUMENT_CONFLICT"
