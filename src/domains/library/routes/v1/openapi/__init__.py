"""Library OpenAPI specifications."""

from src.domains.library.routes.v1.openapi.document_openapi import (
    COMPONENTS as DOCUMENT_COMPONENTS,
)
from src.domains.library.routes.v1.openapi.document_openapi import (
    PATHS as DOCUMENT_PATHS,
)
from src.domains.library.routes.v1.openapi.document_openapi import (
    TAGS as DOCUMENT_TAGS,
)

TAGS = DOCUMENT_TAGS
PATHS = DOCUMENT_PATHS
COMPONENTS = DOCUMENT_COMPONENTS

__all__ = ["COMPONENTS", "PATHS", "TAGS"]
