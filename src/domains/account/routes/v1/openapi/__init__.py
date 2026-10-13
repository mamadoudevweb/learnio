"""Account core OpenAPI specifications."""

from src.domains.account.routes.v1.openapi.account_openapi import (
    COMPONENTS as ACCOUNT_COMPONENTS,
)
from src.domains.account.routes.v1.openapi.account_openapi import (
    PATHS as ACCOUNT_PATHS,
)
from src.domains.account.routes.v1.openapi.account_openapi import (
    TAGS as ACCOUNT_TAGS,
)

TAGS = ACCOUNT_TAGS
PATHS = ACCOUNT_PATHS
COMPONENTS = ACCOUNT_COMPONENTS

__all__ = ["COMPONENTS", "PATHS", "TAGS"]
