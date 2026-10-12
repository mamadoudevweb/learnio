from datetime import date, datetime, timezone
from uuid import uuid4

from src.domains.auth.entities import (
    Account,
    AccountCreated,
    AccountUpdated,
    Credential,
    CredentialCreated,
    CredentialReset,
    PasswordChanged,
    PasswordResetCompleted,
    PasswordResetRequested,
    Permission,
    Role,
    Session,
    SessionCreated,
    SessionRevoked,
)


def test_account_creation_and_events():
    account = Account.create(
        first_name="Mamadou",
        last_name="Diallo",
        birth_date=date(2005, 5, 15),
    )

    assert account.id is not None
    assert account.first_name == "Mamadou"
    assert account.last_name == "Diallo"
    assert account.active is True
    assert account.role_ids == []

    events = account.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], AccountCreated)
    assert events[0].account_id == account.id
    assert events[0].first_name == "Mamadou"

    # Profile update
    account.update_profile(first_name="Mamadou Alfa")
    assert account.first_name == "Mamadou Alfa"
    update_events = account.collect_events()
    assert len(update_events) == 1
    assert isinstance(update_events[0], AccountUpdated)


def test_credential_creation_and_password_change():
    acc_id = uuid4()
    credential = Credential.create(
        account_id=acc_id,
        email="User@Domain.COM",
        password_hash="hashed_pw_123",
    )

    assert credential.email == "user@domain.com"
    assert credential.email_verified is False

    events = credential.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], CredentialCreated)

    credential.change_password("new_hashed_pw")
    assert credential.password_hash == "new_hashed_pw"
    change_events = credential.collect_events()
    assert len(change_events) == 1
    assert isinstance(change_events[0], PasswordChanged)


def test_session_lifecycle():
    acc_id = uuid4()
    session_created_time = datetime(2026, 1, 1, tzinfo=timezone.utc)
    session = Session.create(
        account_id=acc_id,
        token_hash="fake_hash",
        expires_at=session_created_time,
    )
    events = session.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], SessionCreated)

    session.revoke()
    rev_events = session.collect_events()
    assert len(rev_events) == 1
    assert isinstance(rev_events[0], SessionRevoked)


def test_credential_reset_lifecycle():
    cred_id = uuid4()
    from datetime import datetime, timezone, timedelta
    expires = datetime.now(timezone.utc) + timedelta(minutes=15)
    reset = CredentialReset.create(
        credential_id=cred_id,
        token_hash="token_hash_abc",
        expires_at=expires,
        email="user@test.com",
    )

    assert reset.is_valid() is True
    events = reset.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], PasswordResetRequested)

    reset.consume()
    assert reset.is_valid() is False
    assert reset.used_at is not None
    comp_events = reset.collect_events()
    assert len(comp_events) == 1
    assert isinstance(comp_events[0], PasswordResetCompleted)


def test_role_and_permission_entities():
    perm = Permission.create(domain="library", resource="document", action="read")
    assert perm.triplet == "library:document:read"

    role = Role.create(name="Teacher", description="Teaching staff")
    assert role.name == "teacher"
    assert role.permission_ids == []

    role.assign_permission(perm.id)
    assert role.permission_ids == [perm.id]

    role.revoke_permission(perm.id)
    assert role.permission_ids == []
