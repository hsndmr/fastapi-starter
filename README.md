# FastAPI Starter

A minimal FastAPI project template with a clean structure, ready to extend.

## Quick Start

```bash
make venv
make install-dev
make dev
```

The API will be available at `http://localhost:8000`. OpenAPI docs at `http://localhost:8000/docs`.

## Commands

| Command | Description |
|---------|-------------|
| `make dev` | Start dev server with hot reload |
| `make run` | Start production server (4 workers) |
| `make test` | Run tests with coverage |
| `make lint` | Linting and type checks |
| `make format` | Auto-format code |
| `make docker-build` | Build Docker image |
| `make docker-run` | Run Docker container |

## Tech Stack

- **FastAPI** — web framework
- **Pydantic v2** — validation and settings
- **uv** — package manager
- **ruff** — linter and formatter
- **mypy** — static type checking (strict)
- **pytest** — testing with coverage
