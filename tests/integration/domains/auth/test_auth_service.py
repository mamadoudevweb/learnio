from datetime import date
from uuid import uuid4

import pytest

from src.domains.auth.exceptions import (
    AccountInactiveError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    ResetTokenExpiredOrInvalidError,
)
from src.domains.auth.repositories.filters import AccountFilter, RoleFilter


class MockActor:
    def has_permission(self, permission: str) -> bool:
        return True


def test_authentication_service_register_and_login_flow(domain_service):
    actor = MockActor()
    auth_service = domain_service.auth.authentication_service
    acc_service = domain_service.auth.account_service
    role_service = domain_service.auth.role_service

    # 1. Register
    reg_result = auth_service.register(
        first_name="Alpha",
        last_name="Diallo",
        email="alpha@learnio.app",
        password="SecurePassword123!",
        birth_date=date(2006, 1, 1),
    )
    account = reg_result.data["account"]
    assert account.id is not None
    assert account.first_name == "Alpha"

    # Duplicate registration raises EmailAlreadyExistsError
    with pytest.raises(EmailAlreadyExistsError):
        auth_service.register(
            first_name="Alpha",
            last_name="Diallo",
            email="alpha@learnio.app",
            password="OtherPassword123!",
        )

    # 2. Login with bad credentials raises InvalidCredentialsError
    with pytest.raises(InvalidCredentialsError):
        auth_service.login(email="alpha@learnio.app", password="WrongPassword!")

    # 3. Successful login
    login_result = auth_service.login(
        email="alpha@learnio.app",
        password="SecurePassword123!",
        ip="127.0.0.1",
        user_agent="PyTest-Agent",
    )
    token = login_result.data["token"]
    assert token is not None

    # Validate session
    sess_result = auth_service.validate_session(token)
    assert sess_result.data.id == account.id

    # 4. Password reset request
    reset_req = auth_service.request_password_reset("alpha@learnio.app")
    reset_token = reset_req.data["token"]
    assert reset_token is not None

    # Reset password
    auth_service.reset_password(reset_token, "BrandNewPassword123!")

    # Old password no longer works
    with pytest.raises(InvalidCredentialsError):
        auth_service.login(email="alpha@learnio.app", password="SecurePassword123!")

    # New password works
    new_login = auth_service.login(email="alpha@learnio.app", password="BrandNewPassword123!")
    assert new_login.data["token"] is not None

    # 5. Role and permission assignment
    perm = role_service.get_or_create_permission(actor, domain="curriculum", resource="subject", action="create").data
    role = role_service.create_role(actor, name="admin", permission_ids=[perm.id]).data
    acc_service.assign_role_to_account(actor, account.id, role.id)

    # Logging in now returns assigned permissions
    login_with_perms = auth_service.login(email="alpha@learnio.app", password="BrandNewPassword123!")
    assert "curriculum:subject:create" in login_with_perms.data["permissions"]
