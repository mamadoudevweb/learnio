from src.domains.account.subs.access_controle.routes.v1.permission_routes import (
    permission_bp,
)
from src.domains.account.subs.access_controle.routes.v1.role_routes import (
    JwtActor,
    role_bp,
)

__all__ = ["JwtActor", "permission_bp", "role_bp"]
