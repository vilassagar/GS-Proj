from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, validator
from fastapi import UploadFile
from app.schemas.base import CamelModel

class DocumentFieldSchema(CamelModel):
    field_name: str
    field_type: str = Field(..., description="Type of field: TEXT, NUMBER, DATE, etc.")
    label: str
    label_english: str
    is_required: bool = False
    validation_rules: Optional[Dict[str, Any]] = {}
    options: Optional[List[str]] = []
    placeholder: Optional[str] = None
    help_text: Optional[str] = None

class DocumentTypeCreateSchema(CamelModel):
    name: str
    name_english: Optional[str]
    is_mandatory: bool = True
    category: Optional[str]
    instructions: Optional[str]
    field_definitions: Dict[str, Dict[str, Any]]

class DocumentTypeResponseSchema(CamelModel):
    document_type_id: int
    document_type_name: str
    document_type_name_english: Optional[str]
    is_mandatory: bool
    category: Optional[str]
    instructions: Optional[str]
    field_definitions: Optional[Dict[str, Any]] = None

class DocumentUploadSchema(CamelModel):
    document_type_id: int
    field_values: Dict[str, Any]
    
    @validator('field_values')
    def validate_field_values(cls, v):
        if not isinstance(v, dict):
            raise ValueError('Field values must be a dictionary')
        return v

class DocumentUploadRequest(BaseModel):
    document_data: str = Field(..., description="JSON string containing document_type_id and field_values")
    # file will be handled separately in the endpoint

class UserDocumentResponseSchema(CamelModel):
    user_document_id: int
    document_type: DocumentTypeResponseSchema
    file_path: str
    field_values: Dict[str, Any]
    verification_status: str
    admin_comments: Optional[str]
    created_at: str
    updated_at: Optional[str]

class DocumentVerificationSchema(CamelModel):
    user_document_id: int
    verification_status: str = Field(..., description="APPROVED, REJECTED, or RESUBMIT_REQUIRED")
    admin_comments: Optional[str]

class DocumentSearchSchema(CamelModel):
    category: Optional[str]
    is_mandatory: Optional[bool]
    search_term: Optional[str]