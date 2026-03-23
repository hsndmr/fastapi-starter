import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, Field


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


# @demo-code models example
class ItemBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# @demo-code create and update models
class ItemCreate(ItemBase):
    pass


# @demo-code update model with optional fields
class ItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# @demo-code public model with id and timestamps
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


# @demo-code response model with list of items and count
class ItemsPublic(BaseModel):
    data: list[ItemPublic]
    count: int
