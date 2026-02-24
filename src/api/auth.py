from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.users import User
from schemas.users import UserCreate, UserResetPassword
from config.auth import verify_password, hash_password
from config.cookie import security


class AuthInterface:
    @staticmethod
    def login(db: Session, UserCreate: UserCreate):
        user = db.query(User).filter(User.username == UserCreate.username).first()
        if not user:
            raise HTTPException(
                status_code=401, detail="Invalid username/email or password"
            )
        if verify_password(UserCreate.password, user.hashed_password):
            token = security.create_access_token(uid=str(user.id))
            return {"access_token": token}
        raise HTTPException(
            status_code=401, detail="Invalid username/email or password"
        )

    @staticmethod
    def create_user(db: Session, UserCreate: UserCreate):
        user = db.query(User).filter(User.username == UserCreate.username).first()
        if user:
            raise HTTPException(
                status_code=409, detail="The username is already in use"
            )
        user = User(
            username=UserCreate.username,
            hashed_password=hash_password(UserCreate.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def reset_password(db: Session, userId: int, UserResetPassword: UserResetPassword):
        user = db.query(User).filter(User.id == userId).first()
        if user:
            if verify_password(UserResetPassword.oldPassword, user.hashed_password):
                user.hashed_password = hash_password(UserResetPassword.newPassword)
                db.commit()
                db.refresh(user)
                return "ok"
            raise HTTPException(
                status_code=401, detail="Invalid username/email or password"
            )
        raise HTTPException(status_code=404, detail="No user found")
