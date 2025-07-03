from datetime import datetime
from sqlalchemy import DateTime, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.users import User


class UserOTP(Base):
    __tablename__ = "user_otps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # ensures one OTP per user
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    otp: Mapped[str] = mapped_column(String(6), nullable=False)

    # For now storing UTC datetime for OTP expiry time
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    message_sid: Mapped[str] = mapped_column(String(50), nullable=True)

    # Adjust relationship back_populates to match User's definition.
    user: Mapped["User"] = relationship("User", back_populates="otp", uselist=False)

    # table-level constraint:
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_userotp_user_id"),
    )
