from datetime import datetime
from pydantic import BaseModel
from core.enums import WishlistVisibility


class WishlistBase(BaseModel):
    title: str
    description: str
    visibility: WishlistVisibility
    owner_id: int


class WishlistRespone(BaseModel):
    id: int
    title: str
    description: str
    visibility: WishlistVisibility
    owner_id: int
    share_token: str | None
    created_at: datetime
