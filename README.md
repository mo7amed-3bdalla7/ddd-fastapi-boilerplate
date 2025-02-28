# DDD FastAPI Boilerplate

A Domain-Driven Design (DDD) boilerplate for FastAPI applications with MongoDB integration.

## Project Structure

```
.
├── app/
│   ├── domain/              # Domain layer: Business entities and value objects
│   │   ├── entities/        # Business entities (e.g., User, Product)
│   │   └── value_objects/   # Value objects (immutable objects)
│   │
│   ├── application/         # Application layer: Use cases and interfaces
│   │   ├── interfaces/      # Abstract interfaces (e.g., repositories)
│   │   └── use_cases/      # Application use cases/services
│   │
│   └── infrastructure/      # Infrastructure layer: External concerns
│       ├── api/            # API-related code (routes, dependencies)
│       │   └── routes/     # API route handlers
│       ├── config/         # Configuration (settings, env vars)
│       └── database/       # Database implementations
│           └── repositories/# Concrete repository implementations
│
└── tests/                  # Test suite
    ├── unit/              # Unit tests following the same structure as app/
    └── integration/       # Integration tests for API and database
```

## Layer Responsibilities

### Domain Layer (`app/domain/`)
- Contains the core business logic and rules
- Defines business entities and value objects
- No dependencies on other layers
- Pure Python with no external dependencies

### Application Layer (`app/application/`)
- Implements use cases (application services)
- Defines interfaces (ports) for infrastructure
- Orchestrates domain objects
- Contains application-specific business rules

### Infrastructure Layer (`app/infrastructure/`)
- Implements interfaces defined in the application layer
- Contains all external concerns (database, API, etc.)
- Handles technical details and external services
- Framework-specific code (FastAPI, MongoDB)

## Prerequisites

- Python 3.9 or higher
- MongoDB
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

## Setup and Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd ddd-fastapi-boilerplate
```

### 2. Environment Setup

First, install uv if you haven't already:
```bash
# Install uv globally
pip install uv
```

Create and activate a virtual environment using uv:

```bash
# Create virtual environment with uv
uv venv


# Install project dependencies
uv sync

# Install development dependencies
uv sync --dev
```

### 3. Environment Configuration

Copy the example environment file and adjust as needed:
```bash
cp .env.example .env
```

## UV Package Management Commands

```bash
# Install a new package
uv add package_name

# Remove a package
uv remove package_name

# Sync dependencies with pyproject.toml
uv sync

# Change Python version
# 1. Create new venv with specific Python version
uv venv --python=python3.x
```

## Running the Application

1. Start MongoDB:
```bash
# Make sure MongoDB is running on your system
mongod
```

2. Run the FastAPI application:
```bash
# Development Using one of below
uv run fastapi dev
uvicorn app.main:app --reload 

# Production
uvicorn app.main:app
```

The API will be available at `http://localhost:8000`
API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
```

## Development Guidelines

1. Follow Domain-Driven Design principles
2. Write tests for new features
3. Update documentation when making changes
4. Follow PEP 8 style guide
5. Use type hints

## License

[MIT License](LICENSE)
