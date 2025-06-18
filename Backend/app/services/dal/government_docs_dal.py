from datetime import date
from typing import List

from sqlalchemy.orm import Session
from typing_extensions import Optional

from app.models import Book, GR
from app.services.dal.dto.book_dto import BookDTO
from app.services.dal.dto.gr_yojana_dto import GRDTO


class GovernmentDocsDal:

    # ##################### BOOKS ##########################
    @staticmethod
    def create_book(db: Session, title: str, department_id: int, file_path: str,
                    created_by: Optional[int] = None):
        book = Book(
            title=title,
            department_id=department_id,
            file_path=file_path,
            created_by=created_by
        )
        db.add(book)
        db.commit()
        db.refresh(book)

    # @staticmethod
    # def get_book_by_id(db: Session, book_id: int) -> Optional[BookDTO]:
    #     book = db.query(Book).filter(Book.id == book_id, Book.is_active).first()
    #     return BookDTO.to_dto(book) if book else None
    #
    # @staticmethod
    # def get_books_by_department(db: Session, department: str) -> List[BookDTO]:
    #     books = db.query(Book).filter(Book.department == department, Book.is_active).all()
    #     return [BookDTO.to_dto(book) for book in books]

    @staticmethod
    def get_books(db: Session) -> List[BookDTO]:
        books = db.query(Book).all()
        return [BookDTO.to_dto(book).to_camel() for book in books]

    # @staticmethod
    # def update_book(db: Session, book_id: int, **kwargs) -> Optional[Book]:
    #     book = db.query(Book).filter(Book.id == book_id, Book.is_active).first()
    #     if not book:
    #         return None
    #
    #     for key, value in kwargs.items():
    #         if hasattr(book, key):
    #             setattr(book, key, value)
    #     db.commit()
    #     db.refresh(book)
    #     return book
    #
    # @staticmethod
    # def delete_book(db: Session, book_id: int) -> bool:
    #     book = db.query(Book).filter(Book.id == book_id, Book.is_active).first()
    #     if not book:
    #         return False
    #     book.is_active = False
    #     db.commit()
    #     return True

    # ##################### GRS ##########################

    @staticmethod
    def create_gr(db: Session, gr_number: str, gr_code: str, department_id: int, yojana_id: int, subject: str,
                  effective_date: date, file_path: str, created_by: Optional[int] = None
                  ):
        gr = GR(
            gr_number=gr_number,
            gr_code=gr_code,
            department_id=department_id,
            yojana_id=yojana_id,
            subject=subject,
            effective_date=effective_date,
            file_path=file_path,
            created_by=created_by
        )
        db.add(gr)
        db.commit()
        db.refresh(gr)
        # return gr

    @staticmethod
    def get_gr_by_number(db: Session, gr_number: str) -> Optional[GRDTO]:
        gr = db.query(GR).filter(GR.gr_number == gr_number).first()
        GRDTO.to_dto(gr)

    @staticmethod
    def get_grs(db: Session) -> List[BookDTO]:
        grs = db.query(GR).all()
        return [GRDTO.to_dto(gr).to_camel() for gr in grs]

