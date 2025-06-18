from typing import List, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import Base
from app.models.base import TimestampMixin


class Role(Base, TimestampMixin):
    __tablename__ = 'roles'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    # Relationships
    users: Mapped[List["User"]] = relationship(back_populates="role")
