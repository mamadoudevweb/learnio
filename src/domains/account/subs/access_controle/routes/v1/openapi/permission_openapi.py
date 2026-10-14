"""OpenAPI 3.0 specification for Permission endpoints."""

from typing import Any

TAGS: list[dict[str, Any]] = [
    {
        "name": "Permissions",
        "description": "System access control permissions defined by domain:resource:action triplets",
    }
]

COMPONENTS: dict[str, Any] = {
    "schemas": {
        "Permission": {
            "type": "object",
            "required": [
                "id",
                "domain",
                "resource",
                "action",
                "createdAt",
                "updatedAt",
            ],
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Permission unique identifier",
                    "example": "123e4567-e89b-12d3-a456-426614174000",
                },
                "domain": {
                    "type": "string",
                    "description": "Target domain context (e.g., account, curriculum, library)",
                    "example": "curriculum",
                },
                "resource": {
                    "type": "string",
                    "description": "Target resource entity (e.g., subject, chapter, lesson, document)",
                    "example": "lesson",
                },
                "action": {
                    "type": "string",
                    "description": "Action capability (e.g., create, read, update, delete)",
                    "example": "read",
                },
                "createdAt": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Creation timestamp in UTC",
                    "example": "2026-10-12T15:00:00Z",
                },
                "updatedAt": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Last update timestamp in UTC",
                    "example": "2026-10-12T15:00:00Z",
                },
            },
        },
        "PermissionCreate": {
            "type": "object",
            "required": ["domain", "resource", "action"],
            "properties": {
                "domain": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 50,
                    "description": "Domain name",
                    "example": "curriculum",
                },
                "resource": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 50,
                    "description": "Resource entity name",
                    "example": "lesson",
                },
                "action": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 50,
                    "description": "Action capability",
                    "example": "read",
                },
            },
        },
        "PermissionEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {"$ref": "#/components/schemas/Permission"},
                "meta": {"type": "object", "additionalProperties": True},
            },
        },
        "PermissionListEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/Permission"},
                },
                "meta": {
                    "type": "object",
                    "properties": {
                        "page": {"type": "integer", "example": 1},
                        "pageSize": {"type": "integer", "example": 20},
                        "total": {"type": "integer", "example": 14},
                    },
                },
            },
        },
    }
}

PATHS: dict[str, Any] = {
    "/api/v1/permissions": {
        "get": {
            "tags": ["Permissions"],
            "summary": "List all permissions",
            "description": "Retrieve a paginated list of system permissions, optionally filtered by domain, resource, or action.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "page",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "integer", "default": 1, "minimum": 1},
                    "description": "Page number for pagination",
                },
                {
                    "name": "pageSize",
                    "in": "query",
                    "required": False,
                    "schema": {
                        "type": "integer",
                        "default": 20,
                        "minimum": 1,
                        "maximum": 100,
                    },
                    "description": "Number of items per page",
                },
                {
                    "name": "domain",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string"},
                    "description": "Filter by target domain",
                },
                {
                    "name": "resource",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string"},
                    "description": "Filter by target resource entity",
                },
                {
                    "name": "action",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string"},
                    "description": "Filter by action capability",
                },
            ],
            "responses": {
                "200": {
                    "description": "List of permissions retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/PermissionListEnvelope"
                            }
                        }
                    },
                },
                "401": {
                    "description": "Authentication credentials missing or invalid",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        },
        "post": {
            "tags": ["Permissions"],
            "summary": "Create or get permission",
            "description": "Register a new permission triplet or retrieve existing one if already declared.",
            "security": [{"BearerAuth": []}],
            "requestBody": {
                "required": True,
                "description": "Permission triplet payload",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/PermissionCreate"}
                    }
                },
            },
            "responses": {
                "201": {
                    "description": "Permission created or retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/PermissionEnvelope"
                            }
                        }
                    },
                },
                "401": {
                    "description": "Authentication credentials missing or invalid",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
                "422": {
                    "description": "Validation error in request payload",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        },
    },
    "/api/v1/permissions/{permissionId}": {
        "get": {
            "tags": ["Permissions"],
            "summary": "Get permission by ID",
            "description": "Retrieve details of a single permission triplet by its unique ID.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "permissionId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the permission",
                }
            ],
            "responses": {
                "200": {
                    "description": "Permission details retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/PermissionEnvelope"
                            }
                        }
                    },
                },
                "401": {
                    "description": "Authentication credentials missing or invalid",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
                "404": {
                    "description": "Permission not found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        },
        "delete": {
            "tags": ["Permissions"],
            "summary": "Delete a permission",
            "description": "Permanently remove a permission triplet from the system.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "permissionId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the permission to delete",
                }
            ],
            "responses": {
                "200": {
                    "description": "Permission deleted successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/EmptyEnvelope"}
                        }
                    },
                },
                "401": {
                    "description": "Authentication credentials missing or invalid",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
                "404": {
                    "description": "Permission not found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        },
    },
}
