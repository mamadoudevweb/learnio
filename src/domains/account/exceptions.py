from src.core.errors import ConflictError, NotFoundError


class AccountNotFoundError(NotFoundError):
    code = "ACCOUNT_NOT_FOUND"


class AccountInactiveError(NotFoundError):
    code = "ACCOUNT_INACTIVE"


class RoleNotFoundError(NotFoundError):
    """Raised by AccountService when assigning a role that does not exist."""
    code = "ACCOUNT_ROLE_NOT_FOUND"
