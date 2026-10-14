"""OpenAPI 3.0 specification for Subject endpoints."""

from typing import Any

TAGS: list[dict[str, Any]] = [
    {
        "name": "Subjects",
        "description": "Academic curriculum subject management endpoints",
    }
]

COMPONENTS: dict[str, Any] = {
    "schemas": {
        "Subject": {
            "type": "object",
            "required": ["id", "name", "code", "isActive"],
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Subject unique identifier",
                    "example": "123e4567-e89b-12d3-a456-426614174000",
                },
                "name": {
                    "type": "string",
                    "description": "Name of the subject",
                    "example": "Mathematics",
                },
                "code": {
                    "type": "string",
                    "description": "Unique code identifier for the subject",
                    "example": "MATH-101",
                },
                "isActive": {
                    "type": "boolean",
                    "description": "Whether the subject is currently active",
                    "example": True,
                },
            },
        },
        "SubjectCreate": {
            "type": "object",
            "required": ["name", "code"],
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the subject",
                    "example": "Mathematics",
                },
                "code": {
                    "type": "string",
                    "description": "Unique code identifier for the subject",
                    "example": "MATH-101",
                },
            },
        },
        "SubjectUpdate": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Updated name of the subject",
                    "example": "Advanced Mathematics",
                },
                "code": {
                    "type": "string",
                    "description": "Updated code identifier",
                    "example": "MATH-201",
                },
                "isActive": {
                    "type": "boolean",
                    "description": "Updated active status",
                    "example": True,
                },
            },
        },
        "SubjectEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {"$ref": "#/components/schemas/Subject"},
                "meta": {"type": "object", "additionalProperties": True},
            },
        },
        "SubjectListEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/Subject"},
                },
                "meta": {
                    "type": "object",
                    "properties": {
                        "page": {"type": "integer", "example": 1},
                        "pageSize": {"type": "integer", "example": 20},
                        "total": {"type": "integer", "example": 50},
                    },
                },
            },
        },
    }
}

PATHS: dict[str, Any] = {
    "/api/v1/subjects": {
        "get": {
            "tags": ["Subjects"],
            "summary": "List all subjects",
            "description": "Retrieve a paginated list of academic subjects with optional filtering.",
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
                    "name": "isActive",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "boolean"},
                    "description": "Filter by active status",
                },
                {
                    "name": "code",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string"},
                    "description": "Filter by subject code",
                },
            ],
            "responses": {
                "200": {
                    "description": "List of subjects retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/SubjectListEnvelope"
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
            "tags": ["Subjects"],
            "summary": "Create a subject",
            "description": "Create a new academic subject.",
            "security": [{"BearerAuth": []}],
            "requestBody": {
                "required": True,
                "description": "Subject payload",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/SubjectCreate"}
                    }
                },
            },
            "responses": {
                "201": {
                    "description": "Subject created successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/SubjectEnvelope"}
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
    "/api/v1/subjects/{subjectId}": {
        "get": {
            "tags": ["Subjects"],
            "summary": "Get subject by ID",
            "description": "Retrieve details of a single subject by its unique ID.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "subjectId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the subject",
                }
            ],
            "responses": {
                "200": {
                    "description": "Subject details retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/SubjectEnvelope"}
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
                    "description": "Subject not found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        },
        "put": {
            "tags": ["Subjects"],
            "summary": "Update a subject",
            "description": "Update metadata and attributes of an existing subject.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "subjectId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the subject to update",
                }
            ],
            "requestBody": {
                "required": True,
                "description": "Subject update payload",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/SubjectUpdate"}
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "Subject updated successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/SubjectEnvelope"}
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
                    "description": "Subject not found",
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
            "tags": ["Subjects"],
            "summary": "Delete a subject",
            "description": "Permanently remove a subject from the curriculum.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "subjectId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the subject to delete",
                }
            ],
            "responses": {
                "200": {
                    "description": "Subject deleted successfully",
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
                    "description": "Subject not found",
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
