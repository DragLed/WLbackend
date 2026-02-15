from fastapi import HTTPException
from passlib.context import CryptContext
from authx import AuthX, AuthXConfig
from sqlalchemy.orm import Session
from models import Gift, User
from database import credentials


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


config = AuthXConfig()
config.JWT_SECRET_KEY = credentials["JWT_SECRET_KEY"]
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_CSRF_PROTECT = False


securuty = AuthX(config=config)

def hash_password(password: str) -> str:
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    password = password[:72]
    return pwd_context.verify(password, hashed_password)



class DataBaseInterface:

    @staticmethod
    def create_gift(db: Session, name, description, price, photo, user_id):
        gift = Gift(
            name=name,
            description=description,
            price=price,
            photo=photo,
            userId=user_id
        )
        db.add(gift)
        db.commit()
        db.refresh(gift)
        return gift


    @staticmethod
    def get_all_gifts_user(db: Session, id):
        result = db.query(Gift).filter(Gift.userId == id).all()
        return result
    
    @staticmethod
    def get_all_gifts(db: Session):
        result = db.query(Gift).all()
        return result
    
    @staticmethod
    def delete_gift(db: Session,id):
        gift = db.query(Gift).filter(Gift.id == id).first()
        if gift:
            db.delete(gift)
            db.commit()
            return {"message": "Подарок удалён"}
        return None

    @staticmethod
    def get_gift_by_id(db: Session, id):
        gift = db.query(Gift).filter(Gift.id == id).first()
        return gift
    

    @staticmethod
    def edit_gift_by_id(db: Session, id, name, description, price, photo):
        gift = db.query(Gift).filter(Gift.id == id).first()
        if not gift:
            return None
        gift.name = name
        gift.description = description
        gift.price = price
        gift.photo = photo
        db.commit()
        db.refresh(gift)

    
    @staticmethod
    def create_user(db: Session, username:str, password:str):
        user = db.query(User).filter(User.username == username).first()
        if user:
            raise HTTPException(status_code=409, detail="Логин уже используется")
        user = User(
        username=username,
        hashed_password=hash_password(password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


    @staticmethod
    def get_all_users(db: Session):
        result = db.query(User).all()
        return result


    @staticmethod
    def get_user_by_id(db: Session,id:str):
        user = db.query(User).filter(User.id == id).first()
        if user:
            return user
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    @staticmethod
    def login( username:str, password: str ,db: Session):
        user = db.query(User).filter(User.username == username).first()
        if not user:   
            raise HTTPException(status_code=401, detail="Неверный логин/почта или пароль")
        if verify_password(password, user.hashed_password):
            token = securuty.create_access_token(uid=str(user.id))
            return {"access_token": token}
        raise HTTPException(status_code=401, detail="Неверный логин/почта или пароль")
        
