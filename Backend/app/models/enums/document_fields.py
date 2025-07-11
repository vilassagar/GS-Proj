from enum import Enum

class DocumentCategory(Enum):
    IDENTITY = "IDENTITY"
    EDUCATION = "EDUCATION"
    SERVICE = "SERVICE"
    CASTE = "CASTE"
    FINANCIAL = "FINANCIAL"
    AWARDS = "AWARDS"
    OTHER = "OTHER"

class FieldType(Enum):
    TEXT = "TEXT"
    NUMBER = "NUMBER"
    DATE = "DATE"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    SELECT = "SELECT"
    MULTISELECT = "MULTISELECT"
    BOOLEAN = "BOOLEAN"
    PERCENTAGE = "PERCENTAGE"
    YEAR = "YEAR"

class EducationLevel(Enum):
    SSC = "SSC"
    HSC = "HSC"
    DIPLOMA = "DIPLOMA"
    GRADUATE = "GRADUATE"
    POST_GRADUATE = "POST_GRADUATE"
    PHD = "PHD"

class DocumentStatus(Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    RESUBMIT_REQUIRED = "RESUBMIT_REQUIRED"