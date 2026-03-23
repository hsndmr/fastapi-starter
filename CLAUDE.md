# CLAUDE.md

This is a FastAPI starter template. Follow these patterns when adding new features.

## Commands

```bash
make install-dev   # Install dependencies (uses uv)
make dev           # Dev server with hot reload
make test          # Run tests with coverage
make lint          # ruff + mypy (strict mode)
make format        # Auto-format with ruff
```

## Project Structure

```
app/
├── main.py                  # Creates FastAPI app, attaches routers
├── models.py                # Pydantic request/response models
├── core/
│   ├── config.py            # Environment settings (pydantic-settings)
│   └── security.py          # Security utilities
└── api/
    ├── main.py              # Aggregates all routers
    ├── deps.py              # Dependencies (auth, db connection)
    └── routes/              # One file per resource
        ├── items.py
        └── private.py       # Only active in local environment
```

## Adding a New Endpoint

1. Create a new file under `app/api/routes/` (e.g. `users.py`)
2. Define a router with `APIRouter(prefix="/users", tags=["users"])`
3. Register it in `app/api/main.py` via `api_router.include_router()`
4. All endpoints live under the `/api/v1` prefix (`settings.API_V1_STR`)

Each route file owns a single resource. Route functions contain business logic directly — there is no separate service layer.

## Pydantic Models (`app/models.py`)

Each resource follows this model set:

- **Base**: Shared fields (`ItemBase`)
- **Create**: Creation request, inherits from Base (`ItemCreate`)
- **Update**: Update request, all fields optional (`ItemUpdate`)
- **Public**: Response model, adds id + owner_id + created_at (`ItemPublic`)
- **ListPublic**: List response with `data: list[Public]` + `count: int` (`ItemsPublic`)

Follow the same pattern when adding a new resource. All models are defined in `app/models.py`.

Routes declare their response model via the `response_model` parameter on the decorator. FastAPI uses this to validate and serialize the response, and to generate the OpenAPI schema:

```python
@router.get("/", response_model=ItemsPublic)
def read_items(current_user_id: UserIdDep, skip: int = 0, limit: int = 100) -> Any:
    ...
    return ItemsPublic(data=user_items[skip : skip + limit], count=count)

@router.post("/", response_model=ItemPublic)
def create_item(item_in: ItemCreate, current_user_id: UserIdDep) -> Any:
    ...
    return ItemPublic(id=uuid.uuid4(), owner_id=..., created_at=..., **item_in.model_dump())
```

- **Single item** endpoints use the `Public` model (e.g. `response_model=ItemPublic`)
- **List** endpoints use the `ListPublic` wrapper (e.g. `response_model=ItemsPublic`)
- **Request body** is typed as a function parameter (`item_in: ItemCreate`) — FastAPI parses it automatically
- Return type is `Any` — the actual validation is handled by `response_model`, not the type hint

Error responses use `HTTPException` with appropriate status codes:

```python
raise HTTPException(status_code=404, detail="Item not found")
raise HTTPException(status_code=403, detail="Not enough permissions")
raise HTTPException(status_code=401, detail="Missing user id")
```

No need to use `raise ... from e` — ruff rule `B904` is ignored for this reason.

## Dependencies (`app/api/deps.py`)

All shared dependencies live in `app/api/deps.py`. This is the central place for anything that gets injected into route functions.

Each dependency is a plain function paired with an `Annotated` type alias so routes stay clean.

**Regular dependency** (plain return) — for simple lookups, parsed headers, config values:

```python
def get_current_user_id(request: Request) -> int:
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing user id")
    return int(user_id)

UserIdDep = Annotated[int, Depends(get_current_user_id)]

def read_items(current_user_id: UserIdDep): ...
```

**Yield dependency** (generator pattern) — for resources that need cleanup after the request (connections, sessions, file handles):

```python
def get_connection() -> Generator[dict[str, Any], None, None]:
    conn = open_connection()
    try:
        yield conn          # injected into the route
    finally:
        conn.close()        # cleanup after request

ConnectionDep = Annotated[dict, Depends(get_connection)]

def read_items(conn: ConnectionDep): ...
```

**When adding a new dependency**: write the function in `deps.py`, create an `Annotated` alias next to it, and use that alias as a parameter type in your route functions.

Currently defined:
- `get_connection()` / `ConnectionDep` — yield dependency example (resource with cleanup)
- `get_current_user_id()` / `UserIdDep` — reads `X-User-Id` header, returns 401 if missing

## Environment Settings (`app/core/config.py`)

- Uses `pydantic-settings`, loads from `.env` file
- Automatically uses `.env.testing` during test runs
- `ENVIRONMENT`: `"local"`, `"staging"`, `"production"` — private routes are only active in local
- To add new config, add a field to the `Settings` class and update `.env` files
- `SECRET_KEY` cannot remain default in production (enforced by validator)

## Writing Tests

- Tests live under `tests/`, mirroring the app structure (`tests/api/routes/`, `tests/core/`)
- `conftest.py` fixtures: `client` (TestClient), `user_headers`, `superuser_headers`
- Test helpers go in `tests/utils/`
- Cover all CRUD operations + permission checks + 404 cases
- Run with `make test` (generates coverage report)

## Code Quality

- **ruff**: Linter + formatter. `T201` is enabled — do not use `print()`.
- **mypy**: Strict mode. Type annotations required on all functions.
- Use Python 3.10+ syntax (`X | None` instead of `Optional[X]`).
- `B904` is ignored — no need for `from e` when raising `HTTPException`.
