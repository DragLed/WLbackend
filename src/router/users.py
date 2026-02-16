from fastapi import HTTPException, Response, Depends, APIRouter
from api.users import UserInterface
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
def get_user(Id:str, db: Session = Depends(get_db)):
    """
    Getting information about a user by ID
    """
    return UserInterface.get_user_by_id(db,Id)


@rout.delete('/{Id}', dependencies=[Depends(security.access_token_required)])
def remove_user(response: Response, Id: str, db: Session = Depends(get_db), token: dict = Depends(security.access_token_required)):
    """
    Delete a user by ID.
    """
    user_id = token.sub
    if user_id == Id:
        response.delete_cookie(key=config.JWT_ACCESS_COOKIE_NAME)
        return UserInterface.delete_user(db,Id)
    raise HTTPException(status_code=403, detail="Access denied")
    

