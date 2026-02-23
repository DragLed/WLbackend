from api.auth import AuthInterface
from api.users import UserInterface
from config.cookie import security, config
from fastapi import Depends, Response, APIRouter
from authx.schema import TokenPayload
from sqlalchemy.orm import Session
from schemas.users import UserCreate, UserRead, UserResetPassword
from database.database import get_db


rout = APIRouter(prefix="/auth", tags=["Auth"])



@rout.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Creating a user
    """
    return AuthInterface.create_user(db, user)


@rout.post("/login")
def login(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    """
    Checking the user's login and password and creating a JWT token
    """
    token = AuthInterface.login(db, user)["access_token"]
    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=False,  
        samesite="lax",
    )
    
    return {"message": "Successfully logged in"}


@rout.post("/logout", dependencies=[Depends(security.access_token_required)])
def logout(response: Response):
    """
    User logout and removal of JWT token from cookies
    """
    response.delete_cookie(key=config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "You are logged out"}

@rout.post("/reset_password", dependencies=[Depends(security.access_token_required)])
def reset_password(user: UserResetPassword, db: Session = Depends(get_db), token: TokenPayload = Depends(security.access_token_required)):
    """
    pass
    """
    return AuthInterface.reset_password(db, int(token.sub), user)

@rout.get("/me", dependencies=[Depends(security.access_token_required)], response_model=UserRead)
def get_me(db: Session = Depends(get_db), token: TokenPayload = Depends(security.access_token_required)):
    """
    Getting information about the current user using a JWT token
    """
    return UserInterface.get_user_by_id(db,token.sub)

