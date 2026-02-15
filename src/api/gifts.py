from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.gifts import Gift

class GiftInterface:
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
            return {"message": "Gift deleted"}
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