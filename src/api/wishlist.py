from sqlalchemy.orm import Session
from schemas.wishlists import WishlistBase
from core.enums import WishlistVisibility
from models.wishlist import Wishlist


class WishlistNotFound(Exception):
    pass


class WishlistForbidden(Exception):
    pass


class WishlistInterface:
    @staticmethod
    def _check_access(wishlist: Wishlist, user_id: int):
        if not wishlist:
            raise WishlistNotFound()

        if wishlist.owner_id != user_id and wishlist.visibility != "public":
            raise WishlistForbidden()

    @staticmethod
    def create_wishlist(
        db: Session,
        wishlist: WishlistBase,
        owner_id: int,
        visibility: WishlistVisibility,
    ):
        wl = Wishlist(
            title=wishlist.title,
            description=wishlist.description,
            owner_id=owner_id,
            visibility=visibility,
        )
        db.add(wl)
        db.commit()
        db.refresh(wl)
        return {"message": "Wishlist added"}

    @staticmethod
    def get_all_wishlists(db: Session):
        wishlists = db.query(Wishlist).all()
        if wishlists:
            if len(wishlists) > 0:
                return wishlists
            return
        raise WishlistNotFound()

    @staticmethod
    def get_all_user_wishlist(db: Session, userId: int):
        wishlists = db.query(Wishlist).filter(Wishlist.owner_id == userId).all()
        if len(wishlists) > 0:
            return wishlists
        return

    @staticmethod
    def get_wishlist(db: Session, wishlist_id: int, owner_id: int):
        wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
        WishlistInterface._check_access(wishlist, owner_id)
        return wishlist

    @staticmethod
    def delete_wishlist(db: Session, wlid: int, owner_id: int):
        wishlist = db.query(Wishlist).filter(Wishlist.id == wlid).first()
        WishlistInterface._check_access(wishlist, owner_id)
        return wishlist
