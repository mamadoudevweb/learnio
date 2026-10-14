import hashlib
import secrets
from datetime import date, timedelta
from typing import Any

from werkzeug.security import check_password_hash, generate_password_hash

from src.core.email import ConsoleEmailSender, EmailSender
from src.core.entities import ServiceResult, utc_now
from src.core.services import BaseService
from src.domains.account.entities.account import Account
from src.domains.account.exceptions import AccountInactiveError
from src.domains.account.subs.auth.entities.credential import Credential
from src.domains.account.subs.auth.entities.credential_reset import CredentialReset
from src.domains.account.subs.auth.entities.session import Session
from src.domains.account.subs.auth.exceptions import (
    CredentialNotFoundError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    ResetTokenExpiredOrInvalidError,
)
from src.domains.account.subs.auth.repositories.filters import (
    CredentialFilter,
    CredentialResetFilter,
    SessionFilter,
)


class AuthenticationService(BaseService):
    """Service d'authentification, de gestion de session et de réinitialisation de mot de passe."""

    def __init__(
        self,
        uow_factory: Any,
        *,
        email_sender: EmailSender | None = None,
        sender: EmailSender | None = None,
        reset_token_expire_minutes: int = 15,
    ) -> None:
        super().__init__(uow_factory)
        self._email_sender = email_sender or sender or ConsoleEmailSender()
        self._reset_token_expire_minutes = reset_token_expire_minutes

    @property
    def email_sender(self) -> EmailSender:
        """Expéditeur d'emails utilisé par le service."""
        return self._email_sender

    @property
    def reset_token_expire_minutes(self) -> int:
        """Durée de validité des jetons de réinitialisation en minutes."""
        return self._reset_token_expire_minutes

    def register(
        self,
        *,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        birth_date: date | None = None,
    ) -> ServiceResult[dict[str, Any]]:
        """Inscrit un nouvel utilisateur (création de compte + credential)."""
        clean_email = email.strip().lower()
        with self._uow_factory() as uow:
            cred_repo = uow.get_repository("CredentialRepository")
            acc_repo = uow.get_repository("AccountRepository")

            existing_cred = cred_repo.get(CredentialFilter(email=clean_email))
            if existing_cred:
                raise EmailAlreadyExistsError(
                    f"L'adresse email '{email}' est déjà utilisée."
                )

            account = Account.create(
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
            )
            acc_repo.add(account)
            uow.track(account)

            password_hash = generate_password_hash(password)
            credential = Credential.create(
                account_id=account.id,
                email=clean_email,
                password_hash=password_hash,
            )
            cred_repo.add(credential)
            uow.track(credential)

            return ServiceResult(data={"account": account, "credential": credential})

    def login(
        self,
        *,
        email: str,
        password: str,
        ip: str | None = None,
        user_agent: str | None = None,
    ) -> ServiceResult[dict[str, Any]]:
        """Authentifie un utilisateur et génère une session et un jeton."""
        clean_email = email.strip().lower()
        with self._uow_factory() as uow:
            cred_repo = uow.get_repository("CredentialRepository")
            acc_repo = uow.get_repository("AccountRepository")
            sess_repo = uow.get_repository("SessionRepository")
            role_repo = uow.get_repository("RoleRepository")
            perm_repo = uow.get_repository("PermissionRepository")

            cred = cred_repo.get(CredentialFilter(email=clean_email))
            if not cred or not check_password_hash(cred.password_hash, password):
                raise InvalidCredentialsError("Identifiants de connexion invalides.")

            account = acc_repo.get(cred.account_id)
            if not account or not account.active:
                raise AccountInactiveError("Ce compte utilisateur est désactivé.")

            raw_token = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
            expires_at = utc_now() + timedelta(days=7)

            session = Session.create(
                account_id=account.id,
                token_hash=token_hash,
                expires_at=expires_at,
                ip=ip,
                user_agent=user_agent,
            )
            sess_repo.add(session)
            uow.track(session)

            # Résolution des permissions associées aux rôles
            permissions: list[str] = []
            for role_id in account.role_ids:
                role = role_repo.get(role_id)
                if role:
                    for perm_id in role.permission_ids:
                        perm = perm_repo.get(perm_id)
                        if perm and perm.triplet not in permissions:
                            permissions.append(perm.triplet)

            return ServiceResult(
                data={
                    "token": raw_token,
                    "account": account,
                    "permissions": permissions,
                }
            )

    def validate_session(self, token: str) -> ServiceResult[Account]:
        """Vérifie qu'un jeton correspond à une session active et retourne le compte."""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        with self._uow_factory() as uow:
            sess_repo = uow.get_repository("SessionRepository")
            acc_repo = uow.get_repository("AccountRepository")

            session = sess_repo.get(
                SessionFilter(token_hash=token_hash, is_active=True)
            )
            if not session or not session.is_active():
                raise InvalidCredentialsError("Session invalide ou expirée.")

            account = acc_repo.get(session.account_id)
            if not account or not account.active:
                raise AccountInactiveError("Ce compte est désactivé.")

            return ServiceResult(data=account)

    def request_password_reset(self, email: str) -> ServiceResult[dict[str, Any]]:
        """Génère un jeton de réinitialisation de mot de passe à usage unique et l'envoie par email."""
        clean_email = email.strip().lower()
        with self._uow_factory() as uow:
            cred_repo = uow.get_repository("CredentialRepository")
            reset_repo = uow.get_repository("CredentialResetRepository")

            cred = cred_repo.get(CredentialFilter(email=clean_email))
            if not cred:
                raise CredentialNotFoundError(f"Aucun compte associé à '{email}'.")

            raw_token = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
            expires_at = utc_now() + timedelta(minutes=self._reset_token_expire_minutes)

            reset = CredentialReset.create(
                credential_id=cred.id,
                token_hash=token_hash,
                expires_at=expires_at,
                email=clean_email,
                token=raw_token,
            )
            reset_repo.add(reset)
            uow.track(reset)

        return ServiceResult(
            data={"message": "Un email de réinitialisation a été envoyé."}
        )

    def validate_reset_token(self, token: str) -> ServiceResult[dict[str, Any]]:
        """Vérifie la validité d'un jeton de réinitialisation."""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        with self._uow_factory() as uow:
            reset_repo = uow.get_repository("CredentialResetRepository")
            reset = reset_repo.get(
                CredentialResetFilter(token_hash=token_hash, is_valid=True)
            )
            if not reset or not reset.is_valid():
                raise ResetTokenExpiredOrInvalidError(
                    "Jeton de réinitialisation invalide ou expiré."
                )
            return ServiceResult(data={"valid": True})

    def reset_password(self, token: str, new_password: str) -> ServiceResult[None]:
        """Consomme le jeton et met à jour le mot de passe."""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        with self._uow_factory() as uow:
            reset_repo = uow.get_repository("CredentialResetRepository")
            cred_repo = uow.get_repository("CredentialRepository")
            sess_repo = uow.get_repository("SessionRepository")

            reset = reset_repo.get(
                CredentialResetFilter(token_hash=token_hash, is_valid=True)
            )
            if not reset or not reset.is_valid():
                raise ResetTokenExpiredOrInvalidError(
                    "Jeton de réinitialisation invalide ou expiré."
                )

            cred = cred_repo.get(reset.credential_id)
            if not cred:
                raise CredentialNotFoundError("Identifiant introuvable.")

            new_password_hash = generate_password_hash(new_password)
            cred.change_password(new_password_hash)
            cred_repo.update(cred)
            uow.track(cred)

            reset.consume()
            reset_repo.update(reset)
            uow.track(reset)

            # Révocation de toutes les sessions actives de ce compte
            active_sessions = sess_repo.list(
                SessionFilter(account_id=cred.account_id, is_active=True)
            )
            for sess in active_sessions:
                sess.revoke()
                sess_repo.update(sess)
                uow.track(sess)

            return ServiceResult(data=None)

    def revoke_session(self, token: str) -> ServiceResult[None]:
        """Déconnecte une session utilisateur."""
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        with self._uow_factory() as uow:
            sess_repo = uow.get_repository("SessionRepository")
            session = sess_repo.get(SessionFilter(token_hash=token_hash))
            if session:
                session.revoke()
                sess_repo.update(session)
                uow.track(session)
            return ServiceResult(data=None)
