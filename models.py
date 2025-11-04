from sqlalchemy import Column, Integer, String, Numeric,DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr
from typing import Optional


Base = declarative_base() 

class Gift(Base):
    __tablename__ = "gifts" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Numeric(10,2), nullable=False)
    photo = Column(String(255), nullable=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="gifts")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    gifts = relationship("Gift", back_populates="user",cascade="all, delete", passive_deletes=True)


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class GiftView(BaseModel):
    name: str
    description: str | None
    price: int
    photo: str | None

class UpdateGift(BaseModel):
    name: str
    description: str | None
    price: int
    photo: str | None

class UserView(BaseModel):
    username: str
    email: EmailStr
    password: str