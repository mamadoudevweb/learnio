from typing import Any

from flask import Blueprint, current_app, request

from src.core.errors import ValidationError
from src.core.routes.envelope import ok
from src.domains.account.routes.v1.schemas.account_schemas import AccountResponseSchema
from src.domains.account.subs.auth.routes.v1.schemas.auth_schemas import (
    LoginRequestSchema,
    PasswordResetConfirmSchema,
    PasswordResetRequestSchema,
    RegisterRequestSchema,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth_bp.route("/register", methods=["POST"])
def register() -> tuple[Any, int]:
    """Endpoint public d'enregistrement de compte."""
    payload = RegisterRequestSchema.model_validate(request.get_json(force=True))
    ds = current_app.extensions["domain_service"]
    result = ds.account.authentication_service.register(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        password=payload.password,
        birth_date=payload.birth_date,
    )
    data = AccountResponseSchema.model_validate(result.data["account"]).model_dump()
    return ok(data, status=201)


@auth_bp.route("/login", methods=["POST"])
def login() -> tuple[Any, int]:
    """Endpoint public de connexion."""
    payload = LoginRequestSchema.model_validate(request.get_json(force=True))
    ds = current_app.extensions["domain_service"]
    user_agent = request.user_agent.string if request.user_agent else None
    result = ds.account.authentication_service.login(
        email=payload.email,
        password=payload.password,
        ip=request.remote_addr,
        user_agent=user_agent,
    )
    account_dict = AccountResponseSchema.model_validate(
        result.data["account"]
    ).model_dump()
    return ok(
        {
            "token": result.data["token"],
            "account": account_dict,
            "permissions": result.data["permissions"],
        }
    )


@auth_bp.route("/password-reset/request", methods=["POST"])
def request_password_reset() -> tuple[Any, int]:
    """Endpoint public de demande de réinitialisation de mot de passe."""
    payload = PasswordResetRequestSchema.model_validate(request.get_json(force=True))
    ds = current_app.extensions["domain_service"]
    result = ds.account.authentication_service.request_password_reset(
        email=payload.email
    )
    return ok(result.data)


@auth_bp.route("/password-reset/confirm", methods=["GET"])
@auth_bp.route("/password-reset/confirm/<token>", methods=["GET"])
def verify_password_reset_token(token: str | None = None) -> tuple[Any, int]:
    """Endpoint public de vérification de validité d'un jeton de réinitialisation."""
    reset_token = token or request.args.get("token", type=str)
    if not reset_token or not reset_token.strip():
        raise ValidationError(
            "Le jeton de réinitialisation est requis.",
            details={"token": "Jeton manquant dans les paramètres d'URL."},
        )
    ds = current_app.extensions["domain_service"]
    result = ds.account.authentication_service.validate_reset_token(
        token=reset_token.strip()
    )
    return ok(result.data)


@auth_bp.route("/password-reset/confirm", methods=["POST"])
@auth_bp.route("/password-reset/confirm/<token>", methods=["POST"])
def confirm_password_reset(token: str | None = None) -> tuple[Any, int]:
    """Endpoint public de confirmation de réinitialisation de mot de passe."""
    payload = PasswordResetConfirmSchema.model_validate(request.get_json(force=True))
    reset_token = token or request.args.get("token", type=str) or payload.token
    if not reset_token or not reset_token.strip():
        raise ValidationError(
            "Le jeton de réinitialisation est requis.",
            details={
                "token": "Jeton manquant dans les paramètres d'URL ou le corps de la requête."
            },
        )
    ds = current_app.extensions["domain_service"]
    ds.account.authentication_service.reset_password(
        token=reset_token.strip(),
        new_password=payload.new_password,
    )
    return ok(None)


@auth_bp.route("/logout", methods=["POST"])
def logout() -> tuple[Any, int]:
    """Endpoint de révocation de session."""
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()
    if not token and request.is_json:
        token = request.get_json(silent=True, force=False).get("token", "")
    ds = current_app.extensions["domain_service"]
    if token:
        ds.account.authentication_service.revoke_session(token)
    return ok(None)
