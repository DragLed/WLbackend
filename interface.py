from fastapi import HTTPException
from sqlalchemy import text
from database import engine  
from passlib.context import CryptContext
from authx import AuthX, AuthXConfig
from sqlalchemy.orm import Session
from models import Gift, User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


config = AuthXConfig()
config.JWT_SECRET_KEY = "DRAGled"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

securuty = AuthX(config=config)

# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(password, hashed_password)



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
        db.close()
        return gift


    @staticmethod
    def get_all_gifts(db: Session, id):
        result = db.query(Gift).filter(Gift.userId == id).all()
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
        gift.name = name
        gift.description = description
        gift.price = price
        gift.photo = photo
        db.commit()
        db.refresh(gift)

    
    @staticmethod
    def create_user(db: Session, username:str, email: str, hashed_password:str):
        user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()
        return user


    @staticmethod
    def get_all_users(db: Session):
        result = db.query(User).all()
        return result



    @staticmethod
    def get_user_data(db: Session, userId: str):
        result = db.get(User, userId)
        db.close()
        return result


    @staticmethod
    def get_user_by_id(id:str):
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM users WHERE id = :id"),
                {"id": id}
                ).fetchone()
            return dict(result._mapping) if result else None

    @staticmethod
    def verify_password(login_or_email:str, password: str):
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM users WHERE login = :v"),
                {"v": login_or_email}
            ).fetchone()
            if not result:
                result = conn.execute(
                text("SELECT * FROM users WHERE email = :v"),
                {"v": login_or_email}
            ).fetchone()
            if not result:
                raise HTTPException(status_code=401, detail="Неверный логин/почта или пароль")
            user  = dict(result._mapping)
            if password == user["hashed_password"]:
                token = securuty.create_access_token(uid=str(user["id"]))
                return {"access_token": token}
            raise HTTPException(status_code=401, detail="Неверный логин/почта или пароль")


