from typing import Any
from uuid import UUID

from flask import Blueprint, current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.core.routes.envelope import ok
from src.domains.curriculum.repositories.filters import LessonFilter
from src.domains.curriculum.routes.v1.schemas.lesson_schema import (
    LessonCreateSchema,
    LessonListQuerySchema,
    LessonResponseSchema,
    LessonUpdateSchema,
)

lesson_bp = Blueprint("lessons", __name__, url_prefix="/api/v1/lessons")


class MockActor:
    """Acteur simulé pour la V1."""

    def __init__(self, user_id: str):
        self.user_id = user_id

    def has_permission(self, permission: str) -> bool:
        return True


@lesson_bp.route("", methods=["GET"])
@jwt_required()
def list_lessons() -> tuple[Any, int]:
    """Liste les leçons."""
    query_data = LessonListQuerySchema(**request.args)
    actor = MockActor(get_jwt_identity())
    domain_service = current_app.extensions["domain_service"]
    
    filter = LessonFilter(
        page=query_data.page,
        page_size=query_data.page_size,
        chapter_id=query_data.chapter_id,
    )

    result = domain_service.curriculum.lesson_service.list_lessons(actor, filter)
    data = [LessonResponseSchema(**l.__dict__).model_dump() for l in result.data]
    return ok(data, meta=result.meta)


@lesson_bp.route("/<uuid:lesson_id>", methods=["GET"])
@jwt_required()
def get_lesson(lesson_id: UUID) -> tuple[Any, int]:
    """Récupère une leçon par son ID."""
    actor = MockActor(get_jwt_identity())
    domain_service = current_app.extensions["domain_service"]

    result = domain_service.curriculum.lesson_service.get_lesson(actor, lesson_id)
    data = LessonResponseSchema(**result.data.__dict__).model_dump()
    return ok(data)


@lesson_bp.route("", methods=["POST"])
@jwt_required()
def create_lesson() -> tuple[Any, int]:
    """Crée une nouvelle leçon."""
    payload = LessonCreateSchema.model_validate(request.get_json(force=True))
    actor = MockActor(get_jwt_identity())
    domain_service = current_app.extensions["domain_service"]

    result = domain_service.curriculum.lesson_service.create_lesson(
        actor, 
        chapter_id=payload.chapter_id, 
        title=payload.title, 
        content=payload.content,
        order=payload.order
    )
    data = LessonResponseSchema(**result.data.__dict__).model_dump()
    return ok(data, status=201)


@lesson_bp.route("/<uuid:lesson_id>", methods=["PUT"])
@jwt_required()
def update_lesson(lesson_id: UUID) -> tuple[Any, int]:
    """Met à jour une leçon."""
    payload = LessonUpdateSchema.model_validate(request.get_json(force=True))
    actor = MockActor(get_jwt_identity())
    domain_service = current_app.extensions["domain_service"]

    result = domain_service.curriculum.lesson_service.update_lesson(
        actor, 
        lesson_id=lesson_id, 
        title=payload.title, 
        content=payload.content, 
        order=payload.order
    )
    data = LessonResponseSchema(**result.data.__dict__).model_dump()
    return ok(data)


@lesson_bp.route("/<uuid:lesson_id>", methods=["DELETE"])
@jwt_required()
def delete_lesson(lesson_id: UUID) -> tuple[Any, int]:
    """Supprime une leçon."""
    actor = MockActor(get_jwt_identity())
    domain_service = current_app.extensions["domain_service"]

    domain_service.curriculum.lesson_service.delete_lesson(actor, lesson_id)
    return ok(None)
