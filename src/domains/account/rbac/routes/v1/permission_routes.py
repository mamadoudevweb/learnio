from typing import Any
from uuid import UUID

from flask import Blueprint, current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.core.routes.envelope import ok
from src.domains.account.rbac.repositories.filters import PermissionFilter
from src.domains.account.rbac.routes.v1.role_routes import JwtActor
from src.domains.account.rbac.routes.v1.schemas.rbac_schemas import (
    PermissionCreateSchema,
    PermissionResponseSchema,
)

permission_bp = Blueprint("permissions", __name__, url_prefix="/api/v1/permissions")


def _actor() -> JwtActor:
    return JwtActor(get_jwt_identity())


@permission_bp.route("", methods=["GET"])
@jwt_required()
def list_permissions() -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 20, type=int)
    domain = request.args.get("domain", None, type=str)
    resource = request.args.get("resource", None, type=str)
    action = request.args.get("action", None, type=str)
    result = ds.account.permission_service.list_permissions(
        _actor(),
        PermissionFilter(
            page=page,
            page_size=page_size,
            domain=domain,
            resource=resource,
            action=action,
        ),
    )
    return ok(
        [PermissionResponseSchema.model_validate(p).model_dump() for p in result.data],
        meta=result.meta,
    )


@permission_bp.route("/<uuid:permission_id>", methods=["GET"])
@jwt_required()
def get_permission(permission_id: UUID) -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    result = ds.account.permission_service.get_permission(_actor(), permission_id)
    return ok(PermissionResponseSchema.model_validate(result.data).model_dump())


@permission_bp.route("", methods=["POST"])
@jwt_required()
def create_permission() -> tuple[Any, int]:
    payload = PermissionCreateSchema.model_validate(request.get_json(force=True))
    ds = current_app.extensions["domain_service"]
    result = ds.account.permission_service.get_or_create(
        _actor(),
        domain=payload.domain,
        resource=payload.resource,
        action=payload.action,
    )
    return ok(
        PermissionResponseSchema.model_validate(result.data).model_dump(), status=201
    )


@permission_bp.route("/<uuid:permission_id>", methods=["DELETE"])
@jwt_required()
def delete_permission(permission_id: UUID) -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    ds.account.permission_service.delete_permission(_actor(), permission_id)
    return ok(None)
