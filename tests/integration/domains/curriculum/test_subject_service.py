from src.domains.curriculum.exceptions import SubjectNotFoundError
from src.domains.curriculum.repositories.filters import SubjectFilter


class MockActor:
    def has_permission(self, permission: str) -> bool:
        return True


def test_subject_service_crud(domain_service):
    actor = MockActor()
    subject_service = domain_service.curriculum.subject_service

    # Create
    result = subject_service.create_subject(actor, name="Physique", code="PHYS")
    assert result.data.id is not None
    assert result.data.name == "Physique"
    subject_id = result.data.id

    # Read
    get_result = subject_service.get_subject(actor, subject_id)
    assert get_result.data.name == "Physique"

    # List
    filter_req = SubjectFilter(code="PHYS", page=1, page_size=10)
    list_result = subject_service.list_subjects(actor, filter_req)
    assert len(list_result.data) == 1
    assert list_result.meta["total"] == 1

    # Update
    update_result = subject_service.update_subject(actor, subject_id, name="Physique-Chimie", is_active=False)
    assert update_result.data.name == "Physique-Chimie"
    assert update_result.data.is_active is False

    # Read after update
    get_result = subject_service.get_subject(actor, subject_id)
    assert get_result.data.name == "Physique-Chimie"

    # Delete
    subject_service.delete_subject(actor, subject_id)

    # Read after delete (should raise)
    try:
        subject_service.get_subject(actor, subject_id)
        assert False, "Should have raised SubjectNotFoundError"
    except SubjectNotFoundError:
        pass
