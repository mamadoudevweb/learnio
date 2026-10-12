from src.domains.account.entities.account import Account
from src.domains.account.repositories.sql.orms.account_orm import AccountOrm


class AccountMapper:
    @staticmethod
    def to_entity(orm_obj: AccountOrm) -> Account:
        role_ids = (
            [r.id for r in orm_obj.roles] if getattr(orm_obj, "roles", None) else []
        )
        return Account(
            id=orm_obj.id,
            first_name=orm_obj.first_name,
            last_name=orm_obj.last_name,
            birth_date=orm_obj.birth_date,
            active=orm_obj.active,
            role_ids=role_ids,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
        )

    @staticmethod
    def to_orm(entity: Account) -> AccountOrm:
        return AccountOrm(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            birth_date=entity.birth_date,
            active=entity.active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
