from typing import Any
from uuid import UUID

from flask import Blueprint, current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.core.routes.envelope import ok
from src.domains.account.rbac.routes.v1.role_routes import JwtActor
from src.domains.account.repositories.filters import AccountFilter
from src.domains.account.routes.v1.schemas.account_schemas import (
    AccountCreateSchema,
    AccountResponseSchema,
    AccountUpdateSchema,
)

account_bp = Blueprint("accounts", __name__, url_prefix="/api/v1/accounts")


def _actor() -> JwtActor:
    return JwtActor(get_jwt_identity())


@account_bp.route("", methods=["GET"])
@jwt_required()
def list_accounts() -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 20, type=int)
    search = request.args.get("search", None, type=str)
    active = request.args.get("active", None, type=lambda v: str(v).lower() == "true")

    filter_obj = AccountFilter(
        page=page, page_size=page_size, search=search, active=active
    )
    result = ds.account.account_service.list_accounts(_actor(), filter_obj)
    data = [
        AccountResponseSchema.model_validate(acc).model_dump() for acc in result.data
    ]
    return ok(data, meta=result.meta)


@account_bp.route("/<uuid:account_id>", methods=["GET"])
@jwt_required()
def get_account(account_id: UUID) -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    result = ds.account.account_service.get_account(_actor(), account_id)
    return ok(AccountResponseSchema.model_validate(result.data).model_dump())


@account_bp.route("", methods=["POST"])
@jwt_required()
def create_account() -> tuple[Any, int]:
    payload = AccountCreateSchema.model_validate(request.get_json(force=True))
    ds = current_app.extensions["domain_service"]
    result = ds.account.account_service.create_account(
        _actor(),
        first_name=payload.first_name,
        last_name=payload.last_name,
        birth_date=payload.birth_date,
        active=payload.active,
        role_ids=payload.role_ids,
    )
    return ok(
        AccountResponseSchema.model_validate(result.data).model_dump(), status=201
    )


@account_bp.route("/<uuid:account_id>", methods=["PUT"])
@jwt_required()
def update_account(account_id: UUID) -> tuple[Any, int]:
    payload = AccountUpdateSchema.model_validate(request.get_json(force=True))
    ds = current_app.extensions["domain_service"]
    result = ds.account.account_service.update_account(
        _actor(),
        account_id=account_id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        birth_date=payload.birth_date,
        active=payload.active,
    )
    return ok(AccountResponseSchema.model_validate(result.data).model_dump())


@account_bp.route("/<uuid:account_id>/roles/<uuid:role_id>", methods=["POST"])
@jwt_required()
def assign_role_to_account(account_id: UUID, role_id: UUID) -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    result = ds.account.account_service.assign_role_to_account(
        _actor(), account_id, role_id
    )
    return ok(AccountResponseSchema.model_validate(result.data).model_dump())


@account_bp.route("/<uuid:account_id>/roles/<uuid:role_id>", methods=["DELETE"])
@jwt_required()
def remove_role_from_account(account_id: UUID, role_id: UUID) -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    result = ds.account.account_service.remove_role_from_account(
        _actor(), account_id, role_id
    )
    return ok(AccountResponseSchema.model_validate(result.data).model_dump())


@account_bp.route("/<uuid:account_id>", methods=["DELETE"])
@jwt_required()
def delete_account(account_id: UUID) -> tuple[Any, int]:
    ds = current_app.extensions["domain_service"]
    ds.account.account_service.delete_account(_actor(), account_id)
    return ok(None)
