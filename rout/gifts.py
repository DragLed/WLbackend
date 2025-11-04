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


@rout.post("/",
    response_model=str,
    summary="Добавляет подарок",
    description="Добавляет подарок из вводимых данных",
    responses={
        200: {"description": "Успешно", "model": str},
        403: {"description": "Доступ не разрешен", "model": str},
        404: {"description": "Подарок не найден", "model": str},
    })
def create_gift(gift: GiftView, db: Session = Depends(get_db)):
    """
    Добавление подарка
    """
    DataBaseInterface.create_gift(db, gift.name, gift.description, gift.price, gift.photo, gift.user_id)
    return "Подарок дабавлен"


@rout.get("/jwt/{id}")
def get_all_gifts(id:int, db: Session = Depends(get_db)):
    gifts = DataBaseInterface.get_all_gifts(db,id) 
    if len(gifts) == 0:
        raise HTTPException(status_code=404, detail="Подарки пользователя не найдены")
    return gifts


@rout.delete("/{giftId}")
def remove_gift(giftId: int, db: Session = Depends(get_db)):
    respone = DataBaseInterface.delete_gift(db,giftId)
    if respone: 
        return respone
    raise HTTPException(status_code=404, detail="Подарок не найден")


@rout.get("/{giftId}")
def get_gift_by_id(giftId: int, db: Session = Depends(get_db)):
    gift = DataBaseInterface.get_gift_by_id(db,giftId)
    if gift:
        return gift
    raise HTTPException(status_code=404, detail="Подарок не найден")


@rout.put("/{giftId}")
def edit_gift_by_id(giftId: int ,Viewgift: UpdateGift, db: Session = Depends(get_db)):
    gift = DataBaseInterface.get_gift_by_id(db,giftId)
    if gift:
        DataBaseInterface.edit_gift_by_id(db, giftId, Viewgift.name, Viewgift.description, Viewgift.price, Viewgift.photo)
        return {"message": f"Подарок с id: {giftId} обновлён"}
    else:
        raise HTTPException(status_code=404, detail="Подарок не найден")
    



