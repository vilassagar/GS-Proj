from typing import Optional, Dict, Any, List
from sqlalchemy import String, Boolean, Enum as SQAEnum, ForeignKey, Integer, UniqueConstraint, Index, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import Base
from app.models.base import TimestampMixin
from app.models.enums.approval_status import ApprovalStatus
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.users import User

class DocumentType(Base, TimestampMixin):
    """
    Document types with dynamic field definitions
    """
    __tablename__ = 'document_types'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)  # Marathi name
    name_english: Mapped[Optional[str]] = mapped_column(String(200))  # English name
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Dynamic field definitions stored as JSON
    field_definitions: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # Category for grouping similar documents
    category: Mapped[Optional[str]] = mapped_column(String(100))  # e.g., 'EDUCATION', 'IDENTITY', 'SERVICE'
    
    # Instructions for the user
    instructions: Mapped[Optional[str]] = mapped_column(Text)

    created_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))
    updated_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))

    # Relationships - Fixed for Python 3.8
    user_documents: Mapped[List["UserDocument"]] = relationship("UserDocument", back_populates="document_type")


class UserDocument(Base, TimestampMixin):
    """
    User uploaded documents with dynamic field values
    """
    __tablename__ = 'user_documents'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    document_type_id: Mapped[int] = mapped_column(ForeignKey('document_types.id'))
    file_path: Mapped[str] = mapped_column(String(500))
    
    # Store dynamic field values as JSON
    field_values: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    verification_status: Mapped[str] = mapped_column(
        SQAEnum(ApprovalStatus),
        default=ApprovalStatus.PENDING
    )
    
    # Admin comments for verification
    admin_comments: Mapped[Optional[str]] = mapped_column(Text)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="documents", foreign_keys=[user_id])
    document_type: Mapped["DocumentType"] = relationship("DocumentType", back_populates="user_documents", lazy="joined")

    created_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))
    updated_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))

    __table_args__ = (
        UniqueConstraint('user_id', 'document_type_id', name='uq_user_document'),
        Index('ix_user_documents_verification_status', 'verification_status'),
    )