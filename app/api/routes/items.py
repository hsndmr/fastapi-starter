import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.deps import UserIdDep
from app.models import (
    ItemCreate,
    ItemPublic,
    ItemsPublic,
    ItemUpdate,
    get_datetime_utc,
)

router = APIRouter(prefix="/items", tags=["items"])

# @demo-code in-memory fake storage
fake_items_db: dict[uuid.UUID, ItemPublic] = {}


# @demo-code read items endpoint with pagination
@router.get("/", response_model=ItemsPublic)
def read_items(current_user_id: UserIdDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve items for the current user.
    """
    user_items = [
        item
        for item in fake_items_db.values()
        if item.owner_id == uuid.UUID(int=current_user_id)
    ]
    user_items.sort(key=lambda x: x.created_at or get_datetime_utc(), reverse=True)
    count = len(user_items)
    return ItemsPublic(data=user_items[skip : skip + limit], count=count)


# @demo-code read item by id endpoint
@router.get("/{item_id}", response_model=ItemPublic)
def read_item(item_id: uuid.UUID, current_user_id: UserIdDep) -> Any:
    """
    Get item by ID.
    """
    item = fake_items_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != uuid.UUID(int=current_user_id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return item


# @demo-code create item endpoint
@router.post("/", response_model=ItemPublic)
def create_item(item_in: ItemCreate, current_user_id: UserIdDep) -> Any:
    """
    Create new item.
    """
    item = ItemPublic(
        id=uuid.uuid4(),
        owner_id=uuid.UUID(int=current_user_id),
        created_at=get_datetime_utc(),
        **item_in.model_dump(),
    )
    fake_items_db[item.id] = item
    return item


# @demo-code update item endpoint
@router.put("/{item_id}", response_model=ItemPublic)
def update_item(
    item_id: uuid.UUID, item_in: ItemUpdate, current_user_id: UserIdDep
) -> Any:
    """
    Update an item.
    """
    item = fake_items_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != uuid.UUID(int=current_user_id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    update_data = item_in.model_dump(exclude_unset=True)
    updated_item = item.model_copy(update=update_data)
    fake_items_db[item_id] = updated_item
    return updated_item


# @demo-code delete item endpoint
@router.delete("/{item_id}")
def delete_item(item_id: uuid.UUID, current_user_id: UserIdDep) -> dict[str, str]:
    """
    Delete an item.
    """
    item = fake_items_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != uuid.UUID(int=current_user_id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    del fake_items_db[item_id]
    return {"message": "Item deleted successfully"}
