from dataclasses import dataclass

from src.domains.library.services.document_service import DocumentService


@dataclass
class LibraryDomainService:
    """Service agrégateur pour le domaine library."""

    document_service: DocumentService
