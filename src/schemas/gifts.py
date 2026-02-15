from pydantic import BaseModel

class GiftView(BaseModel):
    name: str
    description: str | None
    price: int
    photo: str | None