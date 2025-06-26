from app.models.books import Book
from app.models.books import Page
from app.models.books import Word
from app.models.documents import UserDocument, DocumentType
from app.models.users_hierarchy import District, Block, GramPanchayat
from app.models.gr_yojana import GR, Yojana
from app.models.otp import UserOTP
from app.models.users import User
from app.models.roles import Role
from app.models.department import Department

__all__ = [
    "Book",
    "User",
    "Role",
    "UserDocument",
    "DocumentType",
    "Yojana",
    "GR",
    "UserOTP",
    "District",
    "Block",
    "GramPanchayat",
    "Department"
]
