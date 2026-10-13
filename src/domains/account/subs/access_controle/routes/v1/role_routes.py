from typing import Any
from uuid import UUID

from flask import Blueprint, current_app, request
from flask_jwt_extended import jwt_required

from src.core.routes.envelope import ok
from src.domains.account.subs.access_controle.repositories.filters import RoleFilter
from src.domains.account.subs.access_controle.routes.v1.schemas.rbac_schemas import (
    RoleCreateSchema,
    RoleResponseSchema,
)

role_bp = Blueprint("roles", __name__, url_prefix="/api/v1/roles")


from src.core.security import JwtActor, get_current_actor


def _actor() -> JwtActor:
    return get_current_actor()


@role_bp.route("", methods=["GET"])
@jwt_required()
def list_roles() -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 20, type=int)
    name = request.args.get("name", None, type=str)
    result = ds.account.role_service.list_roles(
        _actor(), RoleFilter(page=page, page_size=page_size, name=name)
    )
    return ok(
        [RoleResponseSchema.model_validate(r).model_dump() for r in result.data],
        meta=result.meta,
    )


@role_bp.route("/<uuid:role_id>", methods=["GET"])
@jwt_required()
def get_role(role_id: UUID) -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    result = ds.account.role_service.get_role(_actor(), role_id)
    return ok(RoleResponseSchema.model_validate(result.data).model_dump())


@role_bp.route("", methods=["POST"])
@jwt_required()
def create_role() -> tuple[Any, int]:
    payload = RoleCreateSchema.model_validate(request.get_json(force=True))
    ds = current_app.extensions["domain_service"]
    result = ds.account.role_service.create_role(
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
    result = ds.account.role_service.assign_permission_to_role(
        _actor(), role_id, permission_id
    )
    return ok(RoleResponseSchema.model_validate(result.data).model_dump())


@role_bp.route("/<uuid:role_id>/permissions/<uuid:permission_id>", methods=["DELETE"])
@jwt_required()
def revoke_permission(role_id: UUID, permission_id: UUID) -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    result = ds.account.role_service.revoke_permission_from_role(
        _actor(), role_id, permission_id
    )
    return ok(RoleResponseSchema.model_validate(result.data).model_dump())


@role_bp.route("/<uuid:role_id>", methods=["DELETE"])
@jwt_required()
def delete_role(role_id: UUID) -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    ds.account.role_service.delete_role(_actor(), role_id)
    return ok(None)
