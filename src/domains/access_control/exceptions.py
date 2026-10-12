from src.core.errors import ConflictError, NotFoundError


class RoleNotFoundError(NotFoundError):
    code = "ACCESS_CONTROL_ROLE_NOT_FOUND"


class RoleAlreadyExistsError(ConflictError):
    code = "ACCESS_CONTROL_ROLE_ALREADY_EXISTS"


class PermissionNotFoundError(NotFoundError):
    code = "ACCESS_CONTROL_PERMISSION_NOT_FOUND"


class PermissionAlreadyExistsError(ConflictError):
    code = "ACCESS_CONTROL_PERMISSION_ALREADY_EXISTS"
