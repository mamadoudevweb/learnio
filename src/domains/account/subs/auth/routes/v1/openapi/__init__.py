"""Auth OpenAPI specifications."""

from src.domains.account.subs.auth.routes.v1.openapi.auth_openapi import (
    COMPONENTS as AUTH_COMPONENTS,
)
from src.domains.account.subs.auth.routes.v1.openapi.auth_openapi import (
    PATHS as AUTH_PATHS,
)
from src.domains.account.subs.auth.routes.v1.openapi.auth_openapi import (
    TAGS as AUTH_TAGS,
)

TAGS = AUTH_TAGS
PATHS = AUTH_PATHS
COMPONENTS = AUTH_COMPONENTS

__all__ = ["COMPONENTS", "PATHS", "TAGS"]
