import uuid
from src.domains.library.entities.document import Document
from src.domains.library.entities.enums import DocumentSource, DocumentType
from src.domains.library.entities.events import DocumentCreated, DocumentUpdated


def test_document_creation():
    subject_id = uuid.uuid4()
    chapter_id = uuid.uuid4()

    doc = Document.create(
        title="Cours d'histoire - Décolonisation",
        file_path="uploads/history_ch1.pdf",
        file_name="history_ch1.pdf",
        file_size_bytes=1048576,
        subject_id=subject_id,
        chapter_id=chapter_id,
        document_type=DocumentType.COURSE,
        source=DocumentSource.USER,
        year=2024,
    )

    assert doc.id is not None
    assert doc.title == "Cours d'histoire - Décolonisation"
    assert doc.file_path == "uploads/history_ch1.pdf"
    assert doc.document_type == DocumentType.COURSE
    assert doc.source == DocumentSource.USER
    assert doc.is_text_extracted is False

    events = doc.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], DocumentCreated)
    assert events[0].document_id == doc.id


def test_document_update_metadata():
    doc = Document.create(
        title="Doc initial",
        file_path="uploads/test.pdf",
        file_name="test.pdf",
        file_size_bytes=500,
    )
    _ = doc.collect_events()

    doc.update_metadata(title="Doc renommé", year=2025)
    assert doc.title == "Doc renommé"
    assert doc.year == 2025

    events = doc.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], DocumentUpdated)


def test_document_extracted_text():
    doc = Document.create(
        title="Doc",
        file_path="uploads/doc.pdf",
        file_name="doc.pdf",
        file_size_bytes=500,
    )
    _ = doc.collect_events()

    doc.set_extracted_text("Extracted content text")
    assert doc.is_text_extracted is True
    assert doc.extracted_text == "Extracted content text"

    events = doc.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], DocumentUpdated)
