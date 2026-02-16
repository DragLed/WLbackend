from pydantic import BaseModel

class GiftRespone(BaseModel):
    id: int
    name: str
    description: str | None
    price: int
    photo: str | None
    userId: int

class GiftEdit(BaseModel):
    name: str
    description: str | None
    price: int
    photo: str | None

