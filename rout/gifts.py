from fastapi import FastAPI, HTTPException, Response, Depends, Request, APIRouter
from interface import DataBaseInterface, config, securuty
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from authx.exceptions import AuthXException
from sqlalchemy.orm import Session

from models import Base, UpdateGift, GiftView
from database import engine, SessionLocal
import uvicorn


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

rout = APIRouter(prefix="/gifts", tags=["Подарок"])




@rout.get("/")
def get_all_gifts(db: Session = Depends(get_db), token: dict = Depends(securuty.access_token_required)):
    user_id = token.sub
    gifts = DataBaseInterface.get_all_gifts(db, user_id) 
    if len(gifts) == 0:
        raise HTTPException(status_code=404, detail="Подарки пользователя не найдены")
    return gifts


@rout.post("/")
def create_gift(gift: GiftView, db: Session = Depends(get_db), token: dict = Depends(securuty.access_token_required)):
    """
    Добавление подарка
    """
    user_id = token.sub
    DataBaseInterface.create_gift(db, gift.name, gift.description, gift.price, gift.photo, user_id)
    return {"message": f"Подарок добавлен"}



@rout.delete("/{giftId}", dependencies=[Depends(securuty.access_token_required)])
def remove_gift(giftId: int, db: Session = Depends(get_db)):
    respone = DataBaseInterface.delete_gift(db,giftId)
    if respone: 
        return respone
    raise HTTPException(status_code=404, detail="Подарок не найден")


@rout.get("/{giftId}", dependencies=[Depends(securuty.access_token_required)])
def get_gift_by_id(giftId: int, db: Session = Depends(get_db)):
    gift = DataBaseInterface.get_gift_by_id(db,giftId)
    if gift:
        return gift
    raise HTTPException(status_code=404, detail="Подарок не найден")


@rout.put("/{giftId}", dependencies=[Depends(securuty.access_token_required)])
def edit_gift_by_id(giftId: int ,Viewgift: UpdateGift, db: Session = Depends(get_db)):
    gift = DataBaseInterface.get_gift_by_id(db,giftId)
    if gift:
        DataBaseInterface.edit_gift_by_id(db, giftId, Viewgift.name, Viewgift.description, Viewgift.price, Viewgift.photo)
        return {"message": f"Подарок с id: {giftId} обновлён"}
    else:
        raise HTTPException(status_code=404, detail="Подарок не найден")
    
@rout.post("/lol")
def test(token: dict = Depends(securuty.access_token_required)):
    return token

