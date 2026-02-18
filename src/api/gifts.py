from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.gifts import Gift
from schemas.gifts import GiftCreate


class GiftInterface:

    
    @staticmethod
    def create_gift(db: Session, GiftCreate:GiftCreate, user_id):
        gift = Gift(
            name=GiftCreate.name,
            description=GiftCreate.description,
            price=GiftCreate.price,
            photo=GiftCreate.photo,
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
    def edit_gift_by_id(db: Session, gift_id:int, GiftEdit:GiftCreate, user_id:int):
        gift = db.query(Gift).filter(Gift.id == gift_id).first()
        if gift:
            if gift.userId == int(user_id):
                gift.name = GiftEdit.name
                gift.description = GiftEdit.description
                gift.price = GiftEdit.price
                gift.photo = GiftEdit.photo
                db.commit()
                db.refresh(gift)
                return {"message": "Gift edited"}
            raise HTTPException(status_code=403, detail="Access denied") 
        raise HTTPException(status_code=404, detail="Gift not found")
    

    @staticmethod
    def reserve_gift(db: Session, gift_id:int, user_id:int):
        gift = db.query(Gift).filter(Gift.id == gift_id).first()
        if gift:
            if gift.userId != int(user_id):
                if gift.is_reserved == False:
                    gift.is_reserved = True
                    db.commit()
                    db.refresh(gift)
                    return {"message": "gift id reserved"}
                return {"message": "gift has already been booked"}
            raise HTTPException(status_code=403, detail="this is your gift") 
        raise HTTPException(status_code=404, detail="Gift not found")
    

    @staticmethod
    def unreserve_gift(db: Session, gift_id:int, user_id:int):
        gift = db.query(Gift).filter(Gift.id == gift_id).first()
        if gift:
            if gift.userId != int(user_id):
                if gift.is_reserved == True:
                    gift.is_reserved = False
                    db.commit()
                    db.refresh(gift)
                    return {"message": "gift id unreserved"}
                return {"message": "gift hasn't already been booked"}
            raise HTTPException(status_code=403, detail="this is your gift") 
        raise HTTPException(status_code=404, detail="Gift not found")

        
