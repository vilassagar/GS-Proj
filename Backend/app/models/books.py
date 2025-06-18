from sqlalchemy import String, Integer, ForeignKey, Index, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.config import Base
from app.models.base import TimestampMixin


class Book(Base, TimestampMixin):

    '''

    '''

    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey('departments.id'), index=True)
    file_path: Mapped[str] = mapped_column(String(500))
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))
    updated_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))

    department: Mapped["Department"] = relationship("Department", back_populates="books", lazy="joined")

    __table_args__ = (
        Index('ix_books_title', 'title'),
        Index('ix_books_department_id', 'department_id'),
    )

    # Not needed
    # category: Mapped[Optional[str]] = mapped_column(String(100))
