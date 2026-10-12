import uuid

from src.domains.library.entities.document import Document
from src.domains.library.entities.enums import DocumentSource, DocumentType
from src.domains.library.repositories.filters import DocumentFilter
from src.domains.library.repositories.sql import DocumentRepository


def test_document_repository_crud_and_filters(uow_factory):
    with uow_factory() as uow:
        repo = uow.get_repository(DocumentRepository)

        s_id = uuid.uuid4()
        c_id = uuid.uuid4()

        doc1 = Document.create(
            title="Sujet BAC 2023 - Histoire",
            file_path="uploads/bac2023.pdf",
            file_name="bac2023.pdf",
            file_size_bytes=2048,
            subject_id=s_id,
            chapter_id=c_id,
            document_type=DocumentType.EXAM_PAPER,
            source=DocumentSource.USER,
            year=2023,
        )
        doc2 = Document.create(
            title="Corrigé Mathématiques Exercice 4",
            file_path="uploads/math_exo4.pdf",
            file_name="math_exo4.pdf",
            file_size_bytes=1024,
            document_type=DocumentType.CORRECTION,
            source=DocumentSource.EXTERNAL,
            year=2022,
        )

        repo.add(doc1)
        repo.add(doc2)

        # Get
        retrieved = repo.get(doc1.id)
        assert retrieved is not None
        assert retrieved.title == "Sujet BAC 2023 - Histoire"
        assert retrieved.year == 2023

        # List by subject_id
        res_subject = repo.list(DocumentFilter(subject_id=s_id))
        assert len(res_subject) == 1
        assert res_subject[0].id == doc1.id

        # List by document_type
        res_type = repo.list(DocumentFilter(document_type=DocumentType.CORRECTION))
        assert len(res_type) == 1
        assert res_type[0].id == doc2.id

        # List by search term
        res_search = repo.list(DocumentFilter(search="bac2023"))
        assert len(res_search) == 1
        assert res_search[0].id == doc1.id

        # Count
        total_count = repo.count(DocumentFilter())
        assert total_count == 2

        # Update
        doc1.update_metadata(title="Sujet BAC 2023 - Histoire SS")
        repo.update(doc1)
        updated = repo.get(doc1.id)
        assert updated.title == "Sujet BAC 2023 - Histoire SS"

        # Delete
        repo.delete(doc2.id)
        assert repo.get(doc2.id) is None
