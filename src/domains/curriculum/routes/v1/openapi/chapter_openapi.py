"""OpenAPI 3.0 specification for Chapter endpoints."""

from typing import Any

TAGS: list[dict[str, Any]] = [
    {
        "name": "Chapters",
        "description": "Curriculum chapter organization within subjects",
    }
]

COMPONENTS: dict[str, Any] = {
    "schemas": {
        "Chapter": {
            "type": "object",
            "required": ["id", "subjectId", "title", "order"],
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Chapter unique identifier",
                    "example": "123e4567-e89b-12d3-a456-426614174000",
                },
                "subjectId": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Parent subject identifier",
                    "example": "223e4567-e89b-12d3-a456-426614174000",
                },
                "title": {
                    "type": "string",
                    "description": "Title of the chapter",
                    "example": "Algebraic Equations",
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of the chapter",
                    "example": "Introduction to quadratic and linear equations",
                },
                "order": {
                    "type": "integer",
                    "description": "Display order index within the subject",
                    "example": 1,
                },
            },
        },
        "ChapterCreate": {
            "type": "object",
            "required": ["subjectId", "title", "order"],
            "properties": {
                "subjectId": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Parent subject identifier",
                    "example": "223e4567-e89b-12d3-a456-426614174000",
                },
                "title": {
                    "type": "string",
                    "description": "Title of the chapter",
                    "example": "Algebraic Equations",
                },
                "order": {
                    "type": "integer",
                    "description": "Order index within the subject",
                    "example": 1,
                },
                "description": {
                    "type": "string",
                    "description": "Description of the chapter",
                    "example": "Introduction to quadratic and linear equations",
                },
            },
        },
        "ChapterUpdate": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Updated title of the chapter",
                    "example": "Advanced Algebraic Equations",
                },
                "description": {
                    "type": "string",
                    "description": "Updated description",
                    "example": "Expanded chapter on non-linear equations",
                },
                "order": {
                    "type": "integer",
                    "description": "Updated order index",
                    "example": 2,
                },
            },
        },
        "ChapterEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {"$ref": "#/components/schemas/Chapter"},
                "meta": {"type": "object", "additionalProperties": True},
            },
        },
        "ChapterListEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/Chapter"},
                },
                "meta": {
                    "type": "object",
                    "properties": {
                        "page": {"type": "integer", "example": 1},
                        "pageSize": {"type": "integer", "example": 20},
                        "total": {"type": "integer", "example": 12},
                    },
                },
            },
        },
    }
}

PATHS: dict[str, Any] = {
    "/api/v1/chapters": {
        "get": {
            "tags": ["Chapters"],
            "summary": "List all chapters",
            "description": "Retrieve a paginated list of chapters, optionally filtered by subject.",
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
                    "schema": {"type": "integer", "default": 20, "minimum": 1, "maximum": 100},
                    "description": "Number of items per page",
                },
                {
                    "name": "subjectId",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Filter chapters by subject UUID",
                },
            ],
            "responses": {
                "200": {
                    "description": "List of chapters retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ChapterListEnvelope"}
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
            "tags": ["Chapters"],
            "summary": "Create a chapter",
            "description": "Create a new chapter within an academic subject.",
            "security": [{"BearerAuth": []}],
            "requestBody": {
                "required": True,
                "description": "Chapter creation payload",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ChapterCreate"}
                    }
                },
            },
            "responses": {
                "201": {
                    "description": "Chapter created successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ChapterEnvelope"}
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
    "/api/v1/chapters/{chapterId}": {
        "get": {
            "tags": ["Chapters"],
            "summary": "Get chapter by ID",
            "description": "Retrieve details of a single chapter by its unique ID.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "chapterId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the chapter",
                }
            ],
            "responses": {
                "200": {
                    "description": "Chapter details retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ChapterEnvelope"}
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
                    "description": "Chapter not found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        },
        "put": {
            "tags": ["Chapters"],
            "summary": "Update a chapter",
            "description": "Update attributes and metadata of an existing chapter.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "chapterId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the chapter to update",
                }
            ],
            "requestBody": {
                "required": True,
                "description": "Chapter update payload",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ChapterUpdate"}
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "Chapter updated successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ChapterEnvelope"}
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
                    "description": "Chapter not found",
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
            "tags": ["Chapters"],
            "summary": "Delete a chapter",
            "description": "Permanently remove a chapter from the curriculum.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "chapterId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the chapter to delete",
                }
            ],
            "responses": {
                "200": {
                    "description": "Chapter deleted successfully",
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
                    "description": "Chapter not found",
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
