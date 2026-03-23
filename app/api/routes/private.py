from typing import Any

from fastapi import APIRouter

from app.api.routes.items import fake_items_db

router = APIRouter(prefix="/private", tags=["private"])


# @demo-code private endpoint — only available in local environment
@router.get("/items", response_model=list[dict[str, Any]])
def read_all_items() -> Any:
    """
    Read all items from all users. For development/debugging only.
    """
    return [item.model_dump() for item in fake_items_db.values()]
