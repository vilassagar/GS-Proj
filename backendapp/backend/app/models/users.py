from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import String, Enum as SQAEnum, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import Base
from app.models.roles import Role
from app.models.base import TimestampMixin
from app.models.enums.approval_status import ApprovalStatus
from app.models.enums.user_designation import UserDesignation
from app.models.users_hierarchy import District, Block, GramPanchayat

if TYPE_CHECKING:
    from app.models.documents import UserDocument
    from app.models.otp import UserOTP

class User(Base, TimestampMixin):
    __tablename__ = 'users'

    # Todo check what all cols to make mandatory
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    mobile_number: Mapped[str] = mapped_column(String(15), unique=True)
    whatsapp_number: Mapped[Optional[str]] = mapped_column(String(15), unique=True)

    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=False)

    # Todo check proper names
    designation: Mapped["UserDesignation"] = mapped_column(SQAEnum(UserDesignation))

    # Add indexes to foreign key columns if frequently queried
    district_id: Mapped[Optional[int]] = mapped_column(ForeignKey('districts.id'), index=True)
    block_id: Mapped[Optional[int]] = mapped_column(ForeignKey('blocks.id'), index=True)
    gram_panchayat_id: Mapped[Optional[int]] = mapped_column(ForeignKey('gram_panchayats.id'), index=True)

    status: Mapped[ApprovalStatus] = mapped_column(
        SQAEnum(ApprovalStatus),
        default=ApprovalStatus.PENDING
    )

    created_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('users.id')
    )

    updated_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('users.id')
    )

    documents_uploaded: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)

    # Relations - Use string references to avoid circular imports
    role: Mapped["Role"] = relationship("Role", back_populates="users")
    
    # Use string references for documents to avoid circular imports
    documents: Mapped[List["UserDocument"]] = relationship(
        "UserDocument",
        back_populates="user",
        foreign_keys="[UserDocument.user_id]",
        cascade="all, delete-orphan"
    )

    district: Mapped["District"] = relationship("District", back_populates="users")
    block: Mapped["Block"] = relationship("Block", back_populates="users")
    gram_panchayat: Mapped["GramPanchayat"] = relationship("GramPanchayat", back_populates="users")

    # For now storing OTP's for user as single entry only instead of List of OTPs
    otp: Mapped["UserOTP"] = relationship("UserOTP", back_populates="user", uselist=False)