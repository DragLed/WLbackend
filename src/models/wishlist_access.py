import enum
from datetime import datetime
from sqlalchemy import ForeignKey, Enum, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base
from core.enums import WishlistRole

class WishlistAccess(Base):
    __tablename__ = "wishlist_accesses"

    __table_args__ = (
        UniqueConstraint("wishlist_id", "user_id", name="uq_wishlist_user"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    wishlist_id: Mapped[int] = mapped_column(
        ForeignKey("wishlists.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
    DateTime,
    default=datetime.utcnow,
    nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    invited_by_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False
    )

    wishlist = relationship("Wishlist", back_populates="accesses")

    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="wishlist_accesses"
    )

    role: Mapped[WishlistRole] = mapped_column(
        Enum(WishlistRole),
        nullable=False, 
        name="role"
    )

    invited_by = relationship(
    "User",
    foreign_keys=[invited_by_id],
    back_populates="invited_accesses"
    )


    
