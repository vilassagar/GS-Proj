from datetime import datetime
from typing import Optional
from app.models.books import Book
from app.services.dal.dto.to_camel import ToCamel


class BookDTO(ToCamel):
    def __init__(
        self,
        id: int,
        title: str,
        department: str,
        file_path: str,
        created_by: Optional[int],
        updated_by: Optional[int],
        created_at: datetime,
        updated_at: Optional[datetime],
        is_active: bool
    ):
        self.id = id
        self.title = title
        self.department = department
        self.file_path = file_path
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active

    @staticmethod
    def to_dto(book: Book) -> "BookDTO":
        return BookDTO(
            id=book.id,
            title=book.title,
            department=book.department,
            file_path=book.file_path,
            created_by=book.created_by,
            updated_by=book.updated_by,
            created_at=book.created_at,
            updated_at=book.updated_at,
            is_active=book.is_active
        )