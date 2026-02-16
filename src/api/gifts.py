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
        return {"message": "Gift added"}


    @staticmethod
    def get_all_gifts_user(db: Session, id):
        result = db.query(Gift).filter(Gift.userId == id).all()
        if len(result) > 0:
            return result
        raise HTTPException(status_code=404, detail="No gifts found for this user")
    
    @staticmethod
    def get_all_gifts(db: Session):
        result = db.query(Gift).all()
        if len(result) > 0:
            return result
        raise HTTPException(status_code=404, detail="No gifts found for this user")
    
    @staticmethod
    def delete_gift(db: Session, giftid: str, userId:int):
        gift = db.query(Gift).filter(Gift.id == giftid).first()
        if gift:
            if gift.userId == int(userId):
                db.delete(gift)
                db.commit()
                return {"message": "Gift deleted"}
            raise HTTPException(status_code=403, detail="Access denied") 
        raise HTTPException(status_code=404, detail="No gift found")

    @staticmethod
    def get_gift_by_id(db: Session, id):
        gift = db.query(Gift).filter(Gift.id == id).first()
        if gift:   
            return gift
        raise HTTPException(status_code=404, detail="Gift not found")
    

    @staticmethod
    def edit_gift_by_id(db: Session, id,UserId:int, name, description, price, photo,):
        gift = db.query(Gift).filter(Gift.id == id).first()
        if gift:
            if gift.userId == int(UserId):
                gift.name = name
                gift.description = description
                gift.price = price
                gift.photo = photo
                db.commit()
                db.refresh(gift)
                return {"message": "Gift edited"}
            raise HTTPException(status_code=403, detail="Access denied") 
        raise HTTPException(status_code=404, detail="Gift not found")
