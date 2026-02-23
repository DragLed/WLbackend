from sqlalchemy.orm import Session
from schemas.wishlists import WishlistBase
from core.enums import WishlistVisibility
from fastapi import HTTPException
from models.wishlist import Wishlist





class WishlistInterface:

    @staticmethod
    def create_wishlist(db: Session, wishlist: WishlistBase, owner_id: int, visibility:WishlistVisibility):
        wl = Wishlist(  title=wishlist.title,
                        description= wishlist.description, 
                        owner_id=owner_id, 
                        visibility=visibility
                        )
        db.add(wl)
        db.commit()
        db.refresh(wl)
        return {"message": "Wishlist added"}
    
    @staticmethod
    def get_all_wishlists(db: Session):
        wishlists = db.query(Wishlist).all()
        if len(wishlists) > 0:
            return wishlists
        raise HTTPException(status_code=404, detail="Not found")
    
    @staticmethod
    def get_all_user_wishlist(db: Session, userId:int):
        wishlists = db.query(Wishlist).filter(Wishlist.owner_id == userId).all()
        if len(wishlists) > 0:
            return wishlists
        raise HTTPException(status_code=404, detail="Not found")
    
    @staticmethod
    def get_wishlist(db: Session, id:int):
        wishlists = db.query(Wishlist).filter(Wishlist.id == id).first()
        if wishlists:
            return wishlists
        raise HTTPException(status_code=404, detail="Not found")
    
    @staticmethod
    def delete_wishlist(db: Session, wlid: int, userId:int):
        wishlists = db.query(Wishlist).filter(Wishlist.id == wlid).first()
        if wishlists:
            if int(wishlists.owner_id) == int(userId):
                db.delete(wishlists)
                db.commit()
                return {"message": "wishlists deleted"}
            raise HTTPException(status_code=401, detail="Access denied")
        raise HTTPException(status_code=404, detail="Not found")
