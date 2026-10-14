from datetime import date
from uuid import UUID

from src.core.entities import ServiceResult
from src.core.services import BaseService, SupportsPermissionCheck
from src.domains.account.entities.account import Account
from src.domains.account.exceptions import AccountNotFoundError, RoleNotFoundError
from src.domains.account.repositories.filters import AccountFilter


class AccountService(BaseService):
    """Service de gestion des profils et comptes utilisateurs."""

    def get_account(
        self, actor: SupportsPermissionCheck, account_id: UUID
    ) -> ServiceResult[Account]:
        self._authorize(actor, "account", "account", "read")
        with self._uow_factory() as uow:
            repo = uow.get_repository("AccountRepository")
            account = repo.get(account_id)
            if not account:
                raise AccountNotFoundError(f"Compte {account_id} introuvable")
            return ServiceResult(data=account)

    def list_accounts(
        self, actor: SupportsPermissionCheck, filter: AccountFilter
    ) -> ServiceResult[list[Account]]:
        self._authorize(actor, "account", "account", "read")
        with self._uow_factory() as uow:
            repo = uow.get_repository("AccountRepository")
            accounts = repo.list(filter)
            count = repo.count(filter)
            return ServiceResult(data=accounts, meta={"total": count})

    def create_account(
        self,
        actor: SupportsPermissionCheck,
        *,
        first_name: str,
        last_name: str,
        birth_date: date | None = None,
        active: bool = True,
        role_ids: list[UUID] | None = None,
    ) -> ServiceResult[Account]:
        self._authorize(actor, "account", "account", "create")
        account = Account.create(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            active=active,
            role_ids=role_ids,
        )
        with self._uow_factory() as uow:
            repo = uow.get_repository("AccountRepository")
            repo.add(account)
            uow.track(account)
            return ServiceResult(data=account)

    def update_account(
        self,
        actor: SupportsPermissionCheck,
        account_id: UUID,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        birth_date: date | None = None,
        active: bool | None = None,
    ) -> ServiceResult[Account]:
        self._authorize(actor, "account", "account", "update")
        with self._uow_factory() as uow:
            repo = uow.get_repository("AccountRepository")
            account = repo.get(account_id)
            if not account:
                raise AccountNotFoundError(f"Compte {account_id} introuvable")
            account.update_profile(
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                active=active,
            )
            repo.update(account)
            uow.track(account)
            return ServiceResult(data=account)

    def assign_role_to_account(
        self, actor: SupportsPermissionCheck, account_id: UUID, role_id: UUID
    ) -> ServiceResult[Account]:
        self._authorize(actor, "account", "account", "update")
        with self._uow_factory() as uow:
            account_repo = uow.get_repository("AccountRepository")
            role_repo = uow.get_repository("RoleRepository")
            account = account_repo.get(account_id)
            if not account:
                raise AccountNotFoundError(f"Compte {account_id} introuvable")
            role = role_repo.get(role_id)
            if not role:
                raise RoleNotFoundError(f"Rôle {role_id} introuvable")
            account.assign_role(role_id)
            account_repo.update(account)
            uow.track(account)
            return ServiceResult(data=account)

    def remove_role_from_account(
        self, actor: SupportsPermissionCheck, account_id: UUID, role_id: UUID
    ) -> ServiceResult[Account]:
        self._authorize(actor, "account", "account", "update")
        with self._uow_factory() as uow:
            account_repo = uow.get_repository("AccountRepository")
            account = account_repo.get(account_id)
            if not account:
                raise AccountNotFoundError(f"Compte {account_id} introuvable")
            account.remove_role(role_id)
            account_repo.update(account)
            uow.track(account)
            return ServiceResult(data=account)

    def delete_account(
        self, actor: SupportsPermissionCheck, account_id: UUID
    ) -> ServiceResult[None]:
        self._authorize(actor, "account", "account", "delete")
        with self._uow_factory() as uow:
            repo = uow.get_repository("AccountRepository")
            account = repo.get(account_id)
            if not account:
                raise AccountNotFoundError(f"Compte {account_id} introuvable")
            repo.delete(account.id)
            return ServiceResult(data=None)
