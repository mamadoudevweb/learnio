import uuid
from src.domains.curriculum.exceptions import ChapterNotFoundError
from src.domains.curriculum.repositories.filters import ChapterFilter


class MockActor:
    def has_permission(self, permission: str) -> bool:
        return True


def test_chapter_service_crud(domain_service):
    actor = MockActor()
    chapter_service = domain_service.curriculum.chapter_service
    subject_id = uuid.uuid4()

    # Create
    result = chapter_service.create_chapter(actor, subject_id=subject_id, title="Algèbre", order=1)
    assert result.data.id is not None
    assert result.data.title == "Algèbre"
    chapter_id = result.data.id

    # Read
    get_result = chapter_service.get_chapter(actor, chapter_id)
    assert get_result.data.title == "Algèbre"

    # List
    filter_req = ChapterFilter(subject_id=subject_id)
    list_result = chapter_service.list_chapters(actor, filter_req)
    assert len(list_result.data) == 1

    # Update
    update_result = chapter_service.update_chapter(actor, chapter_id, title="Algèbre 2", description="Suite")
    assert update_result.data.title == "Algèbre 2"
    assert update_result.data.description == "Suite"

    # Delete
    chapter_service.delete_chapter(actor, chapter_id)

    # Read after delete (should raise)
    try:
        chapter_service.get_chapter(actor, chapter_id)
        assert False, "Should have raised ChapterNotFoundError"
    except ChapterNotFoundError:
        pass
