"""OpenAPI 3.0 specification for Role endpoints."""

from typing import Any

TAGS: list[dict[str, Any]] = [
    {
        "name": "Roles",
        "description": "Role-based access control role definitions and permission mappings",
    }
]

COMPONENTS: dict[str, Any] = {
    "schemas": {
        "Role": {
            "type": "object",
            "required": ["id", "name", "permissionIds", "createdAt", "updatedAt"],
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Role unique identifier",
                    "example": "123e4567-e89b-12d3-a456-426614174000",
                },
                "name": {
                    "type": "string",
                    "description": "Unique role name",
                    "example": "teacher",
                },
                "description": {
                    "type": "string",
                    "nullable": True,
                    "description": "Role description",
                    "example": "Educational teacher role with curriculum management access",
                },
                "permissionIds": {
                    "type": "array",
                    "items": {"type": "string", "format": "uuid"},
                    "description": "List of permission UUIDs associated with this role",
                    "example": ["223e4567-e89b-12d3-a456-426614174000"],
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
        "RoleCreate": {
            "type": "object",
            "required": ["name"],
            "properties": {
                "name": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 100,
                    "description": "Role name",
                    "example": "teacher",
                },
                "description": {
                    "type": "string",
                    "nullable": True,
                    "description": "Description of the role",
                    "example": "Educational teacher role",
                },
                "permissionIds": {
                    "type": "array",
                    "items": {"type": "string", "format": "uuid"},
                    "description": "Initial permission IDs",
                },
            },
        },
        "RoleEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {"$ref": "#/components/schemas/Role"},
                "meta": {"type": "object", "additionalProperties": True},
            },
        },
        "RoleListEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/Role"},
                },
                "meta": {
                    "type": "object",
                    "properties": {
                        "page": {"type": "integer", "example": 1},
                        "pageSize": {"type": "integer", "example": 20},
                        "total": {"type": "integer", "example": 5},
                    },
                },
            },
        },
    }
}

PATHS: dict[str, Any] = {
    "/api/v1/roles": {
        "get": {
            "tags": ["Roles"],
            "summary": "List all roles",
            "description": "Retrieve a paginated list of defined system roles.",
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
                    "name": "name",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string"},
                    "description": "Filter by exact role name",
                },
            ],
            "responses": {
                "200": {
                    "description": "List of roles retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/RoleListEnvelope"}
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
            "tags": ["Roles"],
            "summary": "Create a role",
            "description": "Create a new RBAC role definition.",
            "security": [{"BearerAuth": []}],
            "requestBody": {
                "required": True,
                "description": "Role payload",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/RoleCreate"}
                    }
                },
            },
            "responses": {
                "201": {
                    "description": "Role created successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/RoleEnvelope"}
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
                "409": {
                    "description": "Role with this name already exists",
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
    "/api/v1/roles/{roleId}": {
        "get": {
            "tags": ["Roles"],
            "summary": "Get role by ID",
            "description": "Retrieve details of a single role and its mapped permission IDs.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "roleId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the role",
                }
            ],
            "responses": {
                "200": {
                    "description": "Role details retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/RoleEnvelope"}
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
                    "description": "Role not found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        },
        "delete": {
            "tags": ["Roles"],
            "summary": "Delete a role",
            "description": "Permanently remove a role definition.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "roleId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the role to delete",
                }
            ],
            "responses": {
                "200": {
                    "description": "Role deleted successfully",
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
                    "description": "Role not found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        },
    },
    "/api/v1/roles/{roleId}/permissions/{permissionId}": {
        "post": {
            "tags": ["Roles"],
            "summary": "Assign permission to role",
            "description": "Add an authorized permission triplet to the role.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "roleId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Target role UUID",
                },
                {
                    "name": "permissionId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Permission UUID to assign",
                },
            ],
            "responses": {
                "200": {
                    "description": "Permission assigned to role successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/RoleEnvelope"}
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
                    "description": "Role or Permission not found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        },
        "delete": {
            "tags": ["Roles"],
            "summary": "Revoke permission from role",
            "description": "Remove an assigned permission triplet from the role.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "roleId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Target role UUID",
                },
                {
                    "name": "permissionId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Permission UUID to revoke",
                },
            ],
            "responses": {
                "200": {
                    "description": "Permission revoked from role successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/RoleEnvelope"}
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
                    "description": "Role or Permission not found",
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
