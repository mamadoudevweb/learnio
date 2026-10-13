"""OpenAPI 3.0 specification for Auth endpoints."""

from typing import Any

TAGS: list[dict[str, Any]] = [
    {
        "name": "Auth",
        "description": "Authentication, user registration, sessions, and credential reset",
    }
]

COMPONENTS: dict[str, Any] = {
    "schemas": {
        "RegisterRequest": {
            "type": "object",
            "required": ["firstName", "lastName", "email", "password"],
            "properties": {
                "firstName": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 25,
                    "description": "First name of the user",
                    "example": "Mariama",
                },
                "lastName": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 25,
                    "description": "Last name of the user",
                    "example": "Sow",
                },
                "email": {
                    "type": "string",
                    "format": "email",
                    "minLength": 3,
                    "maxLength": 255,
                    "description": "Unique email address",
                    "example": "mariama.sow@example.com",
                },
                "password": {
                    "type": "string",
                    "format": "password",
                    "writeOnly": True,
                    "minLength": 6,
                    "description": "Secret account password",
                    "example": "SecurePassword123!",
                },
                "birthDate": {
                    "type": "string",
                    "format": "date",
                    "nullable": True,
                    "description": "Birth date of the user",
                    "example": "2004-03-12",
                },
            },
        },
        "LoginRequest": {
            "type": "object",
            "required": ["email", "password"],
            "properties": {
                "email": {
                    "type": "string",
                    "format": "email",
                    "description": "Registered email address",
                    "example": "mariama.sow@example.com",
                },
                "password": {
                    "type": "string",
                    "format": "password",
                    "writeOnly": True,
                    "description": "Account password",
                    "example": "SecurePassword123!",
                },
            },
        },
        "LoginData": {
            "type": "object",
            "required": ["token", "account", "permissions"],
            "properties": {
                "token": {
                    "type": "string",
                    "readOnly": True,
                    "description": "Cryptographic session token or JWT",
                    "example": "7b8e1f2a3c4d5e6f...",
                },
                "account": {
                    "$ref": "#/components/schemas/Account",
                },
                "permissions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of authorized permission triplets ('domain:resource:action')",
                    "example": ["account:account:read", "account:account:update"],
                },
            },
        },
        "LoginEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {"$ref": "#/components/schemas/LoginData"},
                "meta": {"type": "object", "additionalProperties": True},
            },
        },
        "PasswordResetRequest": {
            "type": "object",
            "required": ["email"],
            "properties": {
                "email": {
                    "type": "string",
                    "format": "email",
                    "description": "Registered email address to request password reset",
                    "example": "mariama.sow@example.com",
                },
            },
        },
        "PasswordResetConfirm": {
            "type": "object",
            "required": ["token", "newPassword"],
            "properties": {
                "token": {
                    "type": "string",
                    "writeOnly": True,
                    "description": "Reset token received by the user",
                    "example": "a1b2c3d4e5f6...",
                },
                "newPassword": {
                    "type": "string",
                    "format": "password",
                    "writeOnly": True,
                    "minLength": 6,
                    "description": "New secret password to set",
                    "example": "BrandNewPassword123!",
                },
            },
        },
        "PasswordResetEnvelope": {
            "type": "object",
            "required": ["success", "data"],
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "example": "Password reset token sent"},
                        "resetToken": {
                            "type": "string",
                            "readOnly": True,
                            "description": "Generated password reset token",
                            "example": "a1b2c3d4e5f6...",
                        },
                    },
                },
                "meta": {"type": "object", "additionalProperties": True},
            },
        },
    }
}

PATHS: dict[str, Any] = {
    "/api/v1/auth/register": {
        "post": {
            "tags": ["Auth"],
            "summary": "Register a new user",
            "description": "Public endpoint to register a new user account with credentials.",
            "security": [],
            "requestBody": {
                "required": True,
                "description": "User registration payload",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/RegisterRequest"}
                    }
                },
            },
            "responses": {
                "201": {
                    "description": "Account registered successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/AccountEnvelope"}
                        }
                    },
                },
                "409": {
                    "description": "Email address already registered",
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
    "/api/v1/auth/login": {
        "post": {
            "tags": ["Auth"],
            "summary": "Authenticate user",
            "description": "Public endpoint to verify user credentials and return an active session token.",
            "security": [],
            "requestBody": {
                "required": True,
                "description": "Login credentials",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/LoginRequest"}
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "Authentication successful",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/LoginEnvelope"}
                        }
                    },
                },
                "401": {
                    "description": "Invalid email or password",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
                "403": {
                    "description": "Account is inactive or disabled",
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
    "/api/v1/auth/password-reset/request": {
        "post": {
            "tags": ["Auth"],
            "summary": "Request password reset",
            "description": "Initiate password reset flow for an existing user account email.",
            "security": [],
            "requestBody": {
                "required": True,
                "description": "Target email payload",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/PasswordResetRequest"}
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "Password reset token generated",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/PasswordResetEnvelope"}
                        }
                    },
                },
                "404": {
                    "description": "Credential not found for specified email",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
                "422": {
                    "description": "Validation error in email format",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ErrorEnvelope"}
                        }
                    },
                },
            },
        },
    },
    "/api/v1/auth/password-reset/confirm": {
        "post": {
            "tags": ["Auth"],
            "summary": "Confirm password reset",
            "description": "Consume valid password reset token and update account password.",
            "security": [],
            "requestBody": {
                "required": True,
                "description": "Reset confirmation payload",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/PasswordResetConfirm"}
                    }
                },
            },
            "responses": {
                "200": {
                    "description": "Password updated successfully",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/EmptyEnvelope"}
                        }
                    },
                },
                "400": {
                    "description": "Reset token is invalid, expired, or already used",
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
    "/api/v1/auth/logout": {
        "post": {
            "tags": ["Auth"],
            "summary": "Revoke active session",
            "description": "Revoke user authentication session by invalidating the bearer token.",
            "security": [{"BearerAuth": []}],
            "responses": {
                "200": {
                    "description": "Session revoked successfully",
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
            },
        },
    },
}
