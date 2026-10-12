"""Account entity — belongs to the ``account`` bounded-context."""

from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import Field

from src.core.entities import BaseEntity, EntityId, utc_now
from src.domains.account.entities.events import (
    AccountCreated,
    AccountRoleAssigned,
    AccountRoleRemoved,
    AccountUpdated,
)


class Account(BaseEntity[EntityId]):
    """Profil utilisateur principal (données d'identité/compte)."""

    first_name: str
    last_name: str
    birth_date: date | None = None
    active: bool = True
    role_ids: list[UUID] = Field(default_factory=list)

    @classmethod
    def create(
        cls,
        *,
        first_name: str,
        last_name: str,
        birth_date: date | None = None,
        active: bool = True,
        role_ids: list[UUID] | None = None,
    ) -> Account:
        account = cls(
            first_name=first_name.strip(),
            last_name=last_name.strip(),
            birth_date=birth_date,
            active=active,
            role_ids=list(role_ids) if role_ids else [],
        )
        account.register_event(
            AccountCreated(account_id=account.id, first_name=account.first_name)
        )
        return account

    def update_profile(
        self,
        *,
        first_name: str | None = None,
        last_name: str | None = None,
        birth_date: date | None = None,
        active: bool | None = None,
    ) -> None:
        if first_name is not None:
            self.first_name = first_name.strip()
        if last_name is not None:
            self.last_name = last_name.strip()
        if birth_date is not None:
            self.birth_date = birth_date
        if active is not None:
            self.active = active
        self.updated_at = utc_now()
        self.register_event(AccountUpdated(account_id=self.id))

    def assign_role(self, role_id: UUID) -> None:
        if role_id not in self.role_ids:
            self.role_ids.append(role_id)
            self.updated_at = utc_now()
            self.register_event(
                AccountRoleAssigned(account_id=self.id, role_id=role_id)
            )

    def remove_role(self, role_id: UUID) -> None:
        if role_id in self.role_ids:
            self.role_ids.remove(role_id)
            self.updated_at = utc_now()
            self.register_event(AccountRoleRemoved(account_id=self.id, role_id=role_id))
