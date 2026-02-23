from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from api.gifts import GiftInterface
from config.cookie import security
from database.database import get_db
from schemas.gifts import GiftRespone, GiftCreate


rout = APIRouter(prefix="/gifts", tags=["Gift"])


@rout.post("/", dependencies=[Depends(security.access_token_required)])
def create_gift(gift: GiftCreate, db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Create a gift.
    """
    return GiftInterface.create_gift(db, gift, token.sub)


@rout.get("/all", dependencies=[Depends(security.access_token_required)], response_model=list[GiftRespone])
def get_all_gifts(db: Session = Depends(get_db)):
    """
    Get all gifts.
    """
    return GiftInterface.get_all_gifts(db) 


@rout.get("/", dependencies=[Depends(security.access_token_required)], response_model=list[GiftRespone])
def get_all_my_gifts(db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Get all gifts for the current user.
    """
    return GiftInterface.get_all_gifts_user(db, token.sub) 


@rout.delete("/{giftId}", dependencies=[Depends(security.access_token_required)])
def remove_gift(giftId: str, db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Delete a gift by ID.
    """
    return GiftInterface.delete_gift(db, giftId, token.sub)


@rout.get("/{giftId}", dependencies=[Depends(security.access_token_required)], response_model=GiftRespone)
def get_gift_by_id(giftId: int, db: Session = Depends(get_db)):
    """
    Get a gift by ID.
    """
    return GiftInterface.get_gift_by_id(db,giftId)


@rout.put("/{giftId}", dependencies=[Depends(security.access_token_required)])
def edit_gift(giftId: int, GiftEdit: GiftCreate, db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Update a gift by ID.
    """
    return GiftInterface.edit_gift_by_id(db, giftId, GiftEdit, token.sub)


@rout.get("/all/{userID}", dependencies=[Depends(security.access_token_required)], response_model=list[GiftRespone])
def get_all_gifts_by_user_id(userID: int, db: Session = Depends(get_db)):
    """
    Get all gifts for a user by user ID.
    """
    return GiftInterface.get_all_gifts_user(db, userID)


@rout.put("/{gift_id}/reserve", dependencies=[Depends(security.access_token_required)])
def reserve_gift(gift_id:int, db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Reserve a gift for the current user.
    """
    return GiftInterface.reserve_gift(db, gift_id, token.sub)


@rout.put("/{gift_id}/unreserve", dependencies=[Depends(security.access_token_required)])
def unreserve_gift(gift_id:int, db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Unreserve a previously reserved gift.
    """
    return GiftInterface.unreserve_gift(db, gift_id, token.sub)