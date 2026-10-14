# Learnio

[![CI](https://github.com/mamadoudevweb/learnio/actions/workflows/ci.yml/badge.svg)](https://github.com/mamadoudevweb/learnio/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/mamadoudevweb/learnio/releases)
[![Python](https://img.shields.io/badge/python-3.14%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Learnio** is a modular, high-performance Learning Management System (LMS) backend API built with **Flask**, **Domain-Driven Design (DDD)**, **Clean Architecture**, and the **Builder Pattern**.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
  - [Development Mode](#development-mode)
  - [Production Mode (Gunicorn)](#production-mode-gunicorn)
  - [Docker & Docker Compose](#docker--docker-compose)
- [API Documentation](#api-documentation)
- [Testing & Quality](#testing--quality)
- [Project Structure](#project-structure)
- [Release & Versioning](#release--versioning)
- [License](#license)

---

## Features

- **Account & Identity Management**:
  - Secure authentication via hashed credentials and stateful sessions.
  - Password reset flows via one-time tokens and templated email notifications.
  - Granular Role-Based Access Control (RBAC) with triplet permissions (`domain:resource:action`).
- **Curriculum Management**:
  - Structured academic subjects, chapters, and lessons.
  - Granular ordering and comprehensive filtering.
- **Digital Library**:
  - Document cataloging with MIME type tracking, file size metrics, and OCR text extraction status.
- **Enterprise-Grade Architecture**:
  - Bounded contexts with zero cross-domain circular coupling.
  - Technology-agnostic `RepositoryRegistry` and transactional `UnitOfWork`.
  - Fluent **Builder Pattern** for configuration, repositories, domain services, and application composition.
  - Domain event dispatching after commit to ensure consistency.
- **Developer Experience**:
  - Dynamic OpenAPI 3.0 documentation with interactive Swagger UI.
  - Unified JSON response envelopes (`success`, `data`, `meta`, `error`).
  - Native integration with Flask's logging system.

---

## Architecture

Learnio strictly adheres to Clean Architecture and Domain-Driven Design principles:

```
src/
├── core/                  # Technology-agnostic infrastructure
│   ├── builder.py         # BaseBuilder[T] with Flask logging
│   ├── config.py          # ConfigBuilder & Pydantic configurations
│   ├── database.py        # SQLAlchemy Base
│   ├── email.py           # Email sender & template services
│   ├── errors.py          # Unified application exceptions
│   └── unit_of_work/      # RepositoryRegistry, BaseUnitOfWork, SqlUnitOfWork
│
├── domains/               # Bounded contexts (Business Logic)
│   ├── account/           # User accounts, authentication & RBAC
│   ├── curriculum/        # Subjects, chapters, and lessons
│   └── library/           # Documents and digital assets
│
└── app/                   # Composition root
    ├── builder.py         # AppBuilder (Flask application assembler)
    ├── factory.py         # create_app() factory
    ├── uow.py             # Repository registration
    ├── domain_service_builder.py # DomainServicesBuilder
    ├── routes.py          # Blueprint routing & /api/v1/health
    └── docs.py            # OpenAPI 3.0 specifications
```

---

## Tech Stack

- **Language**: Python 3.14+
- **Framework**: Flask 3.1+
- **Packaging & Tooling**: [uv](https://astral.sh/uv), Ruff
- **ORM & Database**: SQLAlchemy 2.0+, SQLite (Dev/Test) / PostgreSQL (Prod)
- **Validation & Settings**: Pydantic 2.0+, Pydantic-Settings
- **Security & Tokens**: Flask-JWT-Extended
- **WSGI Server**: Gunicorn
- **Testing**: Pytest, Pytest-Flask

---

## Prerequisites

- [uv](https://docs.astral.sh/uv/) (recommended) or Python 3.14+
- Docker & Docker Compose (optional for containerized deployment)

---

## Installation

Clone the repository and install all dependencies:

```bash
git clone https://github.com/mamadoudevweb/learnio.git
cd learnio

# Install dependencies using uv
uv sync --all-extras --dev
```

---

## Configuration

Copy the example environment file and customize your settings:

```bash
cp .env.example .env
```

Key configuration variables:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `LEARNIO_ENV` | Environment (`development`, `testing`, `production`) | `development` |
| `LEARNIO_DEBUG` | Enable debug mode | `true` |
| `LEARNIO_SECRET_KEY` | Flask secret key (minimum 32 chars) | Required in production |
| `LEARNIO_JWT_SECRET_KEY`| JWT secret key (must differ from SECRET_KEY) | Required in production |
| `LEARNIO_DATABASE_URL` | SQLAlchemy database URI | `sqlite:///learnio.db` |
| `LEARNIO_EMAIL_BACKEND` | Email backend (`console`, `memory`, `smtp`) | `console` |
| `LEARNIO_UPLOAD_DIR` | Directory for file uploads | `uploads` |

---

## Running the Application

### Development Mode

Run the Flask development server with auto-reload:

```bash
uv run flask --app main:app run --debug
```

Or run via `main.py`:

```bash
uv run python main.py
```

The application will be accessible at `http://127.0.0.1:5000`.

### Production Mode (Gunicorn)

Run using the production WSGI server:

```bash
uv run gunicorn --bind 0.0.0.0:5000 --workers 4 --threads 2 main:app
```

### Docker & Docker Compose

Build and run using Docker Compose:

```bash
docker compose up --build -d
```

View logs:

```bash
docker compose logs -f
```

---

## API Documentation

Interactive OpenAPI/Swagger documentation is available directly in your browser:

- **Swagger UI**: [http://localhost:5000/api/v1/docs](http://localhost:5000/api/v1/docs)
- **Health Check**: [http://localhost:5000/api/v1/health](http://localhost:5000/api/v1/health)

Example health check response:
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

---

## Testing & Quality

Run the test suite (164 tests):

```bash
uv run pytest -v
```

Run code formatting and linting checks:

```bash
# Check code style with Ruff
uv run ruff check src tests

# Check code formatting with Ruff
uv run ruff format --check src tests

# Verify Python bytecode compilation
uv run python -m compileall src tests
```

---

## Release & Versioning

This project adheres to [Semantic Versioning](https://semver.org/). To prepare a new release:

1. Update version in `src/__version__.py` and `pyproject.toml`.
2. Document changes in `CHANGELOG.md`.
3. Create and push a git tag (e.g. `v0.1.0`):
   ```bash
   git tag -a v0.1.0 -m "Release v0.1.0"
   git push upstream v0.1.0
   ```
4. GitHub Actions will automatically validate the build, run tests, create a GitHub Release, and publish Docker images.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
