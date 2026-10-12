from typing import Any
from uuid import UUID

from flask import Blueprint, current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.core.routes.envelope import ok
from src.domains.library.repositories.filters import DocumentFilter
from src.domains.library.routes.v1.schemas.document_schema import (
    DocumentCreateSchema,
    DocumentListQuerySchema,
    DocumentResponseSchema,
    DocumentUpdateSchema,
)

document_bp = Blueprint("documents", __name__, url_prefix="/api/v1/documents")


class MockActor:
    """Acteur pour vérification d'autorisation."""

    def __init__(self, user_id: str):
        self.user_id = user_id

    def has_permission(self, permission: str) -> bool:
        return True


@document_bp.route("", methods=["GET"])
@jwt_required()
def list_documents() -> tuple[Any, int]:
    """Liste les documents de la bibliothèque avec filtres et pagination."""
    query_data = DocumentListQuerySchema(**request.args)
    actor = MockActor(get_jwt_identity())
    domain_service = current_app.extensions["domain_service"]

    filter = DocumentFilter(
        page=query_data.page,
        page_size=query_data.page_size,
        subject_id=query_data.subject_id,
        chapter_id=query_data.chapter_id,
        document_type=query_data.document_type,
        source=query_data.source,
        year=query_data.year,
        search=query_data.search,
    )

    result = domain_service.library.document_service.list_documents(actor, filter)
    data = [DocumentResponseSchema(**doc.__dict__).model_dump() for doc in result.data]
    return ok(data, meta=result.meta)


@document_bp.route("/<uuid:document_id>", methods=["GET"])
@jwt_required()
def get_document(document_id: UUID) -> tuple[Any, int]:
    """Récupère un document par son identifiant."""
    actor = MockActor(get_jwt_identity())
    domain_service = current_app.extensions["domain_service"]

    result = domain_service.library.document_service.get_document(actor, document_id)
    data = DocumentResponseSchema(**result.data.__dict__).model_dump()
    return ok(data)


@document_bp.route("", methods=["POST"])
@jwt_required()
def create_document() -> tuple[Any, int]:
    """Enregistre un document dans la bibliothèque."""
    payload = DocumentCreateSchema.model_validate(request.get_json(force=True))
    actor = MockActor(get_jwt_identity())
    domain_service = current_app.extensions["domain_service"]

    result = domain_service.library.document_service.create_document(
        actor,
        title=payload.title,
        file_path=payload.file_path,
        file_name=payload.file_name,
        file_size_bytes=payload.file_size_bytes,
        mime_type=payload.mime_type,
        subject_id=payload.subject_id,
        chapter_id=payload.chapter_id,
        document_type=payload.document_type,
        source=payload.source,
        year=payload.year,
        extracted_text=payload.extracted_text,
        is_text_extracted=payload.extracted_text is not None,
    )
    data = DocumentResponseSchema(**result.data.__dict__).model_dump()
    return ok(data, status=201)


@document_bp.route("/<uuid:document_id>", methods=["PUT"])
@jwt_required()
def update_document(document_id: UUID) -> tuple[Any, int]:
    """Met à jour les métadonnées d'un document."""
    payload = DocumentUpdateSchema.model_validate(request.get_json(force=True))
    actor = MockActor(get_jwt_identity())
    domain_service = current_app.extensions["domain_service"]

    result = domain_service.library.document_service.update_document(
        actor,
        document_id=document_id,
        title=payload.title,
        subject_id=payload.subject_id,
        chapter_id=payload.chapter_id,
        document_type=payload.document_type,
        year=payload.year,
        extracted_text=payload.extracted_text,
    )
    data = DocumentResponseSchema(**result.data.__dict__).model_dump()
    return ok(data)


@document_bp.route("/<uuid:document_id>", methods=["DELETE"])
@jwt_required()
def delete_document(document_id: UUID) -> tuple[Any, int]:
    """Supprime un document de la bibliothèque."""
    actor = MockActor(get_jwt_identity())
    domain_service = current_app.extensions["domain_service"]

    domain_service.library.document_service.delete_document(actor, document_id)
    return ok(None)
