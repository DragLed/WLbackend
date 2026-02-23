from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.gifts import Gift
from models.wishlist import Wishlist
from schemas.gifts import GiftCreate


class GiftInterface:


    @staticmethod
    def create_gift(db: Session, gift:GiftCreate, user_id):
        wishlist = db.query(Wishlist).filter(Wishlist.id == gift.wishlist_id).first()
        if not wishlist:
            raise HTTPException(status_code=404, detail="Wishlist not found")
        if wishlist.owner_id != int(user_id):
            raise HTTPException(status_code=403, detail="You cannot add gifts to this wishlist")

        newGift = Gift( 
            title = gift.title,
            description = gift.description,
            price = gift.price,
            photo = gift.photo,
            wishlist_id = gift.wishlist_id,
        )
        db.add(newGift)
        db.commit()
        db.refresh(newGift)
        return {"message": "Gift added"}
    

    @staticmethod
    def get_all_gifts_from_wishlist(db: Session, wishlist_id:int):
        result = db.query(Gift).filter(Gift.wishlist_id == wishlist_id).all()
        if len(result) > 0:
            return result
        raise HTTPException(status_code=404, detail="Not found")
    

    @staticmethod
    def get_gift_by_id(db: Session, id):
        gift = db.query(Gift).filter(Gift.id == id).first()
        if gift:   
            return gift
        raise HTTPException(status_code=404, detail="Gift not found")

    @staticmethod
    def delete_gift(db: Session, giftid: str, userId:int):
        gift = db.query(Gift).filter(Gift.id == giftid).first()
        wishlist = db.query(Wishlist).filter(Wishlist.owner_id == userId).first()
        if gift:
            if gift.wishlist_id == wishlist.id:
                db.delete(gift)
                db.commit()
                return {"message": "Gift deleted"}
            raise HTTPException(status_code=403, detail="Access denied") 
        raise HTTPException(status_code=404, detail="No gift found")


    
    

    # @staticmethod
    # def edit_gift_by_id(db: Session, gift_id:int, GiftEdit:GiftBase, user_id:int):
    #     gift = db.query(Gift).filter(Gift.id == gift_id).first()
    #     if gift:
    #         if gift.userId == int(user_id):
    #             gift.title = GiftEdit.title
    #             gift.description = GiftEdit.description
    #             gift.price = GiftEdit.price
    #             gift.photo = GiftEdit.photo
    #             db.commit()
    #             db.refresh(gift)
    #             return {"message": "Gift edited"}
    #         raise HTTPException(status_code=403, detail="Access denied") 
    #     raise HTTPException(status_code=404, detail="Gift not found")
    

    # @staticmethod
    # def reserve_gift(db: Session, gift_id:int, user_id:int):
    #     gift = db.query(Gift).filter(Gift.id == gift_id).first()
    #     if gift:
    #         if gift.userId != int(user_id):
    #             if gift.is_reserved == False:
    #                 gift.is_reserved = True
    #                 db.commit()
    #                 db.refresh(gift)
    #                 return {"message": "gift id reserved"}
    #             return {"message": "gift has already been booked"}
    #         raise HTTPException(status_code=403, detail="this is your gift") 
    #     raise HTTPException(status_code=404, detail="Gift not found")
    

    # @staticmethod
    # def unreserve_gift(db: Session, gift_id:int, user_id:int):
    #     gift = db.query(Gift).filter(Gift.id == gift_id).first()
    #     if gift:
    #         if gift.userId != int(user_id):
    #             if gift.is_reserved == True:
    #                 gift.is_reserved = False
    #                 db.commit()
    #                 db.refresh(gift)
    #                 return {"message": "gift id unreserved"}
    #             return {"message": "gift hasn't already been booked"}
    #         raise HTTPException(status_code=403, detail="this is your gift") 
    #     raise HTTPException(status_code=404, detail="Gift not found")

        
