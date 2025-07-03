from typing import List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.users import User


class District(Base, TimestampMixin):
    __tablename__ = 'districts'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    
    users: Mapped[List["User"]] = relationship("User", back_populates="district")
    blocks: Mapped[List["Block"]] = relationship("Block", back_populates="district")  # Keep only one

class Block(Base, TimestampMixin):
    """
        Block -> Panchayat Samiti
    """
    __tablename__ = 'blocks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    district_id: Mapped[int] = mapped_column(ForeignKey('districts.id'), index=True)

    district: Mapped["District"] = relationship("District", back_populates="blocks")
    gram_panchayats: Mapped[List["GramPanchayat"]] = relationship("GramPanchayat", back_populates="block")

    users: Mapped[List["User"]] = relationship("User", back_populates="block")

    __table_args__ = (
        Index('ix_block_district_name', 'district_id', 'name'),
    )


class GramPanchayat(Base, TimestampMixin):
    __tablename__ = 'gram_panchayats'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    block_id: Mapped[int] = mapped_column(ForeignKey('blocks.id'), index=True)

    block: Mapped["Block"] = relationship("Block", back_populates="gram_panchayats")

    users: Mapped[List["User"]] = relationship("User", back_populates="gram_panchayat")

    __table_args__ = (
        Index('ix_gram_panchayat_block_name', 'block_id', 'name'),
    )
