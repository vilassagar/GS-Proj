from sqlalchemy import Column, String, Integer, ForeignKey, Index, Boolean, DateTime, Text, Float, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime
from app.config import Base
from app.models.base import TimestampMixin

class Book(Base, TimestampMixin):
    __tablename__ = 'books'
    
    # Use consistent Mapped style throughout
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey('departments.id'), index=True)
    file_path: Mapped[str] = mapped_column(String(500))
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))
    updated_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('users.id'))
    
    # Fixed: Use Mapped style and correct datetime function
    filename: Mapped[str] = mapped_column(String(255), unique=True)
    upload_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())  # Fixed: func.now() instead of DateTime.utcnow
    total_pages: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    
    # Add author field for Marathi books
    author: Mapped[Optional[str]] = mapped_column(String(300))
    
    # Relationships
    pages = relationship("Page", back_populates="book", cascade="all, delete-orphan")
    department: Mapped["Department"] = relationship("Department", back_populates="books", lazy="joined")
    
    # Table arguments
    __table_args__ = (
        Index('ix_books_title', 'title'),
        Index('ix_books_department_id', 'department_id'),
        Index('ix_books_filename', 'filename'),  # Added index for filename
    )

class Page(Base):
    __tablename__ = "pages"
    
    # Use consistent Mapped style
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id"), nullable=False)
    page_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    confidence_score: Mapped[Optional[float]] = mapped_column(Float)
    
    # Additional fields for better Marathi support
    word_count: Mapped[Optional[int]] = mapped_column(Integer)
    character_count: Mapped[Optional[int]] = mapped_column(Integer)
    language_detected: Mapped[Optional[str]] = mapped_column(String(10))  # 'mar', 'eng', 'mixed'
    processing_time: Mapped[Optional[float]] = mapped_column(Float)
    
    # Relationships
    book = relationship("Book", back_populates="pages")
    words = relationship("Word", back_populates="page", cascade="all, delete-orphan")
    
    # Table arguments for better performance
    __table_args__ = (
        Index('ix_pages_book_id', 'book_id'),
        Index('ix_pages_page_number', 'page_number'),
        Index('ix_pages_content_gin', 'content', postgresql_using='gin', postgresql_ops={'content': 'gin_trgm_ops'}),  # For trigram search
    )

class Word(Base):
    __tablename__ = "words"
    
    # Use consistent Mapped style
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    page_id: Mapped[int] = mapped_column(Integer, ForeignKey("pages.id"), nullable=False)
    word: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    x_position: Mapped[Optional[int]] = mapped_column(Integer)
    y_position: Mapped[Optional[int]] = mapped_column(Integer)
    width: Mapped[Optional[int]] = mapped_column(Integer)
    height: Mapped[Optional[int]] = mapped_column(Integer)
    confidence: Mapped[Optional[float]] = mapped_column(Float)
    
    # Additional fields for Marathi text processing
    is_marathi: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    font_size: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Relationships
    page = relationship("Page", back_populates="words")
    
    # Table arguments for better search performance
    __table_args__ = (
        Index('ix_words_page_id', 'page_id'),
        Index('ix_words_word', 'word'),
        Index('ix_words_position', 'x_position', 'y_position'),
        Index('ix_words_marathi', 'is_marathi'),
    )
