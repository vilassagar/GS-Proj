# app/schemas/document_schema.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

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

class DocumentType(BaseModel):
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
    class Config:
        from_attributes = True

class DocumentCategoryResponse(BaseModel):
    """Response model for document categories with their types"""
    category: DocumentCategory
    category_name: str
    category_name_english: str
    description: Optional[str] = None
    document_types: List[DocumentType] = []
    
    class Config:
        from_attributes = True

