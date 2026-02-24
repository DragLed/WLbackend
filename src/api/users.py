from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.users import User


class UserInterface:
    @staticmethod
    def get_all_users(db: Session):
        result = db.query(User).all()
        if len(result) > 0:
            return result
        raise HTTPException(status_code=404, detail="No users found")

    @staticmethod
    def get_user_by_id(db: Session, id: str):
        user = db.query(User).filter(User.id == id).first()
        if user:
            return user
        raise HTTPException(status_code=404, detail="No user found")

    @staticmethod
    def delete_user(db: Session, id: str):
        user = db.query(User).filter(User.id == id).first()
        if user:
            db.delete(user)
            db.commit()
            return {"message": "User deleted"}
        raise HTTPException(status_code=404, detail="No user found")
