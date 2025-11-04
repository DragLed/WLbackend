from fastapi import FastAPI, HTTPException, Response, Depends, Request, APIRouter
from interface import DataBaseInterface, config, securuty
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from authx.exceptions import AuthXException
from sqlalchemy.orm import Session

from models import Base, UserLogin, UserView
from database import engine, SessionLocal
import uvicorn


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


@rout.get("/{userId}")
def get_user(userId:str, db: Session = Depends(get_db)):
    result = DataBaseInterface.get_user_data(db,userId)
    return result


@rout.get("/{JWT}")
def get_user_by_JWT(JWT:str, db: Session = Depends(get_db)):
    token = securuty._decode_token(JWT)
    return DataBaseInterface.get_user_by_id(db ,token.sub)


@rout.post("/verify_password")
def verify_password(user_data: UserLogin, response: Response, db: Session = Depends(get_db)):
    token = DataBaseInterface.verify_password(db, user_data.username, user_data.password)["access_token"]
    
    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=False,  
        samesite="Lax" 
    )
    
    return {"message": token}

