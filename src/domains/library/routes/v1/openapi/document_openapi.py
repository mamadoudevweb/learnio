"""OpenAPI 3.0 specification for Document endpoints."""

from typing import Any

TAGS: list[dict[str, Any]] = [
    {
        "name": "Documents",
        "description": "Library document management, text extraction, and revision files",
    }
]

COMPONENTS: dict[str, Any] = {
    "schemas": {
        "Document": {
            "type": "object",
            "required": [
                "id",
                "title",
                "filePath",
                "fileName",
                "fileSizeBytes",
                "mimeType",
                "documentType",
                "source",
                "isTextExtracted",
                "createdAt",
                "updatedAt",
            ],
            "properties": {
                "id": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Document unique identifier",
                    "example": "123e4567-e89b-12d3-a456-426614174000",
                },
                "title": {
                    "type": "string",
                    "description": "Document title",
                    "example": "Physics Revision Notes 2026",
                },
                "filePath": {
                    "type": "string",
                    "description": "Storage path on disk or cloud",
                    "example": "/uploads/documents/physics_notes.pdf",
                },
                "fileName": {
                    "type": "string",
                    "description": "Original uploaded filename",
                    "example": "physics_notes.pdf",
                },
                "fileSizeBytes": {
                    "type": "integer",
                    "description": "Size of the file in bytes",
                    "example": 1048576,
                },
                "mimeType": {
                    "type": "string",
                    "description": "MIME type of the document",
                    "example": "application/pdf",
                },
                "subjectId": {
                    "type": "string",
                    "format": "uuid",
                    "nullable": True,
                    "description": "Associated subject identifier",
                    "example": "223e4567-e89b-12d3-a456-426614174000",
                },
                "chapterId": {
                    "type": "string",
                    "format": "uuid",
                    "nullable": True,
                    "description": "Associated chapter identifier",
                    "example": "323e4567-e89b-12d3-a456-426614174000",
                },
                "documentType": {
                    "type": "string",
                    "enum": ["course", "exercise", "exam", "summary", "other"],
                    "description": "Categorization of the document",
                    "example": "summary",
                },
                "source": {
                    "type": "string",
                    "enum": ["user", "teacher", "official"],
                    "description": "Source origin of the document",
                    "example": "user",
                },
                "year": {
                    "type": "integer",
                    "nullable": True,
                    "description": "Academic year of the material",
                    "example": 2026,
                },
                "extractedText": {
                    "type": "string",
                    "nullable": True,
                    "description": "Extracted OCR or text content for search",
                    "example": "Newton's Laws of Motion...",
                },
                "isTextExtracted": {
                    "type": "boolean",
                    "description": "Whether text extraction has finished",
                    "example": True,
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
        "DocumentCreate": {
            "type": "object",
            "required": ["title", "filePath", "fileName", "fileSizeBytes"],
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the document",
                    "example": "Physics Revision Notes 2026",
                },
                "filePath": {
                    "type": "string",
                    "description": "Storage path",
                    "example": "/uploads/documents/physics_notes.pdf",
                },
                "fileName": {
                    "type": "string",
                    "description": "File name",
                    "example": "physics_notes.pdf",
                },
                "fileSizeBytes": {
                    "type": "integer",
                    "description": "File size in bytes",
                    "example": 1048576,
                },
                "mimeType": {
                    "type": "string",
                    "default": "application/pdf",
                    "description": "MIME type",
                    "example": "application/pdf",
                },
                "subjectId": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Associated subject ID",
                },
                "chapterId": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Associated chapter ID",
                },
                "documentType": {
                    "type": "string",
                    "enum": ["course", "exercise", "exam", "summary", "other"],
                    "default": "other",
                },
                "source": {
                    "type": "string",
                    "enum": ["user", "teacher", "official"],
                    "default": "user",
                },
                "year": {
                    "type": "integer",
                    "minimum": 1990,
                    "maximum": 2100,
                    "example": 2026,
                },
                "extractedText": {
                    "type": "string",
                    "description": "Initial text content if pre-extracted",
                },
            },
        },
        "DocumentUpdate": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Updated title",
                    "example": "Updated Physics Notes",
                },
                "subjectId": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Updated subject ID",
                },
                "chapterId": {
                    "type": "string",
                    "format": "uuid",
                    "description": "Updated chapter ID",
                },
                "documentType": {
                    "type": "string",
                    "enum": ["course", "exercise", "exam", "summary", "other"],
                },
                "year": {
                    "type": "integer",
                    "minimum": 1990,
                    "maximum": 2100,
                },
                "extractedText": {
                    "type": "string",
                    "description": "Extracted OCR text",
                },
            },
        },
        "DocumentEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {"$ref": "#/components/schemas/Document"},
                "meta": {"type": "object", "additionalProperties": True},
            },
        },
        "DocumentListEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {
                    "type": "array",
                    "items": {"$ref": "#/components/schemas/Document"},
                },
                "meta": {
                    "type": "object",
                    "properties": {
                        "page": {"type": "integer", "example": 1},
                        "pageSize": {"type": "integer", "example": 20},
                        "total": {"type": "integer", "example": 8},
                    },
                },
            },
        },
    }
}

PATHS: dict[str, Any] = {
    "/api/v1/documents": {
        "get": {
            "tags": ["Documents"],
            "summary": "List documents",
            "description": "Retrieve a paginated and filtered list of library documents.",
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
                    "description": "Filter by subject UUID",
                },
                {
                    "name": "chapterId",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Filter by chapter UUID",
                },
                {
                    "name": "documentType",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string", "enum": ["course", "exercise", "exam", "summary", "other"]},
                    "description": "Filter by document type",
                },
                {
                    "name": "source",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string", "enum": ["user", "teacher", "official"]},
                    "description": "Filter by document source",
                },
                {
                    "name": "year",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "integer"},
                    "description": "Filter by year",
                },
                {
                    "name": "search",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string"},
                    "description": "Search term across title and extracted text",
                },
            ],
            "responses": {
                "200": {
                    "description": "List of documents retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/DocumentListEnvelope"}
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
            "tags": ["Documents"],
            "summary": "Create a document",
            "description": "Register metadata for a new revision document.",
            "security": [{"BearerAuth": []}],
            "requestBody": {
                "required": True,
                "description": "Document creation payload",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/DocumentCreate"}
                    }
                },
            },
            "responses": {
                "201": {
                    "description": "Document registered successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/DocumentEnvelope"}
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
    "/api/v1/documents/{documentId}": {
        "get": {
            "tags": ["Documents"],
            "summary": "Get document by ID",
            "description": "Retrieve full metadata and extracted content of a single document.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "documentId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the document",
                }
            ],
            "responses": {
                "200": {
                    "description": "Document details retrieved successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/DocumentEnvelope"}
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
                    "description": "Document not found",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        },
        "put": {
            "tags": ["Documents"],
            "summary": "Update document metadata",
            "description": "Update metadata or extracted text of an existing document.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "documentId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the document to update",
                }
            ],
            "requestBody": {
                "required": True,
                "description": "Document update payload",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/DocumentUpdate"}
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "Document updated successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/DocumentEnvelope"}
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
                    "description": "Document not found",
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
            "tags": ["Documents"],
            "summary": "Delete a document",
            "description": "Permanently remove a document from the library.",
            "security": [{"BearerAuth": []}],
            "parameters": [
                {
                    "name": "documentId",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string", "format": "uuid"},
                    "description": "Unique identifier of the document to delete",
                }
            ],
            "responses": {
                "200": {
                    "description": "Document deleted successfully",
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
                    "description": "Document not found",
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
