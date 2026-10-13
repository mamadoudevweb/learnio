from typing import Any
from uuid import UUID

from flask import Blueprint, current_app, request
from flask_jwt_extended import jwt_required

from src.core.routes.envelope import ok
from src.core.security import get_current_actor
from src.domains.curriculum.repositories.filters import SubjectFilter
from src.domains.curriculum.routes.v1.schemas.subject_schema import (
    SubjectCreateSchema,
    SubjectListQuerySchema,
    SubjectResponseSchema,
    SubjectUpdateSchema,
)

subject_bp = Blueprint("subjects", __name__, url_prefix="/api/v1/subjects")


@subject_bp.route("", methods=["GET"])
@jwt_required()
def list_subjects() -> tuple[Any, int]:
    """Liste les matières scolaires."""
    query_data = SubjectListQuerySchema(**request.args)
    actor = get_current_actor()
    domain_service = current_app.extensions["domain_service"]

    filter = SubjectFilter(
        page=query_data.page,
        page_size=query_data.page_size,
        is_active=query_data.is_active,
        code=query_data.code,
    )

    result = domain_service.curriculum.subject_service.list_subjects(actor, filter)
    data = [SubjectResponseSchema(**s.__dict__).model_dump() for s in result.data]
    return ok(data, meta=result.meta)


@subject_bp.route("/<uuid:subject_id>", methods=["GET"])
@jwt_required()
def get_subject(subject_id: UUID) -> tuple[Any, int]:
    """Récupère une matière par son ID."""
    actor = get_current_actor()
    domain_service = current_app.extensions["domain_service"]

    result = domain_service.curriculum.subject_service.get_subject(actor, subject_id)
    data = SubjectResponseSchema(**result.data.__dict__).model_dump()
    return ok(data)


@subject_bp.route("", methods=["POST"])
@jwt_required()
def create_subject() -> tuple[Any, int]:
    """Crée une nouvelle matière."""
    payload = SubjectCreateSchema.model_validate(request.get_json(force=True))
    actor = get_current_actor()
    domain_service = current_app.extensions["domain_service"]

    result = domain_service.curriculum.subject_service.create_subject(
        actor, name=payload.name, code=payload.code
    )
    data = SubjectResponseSchema(**result.data.__dict__).model_dump()
    return ok(data, status=201)


@subject_bp.route("/<uuid:subject_id>", methods=["PUT"])
@jwt_required()
def update_subject(subject_id: UUID) -> tuple[Any, int]:
    """Met à jour une matière existante."""
    payload = SubjectUpdateSchema.model_validate(request.get_json(force=True))
    actor = get_current_actor()
    domain_service = current_app.extensions["domain_service"]

    result = domain_service.curriculum.subject_service.update_subject(
        actor,
        subject_id=subject_id,
        name=payload.name,
        code=payload.code,
        is_active=payload.is_active,
    )
    data = SubjectResponseSchema(**result.data.__dict__).model_dump()
    return ok(data)


@subject_bp.route("/<uuid:subject_id>", methods=["DELETE"])
@jwt_required()
def delete_subject(subject_id: UUID) -> tuple[Any, int]:
    """Supprime une matière."""
    actor = get_current_actor()
    domain_service = current_app.extensions["domain_service"]

    domain_service.curriculum.subject_service.delete_subject(actor, subject_id)
    return ok(None)
