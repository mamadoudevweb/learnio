from datetime import date
from uuid import uuid4

import pytest

from src.domains.account.exceptions import AccountNotFoundError, RoleNotFoundError
from src.domains.account.repositories.filters import AccountFilter


class MockActor:
    def has_permission(self, permission: str) -> bool:
        return True


def test_create_account_persists_and_returns_account(domain_service):
    actor = MockActor()
    account_service = domain_service.account.account_service

    created = account_service.create_account(
        actor,
        first_name="Amadou",
        last_name="Barry",
        birth_date=date(2000, 10, 10),
    ).data

    assert created.id is not None
    assert created.first_name == "Amadou"
    assert created.last_name == "Barry"
    assert created.active is True


def test_get_account_by_id_returns_account(domain_service):
    actor = MockActor()
    account_service = domain_service.account.account_service

    created = account_service.create_account(
        actor,
        first_name="Boubacar",
        last_name="Diallo",
    ).data

    fetched = account_service.get_account(actor, created.id).data
    assert fetched.id == created.id
    assert fetched.first_name == "Boubacar"


def test_get_account_with_unknown_id_raises_not_found(domain_service):
    actor = MockActor()
    account_service = domain_service.account.account_service

    with pytest.raises(AccountNotFoundError):
        account_service.get_account(actor, uuid4())


def test_update_account_modifies_profile_fields(domain_service):
    actor = MockActor()
    account_service = domain_service.account.account_service

    created = account_service.create_account(
        actor,
        first_name="Cherif",
        last_name="Haïdara",
    ).data

    updated = account_service.update_account(
        actor,
        created.id,
        first_name="Cherif Ousmane",
    ).data

    assert updated.first_name == "Cherif Ousmane"
    assert updated.last_name == "Haïdara"


def test_update_account_with_unknown_id_raises_not_found(domain_service):
    actor = MockActor()
    account_service = domain_service.account.account_service

    with pytest.raises(AccountNotFoundError):
        account_service.update_account(actor, uuid4(), first_name="Test")


def test_list_accounts_returns_matching_results(domain_service):
    actor = MockActor()
    account_service = domain_service.account.account_service

    acc = account_service.create_account(
        actor,
        first_name="UniqueFirstName",
        last_name="UniqueLastName",
    ).data

    results = account_service.list_accounts(
        actor, AccountFilter(search="UniqueFirstName")
    ).data
    assert any(a.id == acc.id for a in results)


def test_assign_role_to_account_adds_role(domain_service):
    actor = MockActor()
    account_service = domain_service.account.account_service
    role_service = domain_service.account.role_service

    acc = account_service.create_account(
        actor, first_name="Role", last_name="User"
    ).data
    role = role_service.create_role(actor, name="assignee_role").data

    with_role = account_service.assign_role_to_account(actor, acc.id, role.id).data
    assert role.id in with_role.role_ids


def test_assign_unknown_role_raises_role_not_found(domain_service):
    actor = MockActor()
    account_service = domain_service.account.account_service

    acc = account_service.create_account(
        actor, first_name="Role2", last_name="User"
    ).data

    with pytest.raises(RoleNotFoundError):
        account_service.assign_role_to_account(actor, acc.id, uuid4())


def test_remove_role_from_account_removes_role(domain_service):
    actor = MockActor()
    account_service = domain_service.account.account_service
    role_service = domain_service.account.role_service

    acc = account_service.create_account(
        actor, first_name="RemoveRole", last_name="User"
    ).data
    role = role_service.create_role(actor, name="revokee_role").data
    account_service.assign_role_to_account(actor, acc.id, role.id)

    without_role = account_service.remove_role_from_account(actor, acc.id, role.id).data
    assert role.id not in without_role.role_ids


def test_delete_account_removes_record(domain_service):
    actor = MockActor()
    account_service = domain_service.account.account_service

    acc = account_service.create_account(
        actor, first_name="Delete", last_name="Me"
    ).data
    account_service.delete_account(actor, acc.id)

    with pytest.raises(AccountNotFoundError):
        account_service.get_account(actor, acc.id)


def test_delete_unknown_account_raises_not_found(domain_service):
    actor = MockActor()
    account_service = domain_service.account.account_service

    with pytest.raises(AccountNotFoundError):
        account_service.delete_account(actor, uuid4())
