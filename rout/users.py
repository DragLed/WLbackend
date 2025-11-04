from fastapi import HTTPException, Response, Depends,  APIRouter
from interface import DataBaseInterface, config, securuty
from sqlalchemy.orm import Session

from models import UserLogin, UserView
from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


rout = APIRouter(prefix="/users", tags=["Пользователь"])

@rout.post("/")
def create_user(user: UserView, db: Session = Depends(get_db)):
    DataBaseInterface.create_user(db, user.username, user.email, user.password)
    return {"login": user.username,"email": user.email, "message": "Пользователь создан"}


@rout.get("/")
def get_all_users(db: Session = Depends(get_db)):
    result = DataBaseInterface.get_all_users(db)
    return result

@rout.get("/me", dependencies=[Depends(securuty.access_token_required)])
def get_me(db: Session = Depends(get_db), token: dict = Depends(securuty.access_token_required)):
    userId = token.sub
    result = DataBaseInterface.get_user_data(db,userId)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@rout.get("/{userId}")
def get_user(userId:str, db: Session = Depends(get_db)):
    result = DataBaseInterface.get_user_data(db,userId)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Пользователь не найден")




@rout.post("/verify_password")
def verify_password(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    token = DataBaseInterface.verify_password(user.username, user.password,db)["access_token"]
    if token:
        response.set_cookie(
            key=config.JWT_ACCESS_COOKIE_NAME,
            value=token,
            httponly=True,
            secure=False,  
            samesite="Lax" 
        )
        return {"message": token}
    raise HTTPException(status_code=404, detail="Пользователь не найден")

