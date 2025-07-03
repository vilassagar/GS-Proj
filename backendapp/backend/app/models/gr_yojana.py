from datetime import date
from sqlalchemy import String, Date, ForeignKey, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING
from app.config import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.department import Department


class Yojana(Base, TimestampMixin):
    __tablename__ = 'yojanas'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    grs: Mapped[List["GR"]] = relationship("GR", back_populates="yojana")


class GR(Base, TimestampMixin):
    __tablename__ = 'grs'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    gr_number: Mapped[str] = mapped_column(String(50), unique=True)
    gr_code: Mapped[Optional[str]] = mapped_column(String(50), unique=True)
    subject: Mapped[Optional[str]] = mapped_column(String(50), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey('departments.id'), index=True)
    effective_date: Mapped[date] = mapped_column(Date, index=True)
    yojana_id: Mapped[int] = mapped_column(ForeignKey('yojanas.id'))
    file_path: Mapped[str] = mapped_column(String(500))
    created_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))
    updated_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))

    yojana: Mapped["Yojana"] = relationship("Yojana", back_populates="grs")
    department: Mapped["Department"] = relationship("Department", back_populates="grs", lazy="joined")

    __table_args__ = (
        Index('ix_gr_department_id_effective_date', 'department_id', 'effective_date'),
    )
