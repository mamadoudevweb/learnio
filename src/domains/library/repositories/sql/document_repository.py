from typing import Any

from sqlalchemy import or_

from src.core.repositories.base_sql import BaseSqlRepository
from src.domains.library.entities.document import Document
from src.domains.library.repositories.filters import DocumentFilter
from src.domains.library.repositories.sql import mappers
from src.domains.library.repositories.sql.orms import DocumentOrm


class DocumentRepository(BaseSqlRepository[Document, DocumentFilter]):
    """Dépôt SQL pour les documents de la bibliothèque."""

    model = DocumentOrm
    mapper = mappers.DocumentMapper
    filter_cls = DocumentFilter

    def _apply_filter(self, query: Any, filter: DocumentFilter) -> Any:
        if filter.subject_id is not None:
            query = query.where(self.model.subject_id == filter.subject_id)
        if filter.chapter_id is not None:
            query = query.where(self.model.chapter_id == filter.chapter_id)
        if filter.document_type is not None:
            query = query.where(self.model.document_type == filter.document_type.value)
        if filter.source is not None:
            query = query.where(self.model.source == filter.source.value)
        if filter.year is not None:
            query = query.where(self.model.year == filter.year)
        if filter.search is not None and filter.search.strip():
            term = f"%{filter.search.strip()}%"
            query = query.where(
                or_(
                    self.model.title.ilike(term),
                    self.model.file_name.ilike(term),
                )
            )
        return query
