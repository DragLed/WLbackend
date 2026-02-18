from pydantic import BaseModel

class GiftRespone(BaseModel):
    id: int
    name: str
    description: str | None
    price: int
    photo: str | None
    userId: int
    is_reserved: bool
    reserved_by_id: int | None

class GiftCreate(BaseModel):
    name: str
    description: str | None
    price: int
    photo: str | None

