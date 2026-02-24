from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    wishlists: Mapped[list["Wishlist"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )

    wishlist_accesses = relationship(
        "WishlistAccess",
        foreign_keys="[WishlistAccess.user_id]",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    reserved_gifts: Mapped[list["Gift"]] = relationship(back_populates="reserved_by")

    invited_accesses = relationship(
        "WishlistAccess",
        foreign_keys="[WishlistAccess.invited_by_id]",
        back_populates="invited_by",
    )
