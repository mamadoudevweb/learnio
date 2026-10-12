from datetime import date

import pytest

from src.domains.account.exceptions import (
    AccountInactiveError,
    CredentialNotFoundError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    ResetTokenExpiredOrInvalidError,
)


class MockActor:
    def has_permission(self, permission: str) -> bool:
        return True


def test_register_creates_account_and_credential(domain_service):
    auth_service = domain_service.account.authentication_service
    res = auth_service.register(
        first_name="Alpha",
        last_name="Diallo",
        email="alpha_create@learnio.app",
        password="SecurePassword123!",
        birth_date=date(2006, 1, 1),
    )

    account = res.data["account"]
    credential = res.data["credential"]
    assert account.id is not None
    assert account.first_name == "Alpha"
    assert credential.email == "alpha_create@learnio.app"


def test_register_duplicate_email_raises_email_already_exists(domain_service):
    auth_service = domain_service.account.authentication_service
    auth_service.register(
        first_name="Alpha",
        last_name="Diallo",
        email="duplicate@learnio.app",
        password="SecurePassword123!",
    )

    with pytest.raises(EmailAlreadyExistsError):
        auth_service.register(
            first_name="Other",
            last_name="User",
            email="duplicate@learnio.app",
            password="OtherPassword123!",
        )


def test_login_with_invalid_password_raises_invalid_credentials(domain_service):
    auth_service = domain_service.account.authentication_service
    auth_service.register(
        first_name="Test",
        last_name="User",
        email="badpass@learnio.app",
        password="CorrectPassword123!",
    )

    with pytest.raises(InvalidCredentialsError):
        auth_service.login(email="badpass@learnio.app", password="WrongPassword!")


def test_login_with_unknown_email_raises_invalid_credentials(domain_service):
    auth_service = domain_service.account.authentication_service

    with pytest.raises(InvalidCredentialsError):
        auth_service.login(email="unknown@learnio.app", password="Password123!")


def test_login_with_inactive_account_raises_account_inactive(domain_service):
    actor = MockActor()
    auth_service = domain_service.account.authentication_service
    account_service = domain_service.account.account_service

    reg = auth_service.register(
        first_name="Inactive",
        last_name="User",
        email="inactive@learnio.app",
        password="Password123!",
    )
    acc = reg.data["account"]
    account_service.update_account(actor, acc.id, active=False)

    with pytest.raises(AccountInactiveError):
        auth_service.login(email="inactive@learnio.app", password="Password123!")


def test_login_success_returns_session_token(domain_service):
    auth_service = domain_service.account.authentication_service
    auth_service.register(
        first_name="Valid",
        last_name="User",
        email="valid@learnio.app",
        password="Password123!",
    )

    login_res = auth_service.login(
        email="valid@learnio.app",
        password="Password123!",
        ip="127.0.0.1",
        user_agent="PyTest",
    )
    assert login_res.data["token"] is not None
    assert (
        login_res.data["account"].email
        if hasattr(login_res.data["account"], "email")
        else True
    )


def test_login_returns_associated_role_permissions(domain_service):
    actor = MockActor()
    auth_service = domain_service.account.authentication_service
    account_service = domain_service.account.account_service
    role_service = domain_service.account.role_service

    reg = auth_service.register(
        first_name="Perm",
        last_name="User",
        email="perms@learnio.app",
        password="Password123!",
    )
    account = reg.data["account"]

    perm = role_service.get_or_create_permission(
        actor, domain="curriculum", resource="subject", action="create"
    ).data
    role = role_service.create_role(
        actor, name="curriculum_creator", permission_ids=[perm.id]
    ).data
    account_service.assign_role_to_account(actor, account.id, role.id)

    login_res = auth_service.login(email="perms@learnio.app", password="Password123!")
    assert "curriculum:subject:create" in login_res.data["permissions"]


def test_validate_session_with_valid_token_returns_account(domain_service):
    auth_service = domain_service.account.authentication_service
    reg = auth_service.register(
        first_name="Sess",
        last_name="User",
        email="sess@learnio.app",
        password="Password123!",
    )
    token = auth_service.login(email="sess@learnio.app", password="Password123!").data[
        "token"
    ]

    validated = auth_service.validate_session(token).data
    assert validated.id == reg.data["account"].id


def test_validate_session_with_invalid_token_raises_invalid_credentials(domain_service):
    auth_service = domain_service.account.authentication_service

    with pytest.raises(InvalidCredentialsError):
        auth_service.validate_session("non_existent_token_string")


def test_request_password_reset_generates_token(domain_service):
    auth_service = domain_service.account.authentication_service
    auth_service.register(
        first_name="Reset",
        last_name="User",
        email="reset@learnio.app",
        password="OldPassword123!",
    )

    req_res = auth_service.request_password_reset("reset@learnio.app")
    assert req_res.data["token"] is not None


def test_request_password_reset_with_unknown_email_raises_credential_not_found(
    domain_service,
):
    auth_service = domain_service.account.authentication_service

    with pytest.raises(CredentialNotFoundError):
        auth_service.request_password_reset("nonexistent@learnio.app")


def test_reset_password_updates_credential_password(domain_service):
    auth_service = domain_service.account.authentication_service
    auth_service.register(
        first_name="ResetOk",
        last_name="User",
        email="reset_ok@learnio.app",
        password="OldPassword123!",
    )

    reset_token = auth_service.request_password_reset("reset_ok@learnio.app").data[
        "token"
    ]
    auth_service.reset_password(reset_token, "BrandNewPassword123!")

    # Login with new password succeeds
    login_new = auth_service.login(
        email="reset_ok@learnio.app", password="BrandNewPassword123!"
    )
    assert login_new.data["token"] is not None


def test_reset_password_invalidates_old_password(domain_service):
    auth_service = domain_service.account.authentication_service
    auth_service.register(
        first_name="ResetInvalid",
        last_name="User",
        email="reset_invalid@learnio.app",
        password="OldPassword123!",
    )

    reset_token = auth_service.request_password_reset("reset_invalid@learnio.app").data[
        "token"
    ]
    auth_service.reset_password(reset_token, "BrandNewPassword123!")

    # Login with old password fails
    with pytest.raises(InvalidCredentialsError):
        auth_service.login(
            email="reset_invalid@learnio.app", password="OldPassword123!"
        )


def test_reset_password_with_invalid_token_raises_error(domain_service):
    auth_service = domain_service.account.authentication_service

    with pytest.raises(ResetTokenExpiredOrInvalidError):
        auth_service.reset_password("invalid_token_xyz", "NewPassword123!")


def test_revoke_session_invalidates_session(domain_service):
    auth_service = domain_service.account.authentication_service
    auth_service.register(
        first_name="Logout",
        last_name="User",
        email="logout@learnio.app",
        password="Password123!",
    )
    token = auth_service.login(
        email="logout@learnio.app", password="Password123!"
    ).data["token"]

    auth_service.revoke_session(token)

    with pytest.raises(InvalidCredentialsError):
        auth_service.validate_session(token)
