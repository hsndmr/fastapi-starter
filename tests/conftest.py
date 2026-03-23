from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.api.routes.items import fake_items_db
from app.main import app


# @demo-code fake db cleanup — clear in-memory store before/after tests
@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[dict, None, None]:
    fake_items_db.clear()
    yield fake_items_db
    fake_items_db.clear()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


# @demo-code user header fixture — simulates authenticated user via X-User-Id
@pytest.fixture(scope="module")
def user_headers() -> dict[str, str]:
    return {"X-User-Id": "1"}


# @demo-code superuser header fixture
@pytest.fixture(scope="module")
def superuser_headers() -> dict[str, str]:
    return {"X-User-Id": "0"}
