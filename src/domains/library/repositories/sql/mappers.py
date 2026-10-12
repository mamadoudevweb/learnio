from src.domains.library.entities.document import Document
from src.domains.library.entities.enums import DocumentSource, DocumentType
from src.domains.library.repositories.sql.orms import DocumentOrm


class DocumentMapper:
    @staticmethod
    def to_entity(orm_obj: DocumentOrm) -> Document:
        return Document(
            id=orm_obj.id,
            title=orm_obj.title,
            file_path=orm_obj.file_path,
            file_name=orm_obj.file_name,
            file_size_bytes=orm_obj.file_size_bytes,
            mime_type=orm_obj.mime_type,
            subject_id=orm_obj.subject_id,
            chapter_id=orm_obj.chapter_id,
            document_type=DocumentType(orm_obj.document_type),
            source=DocumentSource(orm_obj.source),
            year=orm_obj.year,
            extracted_text=orm_obj.extracted_text,
            is_text_extracted=orm_obj.is_text_extracted,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
        )

    @staticmethod
    def to_orm(entity: Document) -> DocumentOrm:
        return DocumentOrm(
            id=entity.id,
            title=entity.title,
            file_path=entity.file_path,
            file_name=entity.file_name,
            file_size_bytes=entity.file_size_bytes,
            mime_type=entity.mime_type,
            subject_id=entity.subject_id,
            chapter_id=entity.chapter_id,
            document_type=entity.document_type.value,
            source=entity.source.value,
            year=entity.year,
            extracted_text=entity.extracted_text,
            is_text_extracted=entity.is_text_extracted,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
