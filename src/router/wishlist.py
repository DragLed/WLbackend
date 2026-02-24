from fastapi import Depends, APIRouter, HTTPException
from authx.schema import TokenPayload
from config.cookie import security
from schemas.wishlists import WishlistBase, WishlistRespone
from sqlalchemy.orm import Session
from database.database import get_db
from api.wishlist import WishlistInterface, WishlistForbidden, WishlistNotFound
from core.enums import WishlistVisibility

rout = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@rout.post("/")
def create_wishlist(
    wl: WishlistBase,
    visibility: WishlistVisibility,
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(security.access_token_required),
):
    """
    Create a wishlist.
    """
    return WishlistInterface.create_wishlist(db, wl, int(token.sub), visibility)


@rout.get("/", response_model=list[WishlistRespone])
def get_my_wishlists(
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(security.access_token_required),
):
    return WishlistInterface.get_all_user_wishlist(db, int(token.sub))


@rout.get("/{id}", response_model=WishlistRespone)
def get_wishlist(
    id: int,
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(security.access_token_required),
):
    try:
        return WishlistInterface.get_wishlist(db, id, int(token.sub))
    except WishlistNotFound:
        raise HTTPException(status_code=404, detail="Wishlist not found")

    except WishlistForbidden:
        raise HTTPException(status_code=403, detail="Access denied")


@rout.delete("/{id}")
def delete_wishlist(
    id: int,
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(security.access_token_required),
):
    try:
        return WishlistInterface.delete_wishlist(db, id, int(token.sub))
    except WishlistNotFound:
        raise HTTPException(status_code=404, detail="Wishlist not found")

    except WishlistForbidden:
        raise HTTPException(status_code=403, detail="Access denied")
