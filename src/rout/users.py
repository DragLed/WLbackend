from fastapi import HTTPException, Response, Depends,  APIRouter
from api.users import UserInterface
from config.cookie import security, config
from sqlalchemy.orm import Session

from schemas.users import UserCreate, UserRead
from database import get_db


rout = APIRouter(prefix="/users", tags=["User"])

@rout.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Creating a user
    """
    return UserInterface.create_user(db, user.username, user.password)
     


@rout.get("/", response_model=list[UserRead])
def get_all_users(db: Session = Depends(get_db)):
    """
    Getting all users
    """
    return UserInterface.get_all_users(db)






@rout.get("/me", dependencies=[Depends(security.access_token_required)], response_model=UserRead)
def get_me(db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Getting information about the current user using a JWT token
    """
    Id = token.sub
    result = UserInterface.get_user_by_id(db,Id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="The user was not found")


@rout.get("/{Id}", response_model=UserRead)
def get_user(Id:str, db: Session = Depends(get_db)):
    """
    Getting information about a user by ID
    """
    result = UserInterface.get_user_by_id(db,Id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="The user was not found")




@rout.post("/login")
def login(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    """
    Checking the user's login and password and creating a JWT token
    """
    token = UserInterface.login(user.username, user.password,db)["access_token"]
    if token:
        response.set_cookie(
            key=config.JWT_ACCESS_COOKIE_NAME,
            value=token,
            httponly=True,
            secure=False,  
            samesite="lax",
        )
        return {"message": "Successfully logged in"}
    raise HTTPException(status_code=404, detail="The user was not found")

@rout.post("/logout", dependencies=[Depends(security.access_token_required)])
def logout(response: Response):
    """
    User logout and removal of JWT token from cookies
    """
    response.delete_cookie(key=config.JWT_ACCESS_COOKIE_NAME)
    return {"message": "You are logged out"}
