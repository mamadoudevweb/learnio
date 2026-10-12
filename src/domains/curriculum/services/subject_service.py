from uuid import UUID

from src.core.services import BaseService, SupportsPermissionCheck
from src.core.entities import ServiceResult
from src.domains.curriculum.entities import Subject
from src.domains.curriculum.exceptions import SubjectNotFoundError
from src.domains.curriculum.repositories.filters import SubjectFilter
from src.domains.curriculum.repositories.sql import SubjectRepository


class SubjectService(BaseService):
    """Service gérant les matières."""

    def get_subject(
        self, actor: SupportsPermissionCheck, subject_id: UUID
    ) -> ServiceResult[Subject]:
        self._authorize(actor, "curriculum", "subject", "read")

        with self._uow_factory() as uow:
            repo = uow.get_repository(SubjectRepository)
            subject = repo.get(subject_id)
            if not subject:
                raise SubjectNotFoundError(f"Matière {subject_id} introuvable")
            return ServiceResult(data=subject)

    def list_subjects(
        self, actor: SupportsPermissionCheck, filter: SubjectFilter
    ) -> ServiceResult[list[Subject]]:
        self._authorize(actor, "curriculum", "subject", "read")

        with self._uow_factory() as uow:
            repo = uow.get_repository(SubjectRepository)
            subjects = repo.list(filter)
            count = repo.count(filter)
            return ServiceResult(data=subjects, meta={"total": count})

    def create_subject(
        self, actor: SupportsPermissionCheck, name: str, code: str
    ) -> ServiceResult[Subject]:
        self._authorize(actor, "curriculum", "subject", "create")

        subject = Subject.create(name=name, code=code)

        with self._uow_factory() as uow:
            repo = uow.get_repository(SubjectRepository)
            # Todo: check if code already exists if we need uniqueness
            repo.add(subject)
            uow.track(subject)
            return ServiceResult(data=subject)

    def update_subject(
        self,
        actor: SupportsPermissionCheck,
        subject_id: UUID,
        name: str | None = None,
        code: str | None = None,
        is_active: bool | None = None,
    ) -> ServiceResult[Subject]:
        self._authorize(actor, "curriculum", "subject", "update")

        with self._uow_factory() as uow:
            repo = uow.get_repository(SubjectRepository)
            subject = repo.get(subject_id)
            if not subject:
                raise SubjectNotFoundError(f"Matière {subject_id} introuvable")

            if name is not None:
                subject.name = name
            if code is not None:
                subject.code = code
            if is_active is not None:
                subject.is_active = is_active

            repo.update(subject)
            uow.track(subject)
            return ServiceResult(data=subject)

    def delete_subject(
        self, actor: SupportsPermissionCheck, subject_id: UUID
    ) -> ServiceResult[None]:
        self._authorize(actor, "curriculum", "subject", "delete")

        with self._uow_factory() as uow:
            repo = uow.get_repository(SubjectRepository)
            subject = repo.get(subject_id)
            if not subject:
                raise SubjectNotFoundError(f"Matière {subject_id} introuvable")
            
            repo.delete(subject_id)
            return ServiceResult(data=None)
