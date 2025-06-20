from typing import Optional
from sqlalchemy import String, Boolean, Enum as SQAEnum, ForeignKey, Integer, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import Base
from app.models.base import TimestampMixin
from app.models.enums.approval_status import ApprovalStatus


class DocumentType(Base, TimestampMixin):

    # Todo write get and post(with user) endpoint for this

    """
        GramSevak Of pune Specific documents. Mandatory and non-mandatory
    """

    __tablename__ = 'document_types'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    name_english: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    is_mandatory: Mapped[bool] = mapped_column(Boolean, default=True)

    created_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('users.id')
    )

    updated_by: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('users.id')
    )


class UserDocument(Base, TimestampMixin):

    """
        Documents specific to users
    """

    __tablename__ = 'user_documents'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    document_type_id: Mapped[int] = mapped_column(ForeignKey('document_types.id'))
    file_path: Mapped[str] = mapped_column(String(500))

    verification_status: Mapped[str] = mapped_column(
        # Todo create seperate enums instead of using directly
        SQAEnum(ApprovalStatus),
        # By default documents will be verified
        default=ApprovalStatus.APPROVED
    )

    # Relationships
    # user: Mapped["User"] = relationship(back_populates="documents")
    user: Mapped["User"] = relationship("User", back_populates="documents")
    document_type: Mapped["DocumentType"] = relationship("DocumentType", lazy="joined")

    created_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))
    updated_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))

    user: Mapped["User"] = relationship("User", back_populates="documents",
                                        foreign_keys=[user_id])

    __table_args__ = (
        # Ensure a user can only have one document per document type.
        # todo check whether we need unique constraint
        UniqueConstraint('user_id', 'document_type_id', name='uq_user_document'),
        Index('ix_user_documents_verification_status', 'verification_status'),
    )
