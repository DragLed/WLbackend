from pydantic import BaseModel


class GiftBase(BaseModel):
    title: str
    description: str | None = None
    price: float | None = None
    photo: str | None = None


class GiftCreate(GiftBase):
    pass


class GiftResponseBase(BaseModel):
    id: int


class GiftResponse(GiftResponseBase, GiftBase):
    is_reserved: bool

    class Config:
        from_attributes = True


class GiftResponseWithWishlist(GiftResponse):
    wishlist_id: int


class EditGift(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    photo: str | None = None