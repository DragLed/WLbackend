from fastapi import HTTPException, Depends, APIRouter
from api.users import UserInterface
from sqlalchemy.orm import Session
from schemas.users import UserRead
from database.database import get_db
from config.cookie import security


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
def remove_user(Id: str, db: Session = Depends(get_db)):
    """
    Delete a user by ID.
    """
    return UserInterface.delete_gift(db,Id)

