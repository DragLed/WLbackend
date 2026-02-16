from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class Gift(Base):
    __tablename__ = "gifts" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Numeric(10,2), nullable=False)
    photo = Column(String(255), nullable=True)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="gifts")
