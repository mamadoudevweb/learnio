from typing import Any
from uuid import UUID

from flask import Blueprint, current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.core.routes.envelope import ok
from src.domains.access_control.repositories.filters import RoleFilter
from src.domains.access_control.routes.v1.schemas.access_control_schemas import (
    RoleCreateSchema,
    RoleResponseSchema,
)

role_bp = Blueprint("roles", __name__, url_prefix="/api/v1/roles")


def _actor() -> Any:
    from src.domains.auth.routes.v1.auth_routes import JwtActor
    return JwtActor(get_jwt_identity())


@role_bp.route("", methods=["GET"])
@jwt_required()
def list_roles() -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 20, type=int)
    name = request.args.get("name", None, type=str)
    result = ds.access_control.role_service.list_roles(
        _actor(), RoleFilter(page=page, page_size=page_size, name=name)
    )
    return ok([RoleResponseSchema.model_validate(r).model_dump() for r in result.data], meta=result.meta)


@role_bp.route("/<uuid:role_id>", methods=["GET"])
@jwt_required()
def get_role(role_id: UUID) -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    result = ds.access_control.role_service.get_role(_actor(), role_id)
    return ok(RoleResponseSchema.model_validate(result.data).model_dump())


@role_bp.route("", methods=["POST"])
@jwt_required()
def create_role() -> tuple[Any, int]:
    payload = RoleCreateSchema.model_validate(request.get_json(force=True))
    ds = current_app.extensions["domain_service"]
    result = ds.access_control.role_service.create_role(
        _actor(),
        name=payload.name,
        description=payload.description,
        permission_ids=payload.permission_ids,
    )
    return ok(RoleResponseSchema.model_validate(result.data).model_dump(), status=201)


@role_bp.route("/<uuid:role_id>/permissions/<uuid:permission_id>", methods=["POST"])
@jwt_required()
def assign_permission(role_id: UUID, permission_id: UUID) -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    result = ds.access_control.role_service.assign_permission_to_role(_actor(), role_id, permission_id)
    return ok(RoleResponseSchema.model_validate(result.data).model_dump())


@role_bp.route("/<uuid:role_id>/permissions/<uuid:permission_id>", methods=["DELETE"])
@jwt_required()
def revoke_permission(role_id: UUID, permission_id: UUID) -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    result = ds.access_control.role_service.revoke_permission_from_role(_actor(), role_id, permission_id)
    return ok(RoleResponseSchema.model_validate(result.data).model_dump())


@role_bp.route("/<uuid:role_id>", methods=["DELETE"])
@jwt_required()
def delete_role(role_id: UUID) -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    ds.access_control.role_service.delete_role(_actor(), role_id)
    return ok(None)
