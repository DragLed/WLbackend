import enum
import secrets
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base
from core.enums import WishlistVisibility


class Wishlist(Base):
    __tablename__ = "wishlists"

    id: Mapped[int] = mapped_column(primary_key=True)

    owner_id: Mapped[int] = mapped_column(
    ForeignKey("users.id", ondelete="CASCADE"),
    nullable=False,
    index=True
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    visibility: Mapped[WishlistVisibility] = mapped_column(
        Enum(WishlistVisibility),
        default=WishlistVisibility.private,
        nullable=False, 
        name="visibility"
    )

    share_token: Mapped[str | None] = mapped_column(
        String(64),
        unique=True,
        index=True
    )

    owner: Mapped["User"] = relationship(back_populates="wishlists")

    gifts: Mapped[list["Gift"]] = relationship(
        back_populates="wishlist",
        cascade="all, delete-orphan"
    )

    accesses: Mapped[list["WishlistAccess"]] = relationship(
        back_populates="wishlist",
        cascade="all, delete-orphan"
    )

    def generate_share_token(self) -> None:
        self.share_token = secrets.token_urlsafe(32)