from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.users import User
from config.auth import hash_password, verify_password
from config.cookie import security

class UserInterface:



    @staticmethod
    def create_user(db: Session, username:str, password:str):
        user = db.query(User).filter(User.username == username).first()
        if user:
            raise HTTPException(status_code=409, detail="The username is already in use")
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
        if len(result) > 0:
            return result
        raise HTTPException(status_code=404, detail="No users found")


    @staticmethod
    def get_user_by_id(db: Session,id:str):
        user = db.query(User).filter(User.id == id).first()
        if user:
            return user
        raise HTTPException(status_code=404, detail="No user found")

    @staticmethod
    def login( username:str, password: str ,db: Session):
        user = db.query(User).filter(User.username == username).first()
        if not user:   
            raise HTTPException(status_code=401, detail="Invalid username/email or password")
        if verify_password(password, user.hashed_password):
            token = security.create_access_token(uid=str(user.id))
            return {"access_token": token}
        raise HTTPException(status_code=401, detail="Invalid username/email or password")