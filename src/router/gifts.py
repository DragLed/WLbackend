from fastapi import Depends, APIRouter, HTTPException
from authx.schema import TokenPayload
from sqlalchemy.orm import Session
from api.gifts import GiftInterface, GiftNotFound
from config.cookie import security
from database.database import get_db
from schemas.gifts import GiftResponse, EditGift
from api.wishlist import WishlistForbidden, WishlistNotFound

rout = APIRouter(prefix="/gifts", tags=["Gift"])


@rout.get("/{gift_id}", response_model=GiftResponse)
def get_gift(gift_id: int, db: Session = Depends(get_db), token: TokenPayload = Depends(security.access_token_required)):
    try:
        return GiftInterface.get_gift(db, gift_id, int(token.sub))
    except GiftNotFound:
        raise HTTPException(status_code=404, detail="Gift not found")
    except WishlistNotFound:
        raise HTTPException(status_code=404, detail="Wishlist not found")

    except WishlistForbidden:
        raise HTTPException(status_code=403, detail="Access denied")
    
@rout.delete("/{gift_id}")
def delete_gift(gift_id: int, db: Session = Depends(get_db), token: TokenPayload = Depends(security.access_token_required)):
    try:
        return GiftInterface.delete_gift(db, gift_id, int(token.sub))
    except GiftNotFound:
        raise HTTPException(status_code=404, detail="Gift not found")
    except WishlistNotFound:
        raise HTTPException(status_code=404, detail="Wishlist not found")

    except WishlistForbidden:
        raise HTTPException(status_code=403, detail="Access denied")
    
@rout.put("/{gift_id}")
def edit_gift(gift_id: int, gift_data: EditGift, db: Session = Depends(get_db), token: TokenPayload = Depends(security.access_token_required)):
    try:
        return GiftInterface.edit_gift(db, gift_data, gift_id, int(token.sub))
    except GiftNotFound:
        raise HTTPException(status_code=404, detail="Gift not found")
    except WishlistNotFound:
        raise HTTPException(status_code=404, detail="Wishlist not found")

    except WishlistForbidden:
        raise HTTPException(status_code=403, detail="Access denied")
