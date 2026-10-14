from uuid import UUID

from src.core.entities import ServiceResult
from src.core.services import BaseService, SupportsPermissionCheck
from src.domains.library.entities.document import Document
from src.domains.library.entities.enums import DocumentSource, DocumentType
from src.domains.library.exceptions import DocumentNotFoundError
from src.domains.library.repositories.filters import DocumentFilter


class DocumentService(BaseService):
    """Service applicatif pour la gestion des documents de la bibliothèque."""

    def get_document(
        self, actor: SupportsPermissionCheck, document_id: UUID
    ) -> ServiceResult[Document]:
        self._authorize(actor, "library", "document", "read")

        with self._uow_factory() as uow:
            repo = uow.get_repository("DocumentRepository")
            document = repo.get(document_id)
            if not document:
                raise DocumentNotFoundError(f"Document {document_id} introuvable")
            return ServiceResult(data=document)

    def list_documents(
        self, actor: SupportsPermissionCheck, filter: DocumentFilter
    ) -> ServiceResult[list[Document]]:
        self._authorize(actor, "library", "document", "read")

        with self._uow_factory() as uow:
            repo = uow.get_repository("DocumentRepository")
            documents = repo.list(filter)
            count = repo.count(filter)
            return ServiceResult(data=documents, meta={"total": count})

    def create_document(
        self,
        actor: SupportsPermissionCheck,
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
    ) -> ServiceResult[Document]:
        self._authorize(actor, "library", "document", "create")

        document = Document.create(
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

        with self._uow_factory() as uow:
            repo = uow.get_repository("DocumentRepository")
            repo.add(document)
            uow.track(document)
            return ServiceResult(data=document)

    def update_document(
        self,
        actor: SupportsPermissionCheck,
        document_id: UUID,
        *,
        title: str | None = None,
        subject_id: UUID | None = None,
        chapter_id: UUID | None = None,
        document_type: DocumentType | None = None,
        year: int | None = None,
        extracted_text: str | None = None,
    ) -> ServiceResult[Document]:
        self._authorize(actor, "library", "document", "update")

        with self._uow_factory() as uow:
            repo = uow.get_repository("DocumentRepository")
            document = repo.get(document_id)
            if not document:
                raise DocumentNotFoundError(f"Document {document_id} introuvable")

            document.update_metadata(
                title=title,
                subject_id=subject_id,
                chapter_id=chapter_id,
                document_type=document_type,
                year=year,
            )
            if extracted_text is not None:
                document.set_extracted_text(extracted_text)

            repo.update(document)
            uow.track(document)
            return ServiceResult(data=document)

    def delete_document(
        self, actor: SupportsPermissionCheck, document_id: UUID
    ) -> ServiceResult[None]:
        self._authorize(actor, "library", "document", "delete")

        with self._uow_factory() as uow:
            repo = uow.get_repository("DocumentRepository")
            document = repo.get(document_id)
            if not document:
                raise DocumentNotFoundError(f"Document {document_id} introuvable")

            repo.delete(document_id)
            return ServiceResult(data=None)
