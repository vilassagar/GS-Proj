from sqlalchemy import String, Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload
from typing import List, Optional, TYPE_CHECKING
from app.config import Base
from app.models.base import TimestampMixin
from app.models.books import Book

if TYPE_CHECKING:
    from app.models.gr_yojana import GR


class Department(Base, TimestampMixin):
    """
        Department Model
    """
    __tablename__ = 'departments'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    books: Mapped[List["Book"]] = relationship("Book", back_populates="department")
    grs: Mapped[List["GR"]] = relationship("GR", back_populates="department")
