from uuid import UUID

from src.core.entities import ServiceResult
from src.core.services import BaseService, SupportsPermissionCheck
from src.domains.curriculum.entities import Chapter
from src.domains.curriculum.exceptions import ChapterNotFoundError
from src.domains.curriculum.repositories.filters import ChapterFilter


class ChapterService(BaseService):
    """Service gérant les chapitres."""

    def get_chapter(
        self, actor: SupportsPermissionCheck, chapter_id: UUID
    ) -> ServiceResult[Chapter]:
        self._authorize(actor, "curriculum", "chapter", "read")

        with self._uow_factory() as uow:
            repo = uow.get_repository("ChapterRepository")
            chapter = repo.get(chapter_id)
            if not chapter:
                raise ChapterNotFoundError(f"Chapitre {chapter_id} introuvable")
            return ServiceResult(data=chapter)

    def list_chapters(
        self, actor: SupportsPermissionCheck, filter: ChapterFilter
    ) -> ServiceResult[list[Chapter]]:
        self._authorize(actor, "curriculum", "chapter", "read")

        with self._uow_factory() as uow:
            repo = uow.get_repository("ChapterRepository")
            chapters = repo.list(filter)
            count = repo.count(filter)
            return ServiceResult(data=chapters, meta={"total": count})

    def create_chapter(
        self,
        actor: SupportsPermissionCheck,
        subject_id: UUID,
        title: str,
        order: int,
        description: str = "",
    ) -> ServiceResult[Chapter]:
        self._authorize(actor, "curriculum", "chapter", "create")

        chapter = Chapter.create(
            subject_id=subject_id, title=title, order=order, description=description
        )

        with self._uow_factory() as uow:
            repo = uow.get_repository("ChapterRepository")
            repo.add(chapter)
            uow.track(chapter)
            return ServiceResult(data=chapter)

    def update_chapter(
        self,
        actor: SupportsPermissionCheck,
        chapter_id: UUID,
        title: str | None = None,
        description: str | None = None,
        order: int | None = None,
    ) -> ServiceResult[Chapter]:
        self._authorize(actor, "curriculum", "chapter", "update")

        with self._uow_factory() as uow:
            repo = uow.get_repository("ChapterRepository")
            chapter = repo.get(chapter_id)
            if not chapter:
                raise ChapterNotFoundError(f"Chapitre {chapter_id} introuvable")

            if title is not None:
                chapter.title = title
            if description is not None:
                chapter.description = description
            if order is not None:
                chapter.order = order

            repo.update(chapter)
            uow.track(chapter)
            return ServiceResult(data=chapter)

    def delete_chapter(
        self, actor: SupportsPermissionCheck, chapter_id: UUID
    ) -> ServiceResult[None]:
        self._authorize(actor, "curriculum", "chapter", "delete")

        with self._uow_factory() as uow:
            repo = uow.get_repository("ChapterRepository")
            chapter = repo.get(chapter_id)
            if not chapter:
                raise ChapterNotFoundError(f"Chapitre {chapter_id} introuvable")

            repo.delete(chapter_id)
            return ServiceResult(data=None)
