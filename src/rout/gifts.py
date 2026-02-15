from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from api.gifts import GiftInterface
from config.cookie import security, config
from database import get_db
from schemas.gifts import GiftView



rout = APIRouter(prefix="/gifts", tags=["Gift"])


@rout.get("/", response_model=list[GiftView])
def get_all_my_gifts(db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Get all gifts for the current user.
    """
    user_id = token.sub
    gifts = GiftInterface.get_all_gifts_user(db, user_id) 
    if len(gifts) == 0:
        raise HTTPException(status_code=404, detail="No gifts found for this user")
    return gifts

@rout.get("/all", response_model=list[GiftView])
def get_all_gifts(db: Session = Depends(get_db)):
    """
    Get all gifts.
    """
    gifts = GiftInterface.get_all_gifts(db) 
    if len(gifts) == 0:
        raise HTTPException(status_code=404, detail="No gifts found")
    return gifts


@rout.post("/")
def create_gift(gift: GiftView, db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Create a gift.
    """
    user_id = token.sub
    GiftInterface.create_gift(db, gift.name, gift.description, gift.price, gift.photo, user_id)
    return {"message": "Gift added"}



@rout.delete("/{giftId}", dependencies=[Depends(security.access_token_required)], response_model=GiftView)
def remove_gift(giftId: int, db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Delete a gift by ID.
    """
    user_id = token.sub
    gift = GiftInterface.get_gift_by_id(db,giftId)
    if not gift:
        raise HTTPException(status_code=404, detail="Gift not found")
    if int(gift.userId) == int(user_id):
        response_data = GiftInterface.delete_gift(db,giftId)
        if response_data:
            return response_data
        raise HTTPException(status_code=404, detail="Gift not found")
    raise HTTPException(status_code=403, detail="Access denied")

@rout.get("/{giftId}", response_model=GiftView)
def get_gift_by_id(giftId: int, db: Session = Depends(get_db)):
    """
    Get a gift by ID.
    """
    gift = GiftInterface.get_gift_by_id(db,giftId)
    if gift:
        return gift
    raise HTTPException(status_code=404, detail="Gift not found")


@rout.put("/{giftId}", dependencies=[Depends(security.access_token_required)])
def edit_gift(giftId: int, gift_data: GiftView, db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Update a gift by ID.
    """
    user_id = token.sub
    gift = GiftInterface.get_gift_by_id(db,giftId)
    if not gift:
        raise HTTPException(status_code=404, detail="Gift not found")
    if int(gift.userId) == int(user_id):
        GiftInterface.edit_gift_by_id(db, giftId, gift_data.name, gift_data.description, gift_data.price, gift_data.photo)
        return {"message": f"Gift with ID {giftId} has been updated"}
    raise HTTPException(status_code=403, detail="Access denied")


@rout.get("/user/{userID}", response_model=list[GiftView])
def get_all_gifts_by_user_id(userID: int, db: Session = Depends(get_db)):
    """
    Get all gifts for a user by user ID.
    """
    gifts = GiftInterface.get_all_gifts_user(db, userID) 
    if len(gifts) == 0:
        raise HTTPException(status_code=404, detail="No gifts found for this user")
    return gifts
