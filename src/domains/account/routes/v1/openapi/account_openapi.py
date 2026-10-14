"""OpenAPI 3.0 specification for Account endpoints."""

from typing import Any

TAGS: list[dict[str, Any]] = [
    {
        "name": "Accounts",
        "description": "User account profiles and role assignment management",
    }
]

COMPONENTS: dict[str, Any] = {
    "schemas": {
        "Account": {
            "type": "object",
            "required": [
                "id",
                "firstName",
                "lastName",
                "active",
                "roleIds",
                "createdAt",
                "updatedAt",
            ],
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Account unique identifier",
                    "example": "123e4567-e89b-12d3-a456-426614174000",
                },
                "firstName": {
                    "type": "string",
                    "description": "First name of the user",
                    "example": "Mariama",
                },
                "lastName": {
                    "type": "string",
                    "description": "Last name of the user",
                    "example": "Sow",
                },
                "birthDate": {
                    "type": "string",
                    "format": "date",
                    "nullable": True,
                    "description": "Birth date of the user",
                    "example": "2004-03-12",
                },
                "active": {
                    "type": "boolean",
                    "description": "Account active status",
                    "example": True,
                },
                "roleIds": {
                    "type": "array",
                    "items": {"type": "string", "format": "uuid"},
                    "description": "List of role identifiers assigned to this account",
                    "example": ["223e4567-e89b-12d3-a456-426614174000"],
                },
                "createdAt": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Account creation timestamp in UTC",
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
        "AccountCreate": {
            "type": "object",
            "required": ["firstName", "lastName"],
            "properties": {
                "firstName": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 25,
                    "description": "First name",
                    "example": "Mariama",
                },
                "lastName": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 25,
                    "description": "Last name",
                    "example": "Sow",
                },
                "birthDate": {
                    "type": "string",
                    "format": "date",
                    "nullable": True,
                    "description": "Date of birth",
                    "example": "2004-03-12",
                },
                "active": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether account is initially active",
                    "example": True,
                },
                "roleIds": {
                    "type": "array",
                    "items": {"type": "string", "format": "uuid"},
                    "description": "Optional initial role IDs",
                },
            },
        },
        "AccountUpdate": {
            "type": "object",
            "properties": {
                "firstName": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 25,
                    "description": "Updated first name",
                    "example": "Mariama",
                },
                "lastName": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 25,
                    "description": "Updated last name",
                    "example": "Diallo",
                },
                "birthDate": {
                    "type": "string",
                    "format": "date",
                    "nullable": True,
                    "description": "Updated birth date",
                    "example": "2004-03-12",
                },
                "active": {
                    "type": "boolean",
                    "description": "Updated status",
                    "example": True,
                },
            },
        },
        "AccountEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {"$ref": "#/components/schemas/Account"},
                "meta": {"type": "object", "additionalProperties": True},
            },
        },
        "AccountListEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/Account"},
                },
                "meta": {
                    "type": "object",
                    "properties": {
                        "page": {"type": "integer", "example": 1},
                        "pageSize": {"type": "integer", "example": 20},
                        "total": {"type": "integer", "example": 100},
                    },
                },
            },
        },
    }
}

PATHS: dict[str, Any] = {
    "/api/v1/accounts": {
        "get": {
            "tags": ["Accounts"],
            "summary": "List all accounts",
            "description": "Retrieve a paginated list of accounts with optional search and active status filter.",
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
                    "name": "search",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string"},
                    "description": "Search term across first and last names",
                },
                {
                    "name": "active",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "boolean"},
                    "description": "Filter by active status",
                },
            ],
            "responses": {
                "200": {
                    "description": "List of accounts retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/AccountListEnvelope"
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
            "tags": ["Accounts"],
            "summary": "Create an account",
            "description": "Create a new user profile account.",
            "security": [{"BearerAuth": []}],
            "requestBody": {
                "required": True,
                "description": "Account payload",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/AccountCreate"}
                    }
                },
            },
            "responses": {
                "201": {
                    "description": "Account created successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/AccountEnvelope"}
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
    "/api/v1/accounts/{accountId}": {
        "get": {
            "tags": ["Accounts"],
            "summary": "Get account by ID",
            "description": "Retrieve full profile information of a single account.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "accountId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the account",
                }
            ],
            "responses": {
                "200": {
                    "description": "Account details retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/AccountEnvelope"}
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
                    "description": "Account not found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        },
        "put": {
            "tags": ["Accounts"],
            "summary": "Update an account",
            "description": "Update profile details of an existing account.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "accountId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the account to update",
                }
            ],
            "requestBody": {
                "required": True,
                "description": "Account update payload",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/AccountUpdate"}
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "Account updated successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/AccountEnvelope"}
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
                    "description": "Account not found",
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
        "delete": {
            "tags": ["Accounts"],
            "summary": "Delete an account",
            "description": "Permanently remove an account.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "accountId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the account to delete",
                }
            ],
            "responses": {
                "200": {
                    "description": "Account deleted successfully",
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
                    "description": "Account not found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        },
    },
    "/api/v1/accounts/{accountId}/roles/{roleId}": {
        "post": {
            "tags": ["Accounts"],
            "summary": "Assign role to account",
            "description": "Assign an RBAC role to the specified account.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "accountId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Target account UUID",
                },
                {
                    "name": "roleId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Role UUID to assign",
                },
            ],
            "responses": {
                "200": {
                    "description": "Role assigned successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/AccountEnvelope"}
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
                    "description": "Account or Role not found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        },
        "delete": {
            "tags": ["Accounts"],
            "summary": "Revoke role from account",
            "description": "Remove an assigned RBAC role from the specified account.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "accountId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Target account UUID",
                },
                {
                    "name": "roleId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Role UUID to revoke",
                },
            ],
            "responses": {
                "200": {
                    "description": "Role removed successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/AccountEnvelope"}
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
                    "description": "Account or Role not found",
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
