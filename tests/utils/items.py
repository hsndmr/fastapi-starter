from fastapi.testclient import TestClient

from app.core.config import settings


# @demo-code helper to create an item via API and return the response json
def create_random_item(client: TestClient, headers: dict[str, str]) -> dict:
    data = {"title": "Test Item", "description": "Test Description"}
    r = client.post(f"{settings.API_V1_STR}/items/", headers=headers, json=data)
    assert r.status_code == 200
    return r.json()
