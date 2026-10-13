from dataclasses import dataclass

from src.domains.account.services.account_service import AccountService
from src.domains.account.subs.access_controle.services.permission_service import (
    PermissionService,
)
from src.domains.account.subs.access_controle.services.role_service import RoleService
from src.domains.account.subs.auth.services.authentication_service import (
    AuthenticationService,
)


@dataclass(kw_only=True)
class AccountDomainService:
    """Façade du domaine Account agrégeant ses services et sous-domaines (auth, access_controle)."""

    account_service: AccountService
    authentication_service: AuthenticationService
    role_service: RoleService
    permission_service: PermissionService

    @property
    def auth_service(self) -> AuthenticationService:
        return self.authentication_service
