from datetime import UTC, date, datetime, timedelta
from uuid import uuid4

from src.domains.account.entities import (
    Account,
    AccountCreated,
    AccountRoleAssigned,
    AccountRoleRemoved,
    AccountUpdated,
)
from src.domains.account.subs.access_controle.entities import (
    Permission,
    PermissionAssignedToRole,
    PermissionCreated,
    PermissionRevokedFromRole,
    Role,
    RoleCreated,
)
from src.domains.account.subs.auth.entities import (
    Credential,
    CredentialCreated,
    CredentialReset,
    PasswordChanged,
    PasswordResetCompleted,
    PasswordResetRequested,
    Session,
    SessionCreated,
    SessionRevoked,
)

# ---------------------------------------------------------------------------
# Account Entity Unit Tests
# ---------------------------------------------------------------------------


def test_account_creation_sets_attributes():
    birth = date(2005, 5, 15)
    account = Account.create(first_name="Mamadou", last_name="Diallo", birth_date=birth)

    assert account.id is not None
    assert account.first_name == "Mamadou"
    assert account.last_name == "Diallo"
    assert account.birth_date == birth
    assert account.active is True
    assert account.role_ids == []


def test_account_creation_emits_account_created_event():
    account = Account.create(first_name="Mamadou", last_name="Diallo")
    events = account.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], AccountCreated)
    assert events[0].account_id == account.id
    assert events[0].first_name == "Mamadou"


def test_account_update_profile_modifies_fields():
    account = Account.create(first_name="Mamadou", last_name="Diallo")
    account.collect_events()

    account.update_profile(first_name="Mamadou Alfa")
    assert account.first_name == "Mamadou Alfa"


def test_account_update_profile_emits_account_updated_event():
    account = Account.create(first_name="Mamadou", last_name="Diallo")
    account.collect_events()

    account.update_profile(last_name="Bah")
    events = account.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], AccountUpdated)
    assert events[0].account_id == account.id


def test_account_assign_role_adds_role_id():
    account = Account.create(first_name="Jane", last_name="Doe")
    role_id = uuid4()

    account.assign_role(role_id)
    assert role_id in account.role_ids


def test_account_assign_role_emits_role_assigned_event():
    account = Account.create(first_name="Jane", last_name="Doe")
    account.collect_events()
    role_id = uuid4()

    account.assign_role(role_id)
    events = account.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], AccountRoleAssigned)
    assert events[0].account_id == account.id
    assert events[0].role_id == role_id


def test_account_assign_existing_role_is_idempotent():
    account = Account.create(first_name="Jane", last_name="Doe")
    role_id = uuid4()
    account.assign_role(role_id)
    account.collect_events()

    account.assign_role(role_id)
    assert len(account.role_ids) == 1
    assert len(account.collect_events()) == 0


def test_account_remove_role_removes_role_id():
    role_id = uuid4()
    account = Account.create(first_name="Jane", last_name="Doe", role_ids=[role_id])

    account.remove_role(role_id)
    assert role_id not in account.role_ids


def test_account_remove_role_emits_role_removed_event():
    role_id = uuid4()
    account = Account.create(first_name="Jane", last_name="Doe", role_ids=[role_id])
    account.collect_events()

    account.remove_role(role_id)
    events = account.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], AccountRoleRemoved)
    assert events[0].account_id == account.id
    assert events[0].role_id == role_id


# ---------------------------------------------------------------------------
# Credential Entity Unit Tests
# ---------------------------------------------------------------------------


def test_credential_creation_normalizes_email():
    acc_id = uuid4()
    credential = Credential.create(
        account_id=acc_id,
        email="  User@Domain.COM  ",
        password_hash="hashed_pw_123",
    )

    assert credential.email == "user@domain.com"
    assert credential.email_verified is False


def test_credential_creation_emits_credential_created_event():
    acc_id = uuid4()
    credential = Credential.create(
        account_id=acc_id,
        email="user@domain.com",
        password_hash="hashed_pw_123",
    )
    events = credential.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], CredentialCreated)
    assert events[0].credential_id == credential.id
    assert events[0].account_id == acc_id
    assert events[0].email == "user@domain.com"


def test_credential_change_password_updates_hash():
    credential = Credential.create(
        account_id=uuid4(),
        email="user@domain.com",
        password_hash="initial_hash",
    )

    credential.change_password("new_hashed_pw")
    assert credential.password_hash == "new_hashed_pw"


def test_credential_change_password_emits_password_changed_event():
    acc_id = uuid4()
    credential = Credential.create(
        account_id=acc_id,
        email="user@domain.com",
        password_hash="initial_hash",
    )
    credential.collect_events()

    credential.change_password("new_hashed_pw")
    events = credential.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], PasswordChanged)
    assert events[0].credential_id == credential.id
    assert events[0].account_id == acc_id


def test_credential_verify_email_marks_verified():
    credential = Credential.create(
        account_id=uuid4(),
        email="user@domain.com",
        password_hash="hash",
    )

    credential.verify_email()
    assert credential.email_verified is True


# ---------------------------------------------------------------------------
# Session Entity Unit Tests
# ---------------------------------------------------------------------------


def test_session_creation_emits_session_created_event():
    acc_id = uuid4()
    expires = datetime.now(UTC) + timedelta(hours=2)
    session = Session.create(
        account_id=acc_id,
        token_hash="fake_hash",
        expires_at=expires,
    )
    events = session.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], SessionCreated)
    assert events[0].session_id == session.id
    assert events[0].account_id == acc_id


