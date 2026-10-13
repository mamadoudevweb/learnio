from datetime import UTC, datetime

from src.domains.account.subs.auth.entities.credential import Credential
from src.domains.account.subs.auth.entities.credential_reset import CredentialReset
from src.domains.account.subs.auth.entities.session import Session
from src.domains.account.subs.auth.repositories.sql.orms import (
    CredentialOrm,
    CredentialResetOrm,
    SessionOrm,
)


def _to_utc(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    return dt if dt.tzinfo is not None else dt.replace(tzinfo=UTC)


class CredentialMapper:
    @staticmethod
    def to_entity(orm_obj: CredentialOrm) -> Credential:
        return Credential(
            id=orm_obj.id,
            account_id=orm_obj.account_id,
            email=orm_obj.email,
            password_hash=orm_obj.password_hash,
            email_verified=orm_obj.email_verified,
            created_at=_to_utc(orm_obj.created_at),  # type: ignore[arg-type]
            updated_at=_to_utc(orm_obj.updated_at),  # type: ignore[arg-type]
        )

    @staticmethod
    def to_orm(entity: Credential) -> CredentialOrm:
        return CredentialOrm(
            id=entity.id,
            account_id=entity.account_id,
            email=entity.email,
            password_hash=entity.password_hash,
            email_verified=entity.email_verified,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class SessionMapper:
    @staticmethod
    def to_entity(orm_obj: SessionOrm) -> Session:
        return Session(
            id=orm_obj.id,
            account_id=orm_obj.account_id,
            token_hash=orm_obj.token_hash,
            expires_at=_to_utc(orm_obj.expires_at),  # type: ignore[arg-type]
            ip=orm_obj.ip,
            user_agent=orm_obj.user_agent,
            revoked_at=_to_utc(orm_obj.revoked_at),
            created_at=_to_utc(orm_obj.created_at),  # type: ignore[arg-type]
            updated_at=_to_utc(orm_obj.updated_at),  # type: ignore[arg-type]
        )

    @staticmethod
    def to_orm(entity: Session) -> SessionOrm:
        return SessionOrm(
            id=entity.id,
            account_id=entity.account_id,
            ip=entity.ip,
            user_agent=entity.user_agent,
            token_hash=entity.token_hash,
            expires_at=entity.expires_at,
            revoked_at=entity.revoked_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class CredentialResetMapper:
    @staticmethod
    def to_entity(orm_obj: CredentialResetOrm) -> CredentialReset:
        return CredentialReset(
            id=orm_obj.id,
            credential_id=orm_obj.credential_id,
            token_hash=orm_obj.token_hash,
            expires_at=_to_utc(orm_obj.expires_at),  # type: ignore[arg-type]
            used_at=_to_utc(orm_obj.used_at),
            created_at=_to_utc(orm_obj.created_at),  # type: ignore[arg-type]
            updated_at=_to_utc(orm_obj.updated_at),  # type: ignore[arg-type]
        )

    @staticmethod
    def to_orm(entity: CredentialReset) -> CredentialResetOrm:
        return CredentialResetOrm(
            id=entity.id,
            credential_id=entity.credential_id,
            token_hash=entity.token_hash,
            expires_at=entity.expires_at,
            used_at=entity.used_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
