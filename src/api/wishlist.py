from sqlalchemy.orm import Session
from schemas.wishlists import WishlistBase, EditWishlist
from core.enums import WishlistVisibility, WishlistRole
from models.wishlist import Wishlist
from models.wishlist_access import WishlistAccess


class WishlistNotFound(Exception):
    pass


class WishlistForbidden(Exception):
    pass


class WishlistInterface:
    @staticmethod
    def _check_access(db: Session, wishlist: Wishlist, user_id: int):
        if not wishlist:
            raise WishlistNotFound()

        if wishlist.owner_id == user_id:
            return "owner"

        if wishlist.visibility == WishlistVisibility.public:
            return "public"

        if wishlist.visibility == WishlistVisibility.link_only:
            access = (
                db.query(WishlistAccess)
                .filter(
                    WishlistAccess.wishlist_id == wishlist.id,
                    WishlistAccess.user_id == user_id,
                )
                .first()
            )

            if access:
                return access.role in [WishlistRole.editor, WishlistRole.viewer]
        raise WishlistForbidden()

    @staticmethod
    def _require_role(role, allowed_roles):
        if role not in allowed_roles:
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
        wishlist = db.query(Wishlist).filter(Wishlist.owner_id == userId).all()
        if wishlist:
            if len(wishlist) > 0:
                return wishlist
            return []
        raise WishlistNotFound()

    @staticmethod
    def get_wishlist(db: Session, wishlist_id: int, owner_id: int):
        wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
        role = WishlistInterface._check_access(db, wishlist, owner_id)
        WishlistInterface._require_role(role, ["owner", "editor", "viewer"])
        return wishlist

    @staticmethod
    def delete_wishlist(db: Session, wlid: int, owner_id: int):
        wishlist = db.query(Wishlist).filter(Wishlist.id == wlid).first()
        role = WishlistInterface._check_access(db, wishlist, owner_id)
        WishlistInterface._require_role(role, ["owner"])
        db.delete(wishlist)
        db.commit()
        return {"message": "wishlist deleted"}

    @staticmethod
    def post_access_wishlist(
        db: Session, wishlist_id: int, owner_id: int, user_id: int, role: WishlistRole
    ):
        wishlist = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()

        if wishlist is None:
            raise WishlistNotFound()

        if wishlist.visibility == WishlistVisibility.public:
            return {"message": "Wishlist is public, no need to add access"}

        if wishlist.visibility == WishlistVisibility.private:
            return {"message": "Wishlist is private, no need to add access"}

        if WishlistInterface._check_access(db, wishlist, owner_id) != "owner":
            raise WishlistForbidden()

        access = (
            db.query(WishlistAccess)
            .filter(
                WishlistAccess.user_id == user_id,
                WishlistAccess.wishlist_id == wishlist_id,
            )
            .first()
        )
        if access:
            access.role = role
            db.commit()
            return {"message": "Wishlist access updated"}
        access = WishlistAccess(
            wishlist_id=wishlist_id,
            user_id=user_id,
            invited_by_id=owner_id,
            role=role,
        )
        db.add(access)
        db.commit()
        db.refresh(access)
        return {"message": "Wishlist access added"}

    @staticmethod
    def delete_access_wishlist(
        db: Session, wishlist_id: int, owner_id: int, user_id: int
    ):
        access = (
            db.query(WishlistAccess)
            .filter(
                WishlistAccess.user_id == user_id,
                WishlistAccess.wishlist_id == wishlist_id,
            )
            .first()
        )
        if access:
            if access.invited_by_id == owner_id:
                db.delete(access)
                db.commit()
                return {"message": "wishlist access deleted"}
            raise WishlistForbidden()
        raise WishlistNotFound()

    @staticmethod
    def get_wishlist_by_token(db: Session, token: str):
        wishlist = db.query(Wishlist).filter(Wishlist.share_token == token).first()
        if not wishlist:
            raise WishlistNotFound()
        return wishlist

    @staticmethod
    def get_all_access(db: Session, user_id: int):
        access_wishlists = (
            db.query(WishlistAccess).filter(WishlistAccess.user_id == user_id).all()
        )
        return access_wishlists

    @staticmethod
    def edit_wishlist(db: Session, wl: EditWishlist, id: int, owner_id: int):
        wishlist = db.query(Wishlist).filter(Wishlist.id == id).first()
        role = WishlistInterface._check_access(db, wishlist, owner_id)
        WishlistInterface._require_role(role, ["owner", "editor"])

        if wl:
            raise WishlistNotFound()

        if wl.title is not None:
            wishlist.title = wl.title
        if wl.description is not None:
            wishlist.description = wl.description
        if wl.visibility is not None:
            wishlist.visibility = wl.visibility

        db.commit()
        db.refresh(wishlist)
        return {"message": "Wishlist updated"}
