from typing import Any
from uuid import UUID

from flask import Blueprint, current_app, request
from flask_jwt_extended import jwt_required

from src.core.routes.envelope import ok
from src.core.security import get_current_actor
from src.domains.curriculum.repositories.filters import ChapterFilter
from src.domains.curriculum.routes.v1.schemas.chapter_schema import (
    ChapterCreateSchema,
    ChapterListQuerySchema,
    ChapterResponseSchema,
    ChapterUpdateSchema,
)

chapter_bp = Blueprint("chapters", __name__, url_prefix="/api/v1/chapters")


@chapter_bp.route("", methods=["GET"])
@jwt_required()
def list_chapters() -> tuple[Any, int]:
    """Liste les chapitres."""
    query_data = ChapterListQuerySchema(**request.args)
    actor = get_current_actor()
    domain_service = current_app.extensions["domain_service"]

    filter = ChapterFilter(
        page=query_data.page,
        page_size=query_data.page_size,
        subject_id=query_data.subject_id,
    )

    result = domain_service.curriculum.chapter_service.list_chapters(actor, filter)
    data = [ChapterResponseSchema(**c.__dict__).model_dump() for c in result.data]
    return ok(data, meta=result.meta)


@chapter_bp.route("/<uuid:chapter_id>", methods=["GET"])
@jwt_required()
def get_chapter(chapter_id: UUID) -> tuple[Any, int]:
    """Récupère un chapitre par son ID."""
    actor = get_current_actor()
    domain_service = current_app.extensions["domain_service"]

    result = domain_service.curriculum.chapter_service.get_chapter(actor, chapter_id)
    data = ChapterResponseSchema(**result.data.__dict__).model_dump()
    return ok(data)


@chapter_bp.route("", methods=["POST"])
@jwt_required()
def create_chapter() -> tuple[Any, int]:
    """Crée un nouveau chapitre."""
    payload = ChapterCreateSchema.model_validate(request.get_json(force=True))
    actor = get_current_actor()
    domain_service = current_app.extensions["domain_service"]

    result = domain_service.curriculum.chapter_service.create_chapter(
        actor,
        subject_id=payload.subject_id,
        title=payload.title,
        order=payload.order,
        description=payload.description,
    )
    data = ChapterResponseSchema(**result.data.__dict__).model_dump()
    return ok(data, status=201)


@chapter_bp.route("/<uuid:chapter_id>", methods=["PUT"])
@jwt_required()
def update_chapter(chapter_id: UUID) -> tuple[Any, int]:
    """Met à jour un chapitre."""
    payload = ChapterUpdateSchema.model_validate(request.get_json(force=True))
    actor = get_current_actor()
    domain_service = current_app.extensions["domain_service"]

    result = domain_service.curriculum.chapter_service.update_chapter(
        actor,
        chapter_id=chapter_id,
        title=payload.title,
        description=payload.description,
        order=payload.order,
    )
    data = ChapterResponseSchema(**result.data.__dict__).model_dump()
    return ok(data)


@chapter_bp.route("/<uuid:chapter_id>", methods=["DELETE"])
@jwt_required()
def delete_chapter(chapter_id: UUID) -> tuple[Any, int]:
    """Supprime un chapitre."""
    actor = get_current_actor()
    domain_service = current_app.extensions["domain_service"]

    domain_service.curriculum.chapter_service.delete_chapter(actor, chapter_id)
    return ok(None)
