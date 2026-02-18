from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    gifts = relationship("Gift", back_populates="user", foreign_keys="Gift.userId", cascade="all, delete", passive_deletes=True)
    reserved_gifts = relationship("Gift", foreign_keys="Gift.reserved_by_id", back_populates="reserved_by")