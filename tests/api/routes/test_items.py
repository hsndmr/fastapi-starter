from fastapi.testclient import TestClient

from app.core.config import settings
from tests.utils.items import create_random_item


# @demo-code test create item
def test_create_item(client: TestClient, user_headers: dict[str, str]) -> None:
    data = {"title": "My Item", "description": "My description"}
    r = client.post(f"{settings.API_V1_STR}/items/", headers=user_headers, json=data)
    assert r.status_code == 200
    content = r.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content
    assert "created_at" in content


# @demo-code test create item without description
def test_create_item_without_description(
    client: TestClient, user_headers: dict[str, str]
) -> None:
    data = {"title": "No Description"}
    r = client.post(f"{settings.API_V1_STR}/items/", headers=user_headers, json=data)
    assert r.status_code == 200
    content = r.json()
    assert content["title"] == data["title"]
    assert content["description"] is None


# @demo-code test read items
def test_read_items(client: TestClient, user_headers: dict[str, str]) -> None:
    create_random_item(client, user_headers)
    create_random_item(client, user_headers)
    r = client.get(f"{settings.API_V1_STR}/items/", headers=user_headers)
    assert r.status_code == 200
    content = r.json()
    assert content["count"] >= 2
    assert len(content["data"]) >= 2


# @demo-code test read item by id
def test_read_item(client: TestClient, user_headers: dict[str, str]) -> None:
    item = create_random_item(client, user_headers)
    r = client.get(f"{settings.API_V1_STR}/items/{item['id']}", headers=user_headers)
    assert r.status_code == 200
    content = r.json()
    assert content["id"] == item["id"]
    assert content["title"] == item["title"]


# @demo-code test read item not found
def test_read_item_not_found(client: TestClient, user_headers: dict[str, str]) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/items/00000000-0000-0000-0000-000000000000",
        headers=user_headers,
    )
    assert r.status_code == 404


# @demo-code test read item not owned by user
def test_read_item_not_owned(client: TestClient) -> None:
    owner_headers = {"X-User-Id": "99"}
    other_headers = {"X-User-Id": "100"}
    item = create_random_item(client, owner_headers)
    r = client.get(f"{settings.API_V1_STR}/items/{item['id']}", headers=other_headers)
    assert r.status_code == 403


# @demo-code test update item
def test_update_item(client: TestClient, user_headers: dict[str, str]) -> None:
    item = create_random_item(client, user_headers)
    data = {"title": "Updated Title"}
    r = client.put(
        f"{settings.API_V1_STR}/items/{item['id']}",
        headers=user_headers,
        json=data,
    )
    assert r.status_code == 200
    content = r.json()
    assert content["title"] == "Updated Title"
    assert content["description"] == item["description"]


# @demo-code test update item not found
def test_update_item_not_found(
    client: TestClient, user_headers: dict[str, str]
) -> None:
    data = {"title": "Updated"}
    r = client.put(
        f"{settings.API_V1_STR}/items/00000000-0000-0000-0000-000000000000",
        headers=user_headers,
        json=data,
    )
    assert r.status_code == 404


# @demo-code test delete item
def test_delete_item(client: TestClient, user_headers: dict[str, str]) -> None:
    item = create_random_item(client, user_headers)
    r = client.delete(f"{settings.API_V1_STR}/items/{item['id']}", headers=user_headers)
    assert r.status_code == 200
    content = r.json()
    assert content["message"] == "Item deleted successfully"

    # verify it's gone
    r = client.get(f"{settings.API_V1_STR}/items/{item['id']}", headers=user_headers)
    assert r.status_code == 404


# @demo-code test delete item not found
def test_delete_item_not_found(
    client: TestClient, user_headers: dict[str, str]
) -> None:
    r = client.delete(
        f"{settings.API_V1_STR}/items/00000000-0000-0000-0000-000000000000",
        headers=user_headers,
    )
    assert r.status_code == 404


# @demo-code test unauthenticated request
def test_create_item_unauthenticated(client: TestClient) -> None:
    data = {"title": "Should Fail"}
    r = client.post(f"{settings.API_V1_STR}/items/", json=data)
    assert r.status_code == 401
