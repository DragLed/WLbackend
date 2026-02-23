from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from schemas.wishlists import WishlistRespone
from database.database import get_db
from models.gifts import Gift
from models.users import User
from sqlalchemy import text
from api.wishlist import WishlistInterface
from config.cookie import security


rout = APIRouter(prefix="/dev", tags=["Dev"])


@rout.get("/health", dependencies=[Depends(security.access_token_required)])
def health_check(db: Session = Depends(get_db)):
    """
    Check database connectivity and return service health.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except:
        raise HTTPException(status_code=500, detail="Database error")
    

@rout.get("/stats", dependencies=[Depends(security.access_token_required)])
def get_stats(db: Session = Depends(get_db)):
    """
    Return counts for users, gifts and reserved gifts.
    """
    users_count = db.query(User).all()
    gifts_count = db.query(Gift).all()
    reserved_gifts = db.query(Gift).filter(Gift.is_reserved == True).count()

    return {
        "users_count": users_count,
        "gifts_count": gifts_count,
        "reserved_gifts": reserved_gifts
    }


@rout.get("/wishlisrt", dependencies=[Depends(security.access_token_required)], response_model=list[WishlistRespone])
def get_all_wishlists(db: Session = Depends(get_db)):
    return WishlistInterface.get_all_wishlists(db)