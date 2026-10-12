from uuid import UUID

from src.core.entities import ServiceResult
from src.core.services import BaseService, SupportsPermissionCheck
from src.domains.curriculum.entities import Lesson
from src.domains.curriculum.exceptions import LessonNotFoundError
from src.domains.curriculum.repositories.filters import LessonFilter
from src.domains.curriculum.repositories.sql import LessonRepository


class LessonService(BaseService):
    """Service gérant les leçons."""

    def get_lesson(
        self, actor: SupportsPermissionCheck, lesson_id: UUID
    ) -> ServiceResult[Lesson]:
        self._authorize(actor, "curriculum", "lesson", "read")

        with self._uow_factory() as uow:
            repo = uow.get_repository(LessonRepository)
            lesson = repo.get(lesson_id)
            if not lesson:
                raise LessonNotFoundError(f"Leçon {lesson_id} introuvable")
            return ServiceResult(data=lesson)

    def list_lessons(
        self, actor: SupportsPermissionCheck, filter: LessonFilter
    ) -> ServiceResult[list[Lesson]]:
        self._authorize(actor, "curriculum", "lesson", "read")

        with self._uow_factory() as uow:
            repo = uow.get_repository(LessonRepository)
            lessons = repo.list(filter)
            count = repo.count(filter)
            return ServiceResult(data=lessons, meta={"total": count})

    def create_lesson(
        self,
        actor: SupportsPermissionCheck,
        chapter_id: UUID,
        title: str,
        content: str,
        order: int,
    ) -> ServiceResult[Lesson]:
        self._authorize(actor, "curriculum", "lesson", "create")

        lesson = Lesson.create(
            chapter_id=chapter_id, title=title, content=content, order=order
        )

        with self._uow_factory() as uow:
            repo = uow.get_repository(LessonRepository)
            repo.add(lesson)
            uow.track(lesson)
            return ServiceResult(data=lesson)

    def update_lesson(
        self,
        actor: SupportsPermissionCheck,
        lesson_id: UUID,
        title: str | None = None,
        content: str | None = None,
        order: int | None = None,
    ) -> ServiceResult[Lesson]:
        self._authorize(actor, "curriculum", "lesson", "update")

        with self._uow_factory() as uow:
            repo = uow.get_repository(LessonRepository)
            lesson = repo.get(lesson_id)
            if not lesson:
                raise LessonNotFoundError(f"Leçon {lesson_id} introuvable")

            if title is not None:
                lesson.title = title
            if content is not None:
                lesson.content = content
            if order is not None:
                lesson.order = order

            repo.update(lesson)
            uow.track(lesson)
            return ServiceResult(data=lesson)

    def delete_lesson(
        self, actor: SupportsPermissionCheck, lesson_id: UUID
    ) -> ServiceResult[None]:
        self._authorize(actor, "curriculum", "lesson", "delete")

        with self._uow_factory() as uow:
            repo = uow.get_repository(LessonRepository)
            lesson = repo.get(lesson_id)
            if not lesson:
                raise LessonNotFoundError(f"Leçon {lesson_id} introuvable")

            repo.delete(lesson_id)
            return ServiceResult(data=None)
