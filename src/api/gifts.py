from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.gifts import Gift
from models.wishlist import Wishlist
from schemas.gifts import GiftCreate
from api.wishlist import WishlistInterface


class GiftInterface:
    @staticmethod
    def create_gift(db: Session, gift_data: GiftCreate, owner_id: int, wlid: int):
        wishlist = db.query(Wishlist).filter(Wishlist.id == wlid).first()
        role = WishlistInterface._check_access(db, wishlist, owner_id)
        WishlistInterface._require_role(role, ["owner", "editor"])

        new_gift = Gift(
            title=gift_data.title,
            description=gift_data.description,
            price=gift_data.price,
            photo=gift_data.photo,
            wishlist_id=wlid
        )
        db.add(new_gift)
        db.commit()
        db.refresh(new_gift)
        return new_gift
    
    @staticmethod
    def get_all_gifts_by_wishlist(db: Session, wlid: int, owner_id: int):
        wishlist = db.query(Wishlist).filter(Wishlist.id == wlid).first()
        role = WishlistInterface._check_access(db, wishlist, owner_id)
        WishlistInterface._require_role(role, ["owner", "editor", "viewer"])
        return wishlist.gifts
    
    @staticmethod
    def get_gift(db: Session, gift_id: int, owner_id: int):
        gift = db.query(Gift).filter(Gift.id == gift_id).first()
        if not gift:
            raise HTTPException(status_code=404, detail="Gift not found")

        wishlist = db.query(Wishlist).filter(Wishlist.id == gift.wishlist_id).first()
        role = WishlistInterface._check_access(db, wishlist, owner_id)
        WishlistInterface._require_role(role, ["owner", "editor", "viewer"])
        return gift