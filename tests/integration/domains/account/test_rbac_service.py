from uuid import uuid4

import pytest

from src.domains.account.rbac.exceptions import (
    PermissionNotFoundError,
    RoleAlreadyExistsError,
    RoleNotFoundError,
)
from src.domains.account.rbac.repositories.filters import (
    PermissionFilter,
    RoleFilter,
)


class MockActor:
    def has_permission(self, permission: str) -> bool:
        return True


def test_create_role_persists_role(domain_service):
    actor = MockActor()
    role_service = domain_service.account.role_service

    role = role_service.create_role(
        actor,
        name="archivist",
        description="Library archivist",
    ).data

    assert role.id is not None
    assert role.name == "archivist"


def test_create_duplicate_role_raises_already_exists(domain_service):
    actor = MockActor()
    role_service = domain_service.account.role_service
    role_service.create_role(actor, name="dup_role")

    with pytest.raises(RoleAlreadyExistsError):
        role_service.create_role(actor, name="dup_role")


def test_get_role_by_id_returns_role(domain_service):
    actor = MockActor()
    role_service = domain_service.account.role_service

    created = role_service.create_role(actor, name="viewer").data
    fetched = role_service.get_role(actor, created.id).data

    assert fetched.id == created.id
    assert fetched.name == "viewer"


def test_get_unknown_role_raises_role_not_found(domain_service):
    actor = MockActor()
    role_service = domain_service.account.role_service

    with pytest.raises(RoleNotFoundError):
        role_service.get_role(actor, uuid4())


def test_list_roles_with_filter_returns_matches(domain_service):
    actor = MockActor()
    role_service = domain_service.account.role_service

    created = role_service.create_role(actor, name="filter_target").data
    matches = role_service.list_roles(actor, RoleFilter(name="filter_target")).data

    assert len(matches) == 1
    assert matches[0].id == created.id


def test_assign_permission_to_role_updates_role(domain_service):
    actor = MockActor()
    role_service = domain_service.account.role_service
    perm_service = domain_service.account.permission_service

    perm = perm_service.get_or_create(
        actor, domain="curriculum", resource="chapter", action="read"
    ).data
    role = role_service.create_role(actor, name="assigned_role").data

    updated = role_service.assign_permission_to_role(actor, role.id, perm.id).data
    assert perm.id in updated.permission_ids


def test_assign_unknown_permission_raises_permission_not_found(domain_service):
    actor = MockActor()
    role_service = domain_service.account.role_service

    role = role_service.create_role(actor, name="target_role").data

    with pytest.raises(PermissionNotFoundError):
        role_service.assign_permission_to_role(actor, role.id, uuid4())


def test_revoke_permission_from_role_updates_role(domain_service):
    actor = MockActor()
    role_service = domain_service.account.role_service
    perm_service = domain_service.account.permission_service

    perm = perm_service.get_or_create(
        actor, domain="curriculum", resource="chapter", action="delete"
    ).data
    role = role_service.create_role(
        actor, name="revoked_role", permission_ids=[perm.id]
    ).data

    updated = role_service.revoke_permission_from_role(actor, role.id, perm.id).data
    assert perm.id not in updated.permission_ids


def test_delete_role_removes_role(domain_service):
    actor = MockActor()
    role_service = domain_service.account.role_service

    role = role_service.create_role(actor, name="to_delete").data
    role_service.delete_role(actor, role.id)

    with pytest.raises(RoleNotFoundError):
        role_service.get_role(actor, role.id)


def test_delete_unknown_role_raises_not_found(domain_service):
    actor = MockActor()
    role_service = domain_service.account.role_service

    with pytest.raises(RoleNotFoundError):
        role_service.delete_role(actor, uuid4())


def test_get_or_create_permission_creates_new(domain_service):
    actor = MockActor()
    perm_service = domain_service.account.permission_service

    perm = perm_service.get_or_create(
        actor, domain="finance", resource="invoice", action="view"
    ).data
    assert perm.triplet == "finance:invoice:view"


def test_get_or_create_permission_returns_existing(domain_service):
    actor = MockActor()
    perm_service = domain_service.account.permission_service

    p1 = perm_service.get_or_create(
        actor, domain="finance", resource="invoice", action="create"
    ).data
    p2 = perm_service.get_or_create(
        actor, domain="finance", resource="invoice", action="create"
    ).data
    assert p1.id == p2.id


def test_get_permission_by_id_returns_permission(domain_service):
    actor = MockActor()
    perm_service = domain_service.account.permission_service

    created = perm_service.get_or_create(
        actor, domain="hr", resource="employee", action="read"
    ).data
    fetched = perm_service.get_permission(actor, created.id).data
    assert fetched.id == created.id


def test_get_unknown_permission_raises_not_found(domain_service):
    actor = MockActor()
    perm_service = domain_service.account.permission_service

    with pytest.raises(PermissionNotFoundError):
        perm_service.get_permission(actor, uuid4())


def test_list_permissions_returns_matches(domain_service):
    actor = MockActor()
    perm_service = domain_service.account.permission_service

    created = perm_service.get_or_create(
        actor, domain="audit", resource="log", action="read"
    ).data
    all_perms = perm_service.list_permissions(
        actor, PermissionFilter(domain="audit")
    ).data
    assert any(p.id == created.id for p in all_perms)


def test_delete_permission_removes_record(domain_service):
    actor = MockActor()
    perm_service = domain_service.account.permission_service

    perm = perm_service.get_or_create(
        actor, domain="temp", resource="record", action="drop"
    ).data
    perm_service.delete_permission(actor, perm.id)

    with pytest.raises(PermissionNotFoundError):
        perm_service.get_permission(actor, perm.id)
