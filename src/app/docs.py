"""OpenAPI documentation composition root.

Wires all domain OpenAPI modules together into an OpenAPI 3.0 specification
and registers documentation endpoints (/api/v1/openapi.json, /api/v1/docs).
"""

from __future__ import annotations

import json
from typing import Any

from flask import Flask, Response

from src.domains.account.routes.v1.openapi import (
    COMPONENTS as ACCOUNT_COMPONENTS,
)
from src.domains.account.routes.v1.openapi import (
    PATHS as ACCOUNT_PATHS,
)
from src.domains.account.routes.v1.openapi import (
    TAGS as ACCOUNT_TAGS,
)
from src.domains.account.subs.access_controle.routes.v1.openapi import (
    COMPONENTS as RBAC_COMPONENTS,
)
from src.domains.account.subs.access_controle.routes.v1.openapi import (
    PATHS as RBAC_PATHS,
)
from src.domains.account.subs.access_controle.routes.v1.openapi import (
    TAGS as RBAC_TAGS,
)
from src.domains.account.subs.auth.routes.v1.openapi import (
    COMPONENTS as AUTH_COMPONENTS,
)
from src.domains.account.subs.auth.routes.v1.openapi import (
    PATHS as AUTH_PATHS,
)
from src.domains.account.subs.auth.routes.v1.openapi import (
    TAGS as AUTH_TAGS,
)
from src.domains.curriculum.routes.v1.openapi import (
    COMPONENTS as CURRICULUM_COMPONENTS,
)
from src.domains.curriculum.routes.v1.openapi import (
    PATHS as CURRICULUM_PATHS,
)
from src.domains.curriculum.routes.v1.openapi import (
    TAGS as CURRICULUM_TAGS,
)
from src.domains.library.routes.v1.openapi import (
    COMPONENTS as LIBRARY_COMPONENTS,
)
from src.domains.library.routes.v1.openapi import (
    PATHS as LIBRARY_PATHS,
)
from src.domains.library.routes.v1.openapi import (
    TAGS as LIBRARY_TAGS,
)

COMMON_COMPONENTS: dict[str, Any] = {
    "securitySchemes": {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT Bearer token obtained from /api/v1/auth/login",
        }
    },
    "schemas": {
        "EmptyEnvelope": {
            "type": "object",
            "required": ["success"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {"nullable": True, "example": None},
                "meta": {"type": "object", "additionalProperties": True},
            },
        },
        "ErrorDetail": {
            "type": "object",
            "required": ["code", "message"],
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Unique domain error code",
                    "example": "ACCOUNT_NOT_FOUND",
                },
                "message": {
                    "type": "string",
                    "description": "Human-readable description of the error",
                    "example": "The requested account does not exist.",
                },
                "details": {
                    "type": "object",
                    "description": "Optional validation or context details",
                    "additionalProperties": True,
                },
            },
        },
        "ErrorEnvelope": {
            "type": "object",
            "required": ["success", "error"],
            "properties": {
                "success": {"type": "boolean", "example": False},
                "error": {"$ref": "#/components/schemas/ErrorDetail"},
            },
        },
    },
}

HEALTH_PATHS: dict[str, Any] = {
    "/api/v1/health": {
        "get": {
            "tags": ["System"],
            "summary": "Health and liveness check",
            "description": "Lightweight unauthenticated liveness check for load balancers and orchestrators.",
            "security": [],
            "responses": {
                "200": {
                    "description": "Service is alive and healthy",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["status"],
                                "properties": {
                                    "status": {"type": "string", "example": "ok"}
                                },
                            }
                        }
                    },
                },
                "500": {
                    "description": "Service is unhealthy or internal server error",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        }
    }
}

SYSTEM_TAGS: list[dict[str, Any]] = [
    {"name": "System", "description": "Core system status and health endpoints"}
]


def build_openapi_spec() -> dict[str, Any]:
    """Assemble and return the complete OpenAPI 3.0 specification dictionary."""
    all_tags = (
        SYSTEM_TAGS
        + AUTH_TAGS
        + ACCOUNT_TAGS
        + RBAC_TAGS
        + CURRICULUM_TAGS
        + LIBRARY_TAGS
    )

    all_paths: dict[str, Any] = {}
    all_paths.update(HEALTH_PATHS)
    all_paths.update(AUTH_PATHS)
    all_paths.update(ACCOUNT_PATHS)
    all_paths.update(RBAC_PATHS)
    all_paths.update(CURRICULUM_PATHS)
    all_paths.update(LIBRARY_PATHS)

    all_schemas: dict[str, Any] = {}
    all_schemas.update(COMMON_COMPONENTS.get("schemas", {}))
    all_schemas.update(AUTH_COMPONENTS.get("schemas", {}))
    all_schemas.update(ACCOUNT_COMPONENTS.get("schemas", {}))
    all_schemas.update(RBAC_COMPONENTS.get("schemas", {}))
    all_schemas.update(CURRICULUM_COMPONENTS.get("schemas", {}))
    all_schemas.update(LIBRARY_COMPONENTS.get("schemas", {}))

    return {
        "openapi": "3.0.3",
        "info": {
            "title": "Learnio API",
            "version": "1.0.0",
            "description": (
                "RESTful backend API for Learnio — educational curriculum, "
                "revision library, and account management platform."
            ),
            "contact": {
                "name": "Learnio Engineering Team",
                "email": "support@learnio.com",
            },
            "license": {
                "name": "Proprietary",
            },
        },
        "servers": [
            {
                "url": "https://api.learnio.app",
                "description": "Production API server",
            },
            {
                "url": "http://localhost:5000",
                "description": "Local development server",
            },
        ],
        "security": [{"BearerAuth": []}],
        "tags": all_tags,
        "paths": all_paths,
        "components": {
            "securitySchemes": COMMON_COMPONENTS["securitySchemes"],
            "schemas": all_schemas,
        },
    }


SWAGGER_UI_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Learnio API Documentation</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" />
  <link rel="icon" type="image/png" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/favicon-32x32.png" />
  <style>
    body { margin: 0; background: #fafafa; }
    .topbar { display: none; }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.onload = function() {
      SwaggerUIBundle({
        url: "/api/v1/openapi.json",
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout"
      });
    };
  </script>
</body>
</html>
"""


def register_docs(app: Flask) -> None:
    """Register OpenAPI specification JSON and Swagger UI documentation routes."""

    @app.get("/api/v1/openapi.json")
    def openapi_json() -> Response:
        """Serve the OpenAPI 3.0 specification as JSON."""
        spec = build_openapi_spec()
        return Response(
            json.dumps(spec, indent=2),
            mimetype="application/json",
            status=200,
        )

    @app.get("/api/v1/docs")
    def swagger_ui() -> tuple[str, int, dict[str, str]]:
        """Serve the interactive Swagger UI page."""
        return SWAGGER_UI_HTML, 200, {"Content-Type": "text/html; charset=utf-8"}
