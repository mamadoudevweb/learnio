"""OpenAPI 3.0 specification for Lesson endpoints."""

from typing import Any

TAGS: list[dict[str, Any]] = [
    {
        "name": "Lessons",
        "description": "Educational lesson management within chapters",
    }
]

COMPONENTS: dict[str, Any] = {
    "schemas": {
        "Lesson": {
            "type": "object",
            "required": ["id", "chapterId", "title", "content", "order"],
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Lesson unique identifier",
                    "example": "123e4567-e89b-12d3-a456-426614174000",
                },
                "chapterId": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Parent chapter identifier",
                    "example": "223e4567-e89b-12d3-a456-426614174000",
                },
                "title": {
                    "type": "string",
                    "description": "Title of the lesson",
                    "example": "Solving Quadratic Equations by Factoring",
                },
                "content": {
                    "type": "string",
                    "description": "Lesson instructional text and markdown content",
                    "example": "Step 1: Write equation in standard form ax^2 + bx + c = 0...",
                },
                "order": {
                    "type": "integer",
                    "description": "Order index within the chapter",
                    "example": 1,
                },
            },
        },
        "LessonCreate": {
            "type": "object",
            "required": ["chapterId", "title", "content", "order"],
            "properties": {
                "chapterId": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Parent chapter identifier",
                    "example": "223e4567-e89b-12d3-a456-426614174000",
                },
                "title": {
                    "type": "string",
                    "description": "Title of the lesson",
                    "example": "Solving Quadratic Equations by Factoring",
                },
                "content": {
                    "type": "string",
                    "description": "Instructional content of the lesson",
                    "example": "Step 1: Write equation in standard form...",
                },
                "order": {
                    "type": "integer",
                    "description": "Order index within the chapter",
                    "example": 1,
                },
            },
        },
        "LessonUpdate": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Updated title of the lesson",
                    "example": "Solving Quadratic Equations by Factoring - Revised",
                },
                "content": {
                    "type": "string",
                    "description": "Updated lesson content",
                    "example": "Revised step-by-step factoring method...",
                },
                "order": {
                    "type": "integer",
                    "description": "Updated order index",
                    "example": 2,
                },
            },
        },
        "LessonEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {"$ref": "#/components/schemas/Lesson"},
                "meta": {"type": "object", "additionalProperties": True},
            },
        },
        "LessonListEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/Lesson"},
                },
                "meta": {
                    "type": "object",
                    "properties": {
                        "page": {"type": "integer", "example": 1},
                        "pageSize": {"type": "integer", "example": 20},
                        "total": {"type": "integer", "example": 35},
                    },
                },
            },
        },
    }
}

PATHS: dict[str, Any] = {
    "/api/v1/lessons": {
        "get": {
            "tags": ["Lessons"],
            "summary": "List all lessons",
            "description": "Retrieve a paginated list of lessons, optionally filtered by chapter.",
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
                    "name": "chapterId",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Filter lessons by chapter UUID",
                },
            ],
            "responses": {
                "200": {
                    "description": "List of lessons retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/LessonListEnvelope"
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
            "tags": ["Lessons"],
            "summary": "Create a lesson",
            "description": "Create a new instructional lesson within a chapter.",
            "security": [{"BearerAuth": []}],
            "requestBody": {
                "required": True,
                "description": "Lesson creation payload",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/LessonCreate"}
                    }
                },
            },
            "responses": {
                "201": {
                    "description": "Lesson created successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/LessonEnvelope"}
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
    "/api/v1/lessons/{lessonId}": {
        "get": {
            "tags": ["Lessons"],
            "summary": "Get lesson by ID",
            "description": "Retrieve details of a single lesson by its unique ID.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "lessonId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the lesson",
                }
            ],
            "responses": {
                "200": {
                    "description": "Lesson details retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/LessonEnvelope"}
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
                    "description": "Lesson not found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        },
        "put": {
            "tags": ["Lessons"],
            "summary": "Update a lesson",
            "description": "Update content and attributes of an existing lesson.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "lessonId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the lesson to update",
                }
            ],
            "requestBody": {
                "required": True,
                "description": "Lesson update payload",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/LessonUpdate"}
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "Lesson updated successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/LessonEnvelope"}
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
                    "description": "Lesson not found",
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
            "tags": ["Lessons"],
            "summary": "Delete a lesson",
            "description": "Permanently remove a lesson from the chapter.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "lessonId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the lesson to delete",
                }
            ],
            "responses": {
                "200": {
                    "description": "Lesson deleted successfully",
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
                    "description": "Lesson not found",
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
