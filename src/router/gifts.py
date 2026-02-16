from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from api.gifts import GiftInterface
from config.cookie import security
from database.database import get_db
from schemas.gifts import GiftRespone,GiftEdit


rout = APIRouter(prefix="/gifts", tags=["Gift"])


@rout.get("/", response_model=list[GiftRespone])
def get_all_my_gifts(db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Get all gifts for the current user.
    """
    return GiftInterface.get_all_gifts_user(db, token.sub) 
    

@rout.get("/all", response_model=list[GiftRespone])
def get_all_gifts(db: Session = Depends(get_db)):
    """
    Get all gifts.
    """
    return GiftInterface.get_all_gifts(db) 
     

@rout.post("/")
def create_gift(gift: GiftRespone, db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Create a gift.
    """
    return GiftInterface.create_gift(db, gift.name, gift.description, gift.price, gift.photo, token.sub)


@rout.delete("/{giftId}", dependencies=[Depends(security.access_token_required)])
def remove_gift(giftId: str, db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Delete a gift by ID.
    """
    return GiftInterface.delete_gift(db, giftId, token.sub)


@rout.get("/{giftId}", response_model=GiftRespone)
def get_gift_by_id(giftId: int, db: Session = Depends(get_db)):
    """
    Get a gift by ID.
    """
    gift = GiftInterface.get_gift_by_id(db,giftId)
    if gift:
        return gift
    raise HTTPException(status_code=404, detail="Gift not found")


@rout.put("/{giftId}", dependencies=[Depends(security.access_token_required)])
def edit_gift(giftId: int, GiftEdit: GiftEdit, db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Update a gift by ID.
    """
    return GiftInterface.edit_gift_by_id(db, giftId, token.sub, GiftEdit.name, GiftEdit.description, GiftEdit.price, GiftEdit.photo)


@rout.get("/all/{userID}", response_model=list[GiftRespone])
def get_all_gifts_by_user_id(userID: int, db: Session = Depends(get_db)):
    """
    Get all gifts for a user by user ID.
    """
    return GiftInterface.get_all_gifts_user(db, userID) 