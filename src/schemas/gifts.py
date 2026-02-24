from pydantic import BaseModel


class GiftBase(BaseModel):
    title: str
    description: str | None
    price: int
    photo: str | None


class GiftCreate(GiftBase):
    wishlist_id: int


class GiftResponse(BaseModel):
    id: int
    title: str
    description: str | None
    price: int
    photo: str | None
    is_reserved: bool
    wishlist_id: int

    class Config:
        from_attributes = True
