# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-10-14

### Added

#### Core Architecture & Domain-Driven Design (DDD)
- **Account Domain**:
  - User accounts and profile management.
  - Authentication subsystem (`Credential`, `Session`, `CredentialReset`).
  - Role-Based Access Control (`Role`, `Permission`) with triplet definitions (`domain:resource:action`).
  - Domain events and asynchronous event handlers for email notifications (welcome emails, password resets).
- **Curriculum Domain**:
  - Structured academic hierarchy: `Subject`, `Chapter`, `Lesson`.
  - Ordering, filtering, and comprehensive CRUD operations.
- **Library Domain**:
  - Digital document repository (`Document`) with metadata, MIME types, and text extraction status tracking.

#### Generic Core Infrastructure
- `BaseEntity` dataclass with domain event registration and validation.
- Abstract `BaseRepository` interface and SQLAlchemy-based `BaseSqlRepository`.
- Registry-based `RepositoryRegistry` agnostic of storage engines, supporting canonical names and aliases.
- Transactional `SqlUnitOfWork` with intra-session repository caching and post-commit event publishing.
- Multi-backend email service (`ConsoleEmailSender`, `SmtpEmailSender`) with Jinja template rendering.
- Environment-specific Pydantic configuration with validation (`DevelopmentConfig`, `TestingConfig`, `ProductionConfig`).

#### Builder Pattern
- `BaseBuilder[T]` base class integrated with Flask's logging system (`default_handler`, `app.logger`).
- `ConfigBuilder` for fluent configuration assembly and overrides.
- `RepositoryRegistryBuilder` for expressive repository registration.
- Modular domain service builders (`CurriculumServicesBuilder`, `LibraryServicesBuilder`, `AccountServicesBuilder`, `DomainServicesBuilder`).
- `AppBuilder` orchestrating the complete Flask application assembly.

#### REST API & Security
- Standardized API response envelopes for both success and error responses.
- Stateless authentication with JWT (`Flask-JWT-Extended`).
- Dynamic OpenAPI 3.0 documentation with Swagger UI served at `/api/v1/docs`.
- Health check endpoint at `/api/v1/health` providing service status and version information.
- Rate limiting and standard error handlers (HTTP 422, 500, Domain `AppError`).

#### DevOps & Packaging
- Python 3.14 compatibility managed via Astral `uv`.
- Multi-stage `Dockerfile` with non-root security user and `gunicorn` production WSGI server.
- `compose.yml` for multi-container orchestration.
- GitHub Actions CI workflow for linting (Ruff), formatting checks, bytecode compilation, and pytest execution.
- Automated Docker Hub deployment and GitHub Release publishing workflows.
- Comprehensive test suite comprising 164 unit and integration tests.
