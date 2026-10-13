"""Integration tests for OpenAPI documentation endpoints."""

from __future__ import annotations


def test_openapi_json_returns_200_and_valid_spec(client):
    """GET /api/v1/openapi.json should return 200 with OpenAPI 3.0.3 specification."""
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    data = response.get_json()
    assert data["openapi"] == "3.0.3"
    assert data["info"]["title"] == "Learnio API"
    assert data["info"]["version"] == "1.0.0"
    assert "paths" in data
    assert "components" in data


def test_openapi_json_contains_all_core_routes(client):
    """GET /api/v1/openapi.json must contain route specifications for all domains."""
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    paths = response.get_json()["paths"]

    # System health
    assert "/api/v1/health" in paths

    # Curriculum domain
    assert "/api/v1/subjects" in paths
    assert "/api/v1/subjects/{subjectId}" in paths
    assert "/api/v1/chapters" in paths
    assert "/api/v1/chapters/{chapterId}" in paths
    assert "/api/v1/lessons" in paths
    assert "/api/v1/lessons/{lessonId}" in paths

    # Library domain
    assert "/api/v1/documents" in paths
    assert "/api/v1/documents/{documentId}" in paths

    # Account domain
    assert "/api/v1/accounts" in paths
    assert "/api/v1/accounts/{accountId}" in paths
    assert "/api/v1/accounts/{accountId}/roles/{roleId}" in paths

    # Auth subdomain
    assert "/api/v1/auth/register" in paths
    assert "/api/v1/auth/login" in paths
    assert "/api/v1/auth/password-reset/request" in paths
    assert "/api/v1/auth/password-reset/confirm" in paths
    assert "/api/v1/auth/logout" in paths

    # Access control (Roles & Permissions) subdomain
    assert "/api/v1/roles" in paths
    assert "/api/v1/roles/{roleId}" in paths
    assert "/api/v1/roles/{roleId}/permissions/{permissionId}" in paths
    assert "/api/v1/permissions" in paths
    assert "/api/v1/permissions/{permissionId}" in paths


def test_openapi_json_contains_security_schemes(client):
    """GET /api/v1/openapi.json must include BearerAuth security scheme and schemas."""
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    components = response.get_json()["components"]

    assert "securitySchemes" in components
    assert "BearerAuth" in components["securitySchemes"]
    assert components["securitySchemes"]["BearerAuth"]["scheme"] == "bearer"

    schemas = components["schemas"]
    assert "EmptyEnvelope" in schemas
    assert "ErrorEnvelope" in schemas
    assert "Subject" in schemas
    assert "Chapter" in schemas
    assert "Lesson" in schemas
    assert "Document" in schemas
    assert "Account" in schemas
    assert "Role" in schemas
    assert "Permission" in schemas


def test_swagger_ui_endpoint_returns_html(client):
    """GET /api/v1/docs should serve the interactive Swagger UI page."""
    response = client.get("/api/v1/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["Content-Type"]
    html = response.get_data(as_text=True)
    assert "swagger-ui" in html
    assert "/api/v1/openapi.json" in html
