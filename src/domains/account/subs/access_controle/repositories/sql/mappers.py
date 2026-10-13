from src.domains.account.subs.access_controle.entities.permission import Permission
from src.domains.account.subs.access_controle.entities.role import Role
from src.domains.account.subs.access_controle.repositories.sql.orms import (
    PermissionOrm,
    RoleOrm,
)


class RoleMapper:
    @staticmethod
    def to_entity(orm_obj: RoleOrm) -> Role:
        perm_ids = (
            [p.id for p in orm_obj.permissions]
            if getattr(orm_obj, "permissions", None)
            else []
        )
        return Role(
            id=orm_obj.id,
            name=orm_obj.name,
            description=orm_obj.description,
            permission_ids=perm_ids,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
        )

    @staticmethod
    def to_orm(entity: Role) -> RoleOrm:
        return RoleOrm(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class PermissionMapper:
    @staticmethod
    def to_entity(orm_obj: PermissionOrm) -> Permission:
        return Permission(
            id=orm_obj.id,
            domain=orm_obj.domain,
            resource=orm_obj.resource,
            action=orm_obj.action,
            created_at=orm_obj.created_at,
            updated_at=orm_obj.updated_at,
        )

    @staticmethod
    def to_orm(entity: Permission) -> PermissionOrm:
        return PermissionOrm(
            id=entity.id,
            domain=entity.domain,
            resource=entity.resource,
            action=entity.action,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
