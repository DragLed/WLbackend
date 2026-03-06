from fastapi import Depends, APIRouter
from authx.schema import TokenPayload
from sqlalchemy.orm import Session
from api.gifts import GiftInterface
from config.cookie import security
from database.database import get_db
from schemas.gifts import GiftResponse, GiftCreate

rout = APIRouter(prefix="/gifts", tags=["Gift"])


