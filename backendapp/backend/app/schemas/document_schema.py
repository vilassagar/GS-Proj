# app/schemas/document_schema.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from app.schemas.base import CamelCaseModel

class DocumentCategory(str, Enum):
    """Document categories for organizing different types of documents"""
    IDENTITY_PROOF = "identity_proof"
    EDUCATIONAL = "educational"
    ADDRESS_PROOF = "address_proof"
    PROFESSIONAL = "professional"
    CASTE_CATEGORY = "caste_category"
    INCOME_PROOF = "income_proof"
    MEDICAL = "medical"
    OTHER = "other"

class DocumentType(CamelCaseModel):
    """Document type model with category support"""
    id: int
    name: str
    name_english: str
    category: DocumentCategory
    is_mandatory: bool = False
    instructions: Optional[str] = None
    max_file_size_mb: int = 5
    allowed_formats: List[str] = ["pdf", "jpg", "jpeg", "png", "doc", "docx"]
    field_definitions: Optional[Dict[str, Any]] = None

class DocumentTypeResponse(CamelCaseModel):
    """Response model for document types with additional metadata"""
    document_type_id: int = Field(..., alias="documentTypeId")
    document_type_name: str = Field(..., alias="documentTypeName")
    document_type_name_english: str = Field(..., alias="documentTypeNameEnglish")
    category: DocumentCategory
    is_mandatory: bool = Field(..., alias="isMandatory")
    instructions: Optional[str] = None
    max_file_size_mb: int = Field(5, alias="maxFileSizeMb")
    allowed_formats: List[str] = Field(["pdf", "jpg", "jpeg", "png", "doc", "docx"], alias="allowedFormats")
    field_definitions: Optional[Dict[str, Any]] = Field(None, alias="fieldDefinitions")
    
    class Config(CamelCaseModel.Config):
        from_attributes = True

class DocumentCategoryResponse(CamelCaseModel):
    """Response model for document categories with their types"""
    category: DocumentCategory
    category_name: str = Field(..., alias="categoryName")
    category_name_english: str = Field(..., alias="categoryNameEnglish")
    description: Optional[str] = None
    document_types: List[DocumentTypeResponse] = Field(..., alias="documentTypes")
    
    class Config(CamelCaseModel.Config):
        from_attributes = True