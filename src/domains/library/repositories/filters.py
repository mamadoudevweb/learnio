from dataclasses import dataclass
from uuid import UUID

from src.core.repositories.filters import EntityFilter
from src.domains.library.entities.enums import DocumentSource, DocumentType


@dataclass(kw_only=True)
class DocumentFilter(EntityFilter):
    """Filtre pour la recherche et la pagination des documents."""

    subject_id: UUID | None = None
    chapter_id: UUID | None = None
    document_type: DocumentType | None = None
    source: DocumentSource | None = None
    year: int | None = None
    search: str | None = None
