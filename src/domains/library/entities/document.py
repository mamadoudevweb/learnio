from uuid import UUID

from src.core.entities import BaseEntity, EntityId
from src.domains.library.entities.enums import DocumentSource, DocumentType
from src.domains.library.entities.events import DocumentCreated, DocumentUpdated


class Document(BaseEntity[EntityId]):
    """Document de la bibliothèque personnelle de révision."""

    title: str
    file_path: str
    file_name: str
    file_size_bytes: int
    mime_type: str = "application/pdf"
    subject_id: UUID | None = None
    chapter_id: UUID | None = None
    document_type: DocumentType = DocumentType.OTHER
    source: DocumentSource = DocumentSource.USER
    year: int | None = None
    extracted_text: str | None = None
    is_text_extracted: bool = False

    @classmethod
    def create(
        cls,
        *,
        title: str,
        file_path: str,
        file_name: str,
        file_size_bytes: int,
        mime_type: str = "application/pdf",
        subject_id: UUID | None = None,
        chapter_id: UUID | None = None,
        document_type: DocumentType = DocumentType.OTHER,
        source: DocumentSource = DocumentSource.USER,
        year: int | None = None,
        extracted_text: str | None = None,
        is_text_extracted: bool = False,
    ) -> Document:
        doc = cls(
            title=title,
            file_path=file_path,
            file_name=file_name,
            file_size_bytes=file_size_bytes,
            mime_type=mime_type,
            subject_id=subject_id,
            chapter_id=chapter_id,
            document_type=document_type,
            source=source,
            year=year,
            extracted_text=extracted_text,
            is_text_extracted=is_text_extracted,
        )
        doc.register_event(DocumentCreated(document_id=doc.id, title=title))
        return doc

    def update_metadata(
        self,
        *,
        title: str | None = None,
        subject_id: UUID | None = None,
        chapter_id: UUID | None = None,
        document_type: DocumentType | None = None,
        year: int | None = None,
    ) -> None:
        if title is not None:
            self.title = title
        if subject_id is not None:
            self.subject_id = subject_id
        if chapter_id is not None:
            self.chapter_id = chapter_id
        if document_type is not None:
            self.document_type = document_type
        if year is not None:
            self.year = year
        self.register_event(DocumentUpdated(document_id=self.id))

    def set_extracted_text(self, text: str) -> None:
        self.extracted_text = text
        self.is_text_extracted = True
        self.register_event(DocumentUpdated(document_id=self.id))
