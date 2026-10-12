from src.domains.curriculum.entities import Chapter, Lesson, Subject
from src.domains.curriculum.repositories.sql.orms import (
    ChapterOrm,
    LessonOrm,
    SubjectOrm,
)


class SubjectMapper:
    @staticmethod
    def to_entity(orm_obj: SubjectOrm) -> Subject:
        return Subject(
            id=orm_obj.id,
            name=orm_obj.name,
            code=orm_obj.code,
            is_active=orm_obj.is_active,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
        )

    @staticmethod
    def to_orm(entity: Subject) -> SubjectOrm:
        return SubjectOrm(
            id=entity.id,
            name=entity.name,
            code=entity.code,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class ChapterMapper:
    @staticmethod
    def to_entity(orm_obj: ChapterOrm) -> Chapter:
        return Chapter(
            id=orm_obj.id,
            subject_id=orm_obj.subject_id,
            title=orm_obj.title,
            description=orm_obj.description,
            order=orm_obj.order,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
        )

    @staticmethod
    def to_orm(entity: Chapter) -> ChapterOrm:
        return ChapterOrm(
            id=entity.id,
            subject_id=entity.subject_id,
            title=entity.title,
            description=entity.description,
            order=entity.order,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class LessonMapper:
    @staticmethod
    def to_entity(orm_obj: LessonOrm) -> Lesson:
        return Lesson(
            id=orm_obj.id,
            chapter_id=orm_obj.chapter_id,
            title=orm_obj.title,
            content=orm_obj.content,
            order=orm_obj.order,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
        )

    @staticmethod
    def to_orm(entity: Lesson) -> LessonOrm:
        return LessonOrm(
            id=entity.id,
            chapter_id=entity.chapter_id,
            title=entity.title,
            content=entity.content,
            order=entity.order,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