def test_session_active_when_not_expired_and_not_revoked():
    expires = datetime.now(UTC) + timedelta(hours=1)
    session = Session.create(
        account_id=uuid4(),
        token_hash="fake_hash",
        expires_at=expires,
    )

    assert session.is_active() is True


def test_session_inactive_when_expired():
    expired_time = datetime.now(UTC) - timedelta(seconds=10)
    session = Session.create(
        account_id=uuid4(),
        token_hash="expired_hash",
        expires_at=expired_time,
    )

    assert session.is_active() is False


def test_session_revoke_marks_inactive():
    expires = datetime.now(UTC) + timedelta(hours=1)
    session = Session.create(
        account_id=uuid4(),
        token_hash="hash",
        expires_at=expires,
    )

    session.revoke()
    assert session.is_active() is False
    assert session.revoked_at is not None


def test_session_revoke_emits_session_revoked_event():
    acc_id = uuid4()
    session = Session.create(
        account_id=acc_id,
        token_hash="hash",
        expires_at=datetime.now(UTC) + timedelta(hours=1),
    )
    session.collect_events()

    session.revoke()
    events = session.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], SessionRevoked)
    assert events[0].session_id == session.id
    assert events[0].account_id == acc_id


# ---------------------------------------------------------------------------
# CredentialReset Entity Unit Tests
# ---------------------------------------------------------------------------


def test_credential_reset_creation_emits_reset_requested_event():
    cred_id = uuid4()
    expires = datetime.now(UTC) + timedelta(minutes=15)
    reset = CredentialReset.create(
        credential_id=cred_id,
        token_hash="token_hash_abc",
        expires_at=expires,
        email="user@test.com",
    )
    events = reset.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], PasswordResetRequested)
    assert events[0].reset_id == reset.id
    assert events[0].credential_id == cred_id
    assert events[0].email == "user@test.com"


def test_credential_reset_is_valid_when_unconsumed_and_unexpired():
    expires = datetime.now(UTC) + timedelta(minutes=15)
    reset = CredentialReset.create(
        credential_id=uuid4(),
        token_hash="token_hash_abc",
        expires_at=expires,
        email="user@test.com",
    )

    assert reset.is_valid() is True


def test_credential_reset_is_invalid_when_expired():
    expired = datetime.now(UTC) - timedelta(minutes=5)
    reset = CredentialReset.create(
        credential_id=uuid4(),
        token_hash="token_hash_expired",
        expires_at=expired,
        email="user@test.com",
    )

    assert reset.is_valid() is False


def test_credential_reset_consume_marks_used():
    expires = datetime.now(UTC) + timedelta(minutes=15)
    reset = CredentialReset.create(
        credential_id=uuid4(),
        token_hash="hash",
        expires_at=expires,
        email="user@test.com",
    )

    reset.consume()
    assert reset.is_valid() is False
    assert reset.used_at is not None


def test_credential_reset_consume_emits_reset_completed_event():
    cred_id = uuid4()
    reset = CredentialReset.create(
        credential_id=cred_id,
        token_hash="hash",
        expires_at=datetime.now(UTC) + timedelta(minutes=15),
        email="user@test.com",
    )
    reset.collect_events()

    reset.consume()
    events = reset.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], PasswordResetCompleted)
    assert events[0].reset_id == reset.id
    assert events[0].credential_id == cred_id


# ---------------------------------------------------------------------------
# Role and Permission Entity Unit Tests
# ---------------------------------------------------------------------------


def test_permission_creation_normalizes_triplet():
    perm = Permission.create(domain="Library", resource="Document", action="READ")
    assert perm.triplet == "library:document:read"


def test_permission_creation_emits_permission_created_event():
    perm = Permission.create(domain="library", resource="document", action="read")
    events = perm.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], PermissionCreated)
    assert events[0].permission_id == perm.id
    assert events[0].triplet == "library:document:read"


def test_role_creation_normalizes_name():
    role = Role.create(name="  Teacher  ", description="Teaching staff")
    assert role.name == "teacher"
    assert role.description == "Teaching staff"
    assert role.permission_ids == []


def test_role_creation_emits_role_created_event():
    role = Role.create(name="student")
    events = role.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], RoleCreated)
    assert events[0].role_id == role.id
    assert events[0].name == "student"


def test_role_assign_permission_adds_id():
    role = Role.create(name="editor")
    perm_id = uuid4()

    role.assign_permission(perm_id)
    assert perm_id in role.permission_ids


def test_role_assign_permission_emits_event():
    role = Role.create(name="editor")
    role.collect_events()
    perm_id = uuid4()

    role.assign_permission(perm_id)
    events = role.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], PermissionAssignedToRole)
    assert events[0].role_id == role.id
    assert events[0].permission_id == perm_id


def test_role_revoke_permission_removes_id():
    perm_id = uuid4()
    role = Role.create(name="editor", permission_ids=[perm_id])

    role.revoke_permission(perm_id)
    assert perm_id not in role.permission_ids


def test_role_revoke_permission_emits_event():
    perm_id = uuid4()
    role = Role.create(name="editor", permission_ids=[perm_id])
    role.collect_events()

    role.revoke_permission(perm_id)
    events = role.collect_events()

    assert len(events) == 1
    assert isinstance(events[0], PermissionRevokedFromRole)
    assert events[0].role_id == role.id
    assert events[0].permission_id == perm_id
