import uuid
import pytest
from src.domains.library.entities.enums import DocumentSource, DocumentType
from src.domains.library.exceptions import DocumentNotFoundError
from src.domains.library.repositories.filters import DocumentFilter


class MockActor:
    def has_permission(self, permission: str) -> bool:
        return True


def test_document_service_crud(domain_service):
    actor = MockActor()
    doc_service = domain_service.library.document_service
    s_id = uuid.uuid4()

    # Create
    result = doc_service.create_document(
        actor,
        title="Fiche résumé Géographie",
        file_path="uploads/geo.pdf",
        file_name="geo.pdf",
        file_size_bytes=512,
        subject_id=s_id,
        document_type=DocumentType.COURSE,
        source=DocumentSource.USER,
        year=2024,
    )
    doc = result.data
    assert doc.id is not None
    assert doc.title == "Fiche résumé Géographie"

    # Get
    get_res = doc_service.get_document(actor, doc.id)
    assert get_res.data.id == doc.id

    # List
    list_res = doc_service.list_documents(actor, DocumentFilter(subject_id=s_id))
    assert len(list_res.data) == 1
    assert list_res.meta["total"] == 1

    # Update
    update_res = doc_service.update_document(
        actor,
        doc.id,
        title="Fiche résumé Géographie - Climat",
        extracted_text="Contenu du climat en Guinée",
    )
    assert update_res.data.title == "Fiche résumé Géographie - Climat"
    assert update_res.data.is_text_extracted is True
    assert update_res.data.extracted_text == "Contenu du climat en Guinée"

    # Delete
    delete_res = doc_service.delete_document(actor, doc.id)
    assert delete_res.data is None

    # Get after delete raises NotFoundError
    with pytest.raises(DocumentNotFoundError):
        doc_service.get_document(actor, doc.id)
