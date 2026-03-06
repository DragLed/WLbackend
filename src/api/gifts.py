from sqlalchemy.orm import Session
from models.gifts import Gift
from models.wishlist import Wishlist
from schemas.gifts import GiftCreate, EditGift
from api.wishlist import WishlistInterface

class GiftNotFound(Exception):
    pass

class GiftInterface:
    @staticmethod
    def create_gift(db: Session, gift_data: GiftCreate, owner_id: int, wlid: int):
        wishlist = db.query(Wishlist).filter(Wishlist.id == wlid).first()
        role = WishlistInterface._check_access(db, wishlist, owner_id)
        WishlistInterface._require_role(role, ["owner", "editor"])

        new_gift = Gift(**gift_data.dict(), wishlist_id=wlid)
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
            raise GiftNotFound()

        wishlist = db.query(Wishlist).filter(Wishlist.id == gift.wishlist_id).first()
        role = WishlistInterface._check_access(db, wishlist, owner_id)
        WishlistInterface._require_role(role, ["owner", "editor", "viewer"])
        return gift
    

    @staticmethod
    def delete_gift(db: Session, gift_id: int, owner_id: int):
        gift = db.query(Gift).filter(Gift.id == gift_id).first()
        if not gift:
            raise GiftNotFound()
        wishlist = db.query(Wishlist).filter(Wishlist.id == gift.wishlist_id).first()
        role = WishlistInterface._check_access(db, wishlist, owner_id)
        WishlistInterface._require_role(role, ["owner", "editor"])
        db.delete(gift)
        db.commit()
        return {"message": "gift is removed"}
    
    @staticmethod
    def edit_gift(db: Session, gift_data: EditGift, gift_id: int, user_id: int):

        gift = db.query(Gift).filter(Gift.id == gift_id).first()

        if not gift:
            raise GiftNotFound()

        wishlist = db.query(Wishlist).filter(Wishlist.id == gift.wishlist_id).first()

        role = WishlistInterface._check_access(db, wishlist, user_id)
        WishlistInterface._require_role(role, ["owner", "editor"])

        for key, value in gift_data.model_dump(exclude_unset=True).items():
            setattr(gift, key, value)

        db.commit()
        db.refresh(gift)

        return gift

