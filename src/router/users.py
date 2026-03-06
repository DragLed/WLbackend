from fastapi import HTTPException, Response, Depends, APIRouter, Query
from authx.schema import TokenPayload
from api.users import UserInterface
from api.wishlist import WishlistInterface
from sqlalchemy.orm import Session
from schemas.users import UserRead
from database.database import get_db
from config.cookie import security, config

rout = APIRouter(prefix="/users", tags=["User"])


@rout.get("/", response_model=list[UserRead])
def get_all_users(db: Session = Depends(get_db)):
    """
    Getting all users
    """
    return UserInterface.get_all_users(db)


@rout.get("/{Id}", response_model=UserRead)
def get_user_by_id(Id: str, db: Session = Depends(get_db)):
    """
    Getting information about a user by ID
    """
    return UserInterface.get_user_by_id(db, Id)


@rout.get("/search/{username}", response_model=list[UserRead])
def get_users_by_username(
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(security.access_token_required),
):
    """
    Getting information about users by username
    """
    return UserInterface.get_users_by_username(db, q, int(token.sub))


@rout.delete("/{Id}", dependencies=[Depends(security.access_token_required)])
def remove_user(
    response: Response,
    Id: str,
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(security.access_token_required),
):
    """
    Delete a user by ID.
    """
    user_id = token.sub
    if user_id == Id:
        response.delete_cookie(key=config.JWT_ACCESS_COOKIE_NAME)
        return UserInterface.delete_user(db, Id)
    raise HTTPException(status_code=403, detail="Access denied")


@rout.get("/{userId}/wishlist", dependencies=[Depends(security.access_token_required)])
def get_user_wishlists(userId: int, db: Session = Depends(get_db)):
    return WishlistInterface.get_all_user_wishlist(db, userId)
