"""RBAC OpenAPI specifications."""

from src.domains.account.subs.access_controle.routes.v1.openapi.permission_openapi import (
    COMPONENTS as PERMISSION_COMPONENTS,
)
from src.domains.account.subs.access_controle.routes.v1.openapi.permission_openapi import (
    PATHS as PERMISSION_PATHS,
)
from src.domains.account.subs.access_controle.routes.v1.openapi.permission_openapi import (
    TAGS as PERMISSION_TAGS,
)
from src.domains.account.subs.access_controle.routes.v1.openapi.role_openapi import (
    COMPONENTS as ROLE_COMPONENTS,
)
from src.domains.account.subs.access_controle.routes.v1.openapi.role_openapi import (
    PATHS as ROLE_PATHS,
)
from src.domains.account.subs.access_controle.routes.v1.openapi.role_openapi import (
    TAGS as ROLE_TAGS,
)

TAGS = ROLE_TAGS + PERMISSION_TAGS
PATHS = {**ROLE_PATHS, **PERMISSION_PATHS}
COMPONENTS = {
    "schemas": {
        **ROLE_COMPONENTS.get("schemas", {}),
        **PERMISSION_COMPONENTS.get("schemas", {}),
    }
}

__all__ = ["COMPONENTS", "PATHS", "TAGS"]
