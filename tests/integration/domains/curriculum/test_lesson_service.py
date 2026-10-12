import uuid
from src.domains.curriculum.exceptions import LessonNotFoundError
from src.domains.curriculum.repositories.filters import LessonFilter


class MockActor:
    def has_permission(self, permission: str) -> bool:
        return True


def test_lesson_service_crud(domain_service):
    actor = MockActor()
    lesson_service = domain_service.curriculum.lesson_service
    chapter_id = uuid.uuid4()

    # Create
    result = lesson_service.create_lesson(
        actor, chapter_id=chapter_id, title="Les équations", content="Contenu", order=1
    )
    assert result.data.id is not None
    assert result.data.title == "Les équations"
    lesson_id = result.data.id

    # Read
    get_result = lesson_service.get_lesson(actor, lesson_id)
    assert get_result.data.content == "Contenu"

    # List
    filter_req = LessonFilter(chapter_id=chapter_id)
    list_result = lesson_service.list_lessons(actor, filter_req)
    assert len(list_result.data) == 1

    # Update
    update_result = lesson_service.update_lesson(actor, lesson_id, title="Équations du 1er degré")
    assert update_result.data.title == "Équations du 1er degré"

    # Delete
    lesson_service.delete_lesson(actor, lesson_id)

    # Read after delete (should raise)
    try:
        lesson_service.get_lesson(actor, lesson_id)
        assert False, "Should have raised LessonNotFoundError"
    except LessonNotFoundError:
        pass
