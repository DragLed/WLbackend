from pydantic import BaseModel


class GiftBase(BaseModel):
    title: str
    description: str | None
    price: int
    photo: str | None


class GiftCreate(GiftBase):
    pass


class GiftResponse(BaseModel):
    id: int
    title: str
    description: str | None
    price: int
    photo: str | None
    is_reserved: bool

    class Config:
        from_attributes = True


class GiftResponeWithWishlist(GiftResponse):
    wishlist_id: int

class EditGift(GiftBase):
    pass