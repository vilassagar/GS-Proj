# app/schemas/profile_schema.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .document_schema import DocumentCategory, DocumentType, DocumentCategoryResponse

class ProfileBasicDetailsUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    mobile_number: Optional[str] = Field(None, max_length=15)
    whatsapp_number: Optional[str] = Field(None, max_length=15)
    email: Optional[str] = Field(None, max_length=255)
    district_id: Optional[int] = None
    block_id: Optional[int] = None
    gram_panchayat_id: Optional[int] = None

    class Config:
        from_attributes = True

class ProfileDocumentResponse(BaseModel):
    document_id: int = Field(..., alias="documentId")
    document_type_id: int = Field(..., alias="documentTypeId")
    document_type_name: str = Field(..., alias="documentTypeName")
    document_type_name_english: str = Field(..., alias="documentTypeNameEnglish")
    category: DocumentCategory = None
    file_path: str = Field(..., alias="filePath")
    verification_status: str = Field(..., alias="verificationStatus")
    uploaded_at: str = Field(..., alias="uploadedAt")
    admin_comments: Optional[str] = Field(None, alias="adminComments")

    class Config:
        from_attributes = True
        populate_by_name = True

class DocumentTypeResponse(BaseModel):
    document_type_id: int = Field(..., alias="documentTypeId")
    document_type_name: str = Field(..., alias="documentTypeName")
    document_type_name_english: str = Field(..., alias="documentTypeNameEnglish")
    category: DocumentCategory = None
    is_mandatory: bool = Field(..., alias="isMandatory")
    instructions: Optional[str] = None
    max_file_size_mb: int = Field(5, alias="maxFileSizeMb")
    allowed_formats: List[str] = Field(..., alias="allowedFormats")

    class Config:
        from_attributes = True
        populate_by_name = True

class DocumentsByCategoryResponse(BaseModel):
    category: DocumentCategory
    category_name: str = Field(..., alias="categoryName")
    category_name_english: str = Field(..., alias="categoryNameEnglish")
    description: Optional[str] = None
    document_types: List[DocumentTypeResponse] = Field(..., alias="documentTypes")
    uploaded_documents: List[ProfileDocumentResponse] = Field(..., alias="uploadedDocuments")
    completion_status: Dict[str, Any] = Field(..., alias="completionStatus")

    class Config:
        from_attributes = True
        populate_by_name = True

class ProfileBasicDetails(BaseModel):
    user_id: int = Field(..., alias="userId")
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    designation: Optional[str] = None
    district: Optional[Dict[str, Any]] = None
    block: Optional[Dict[str, Any]] = None
    gram_panchayat: Optional[Dict[str, Any]] = Field(None, alias="gramPanchayat")
    mobile_number: Optional[str] = Field(None, alias="mobileNumber")
    whatsapp_number: Optional[str] = Field(None, alias="whatsappNumber")
    email: Optional[str] = None
    status: str = None
    created_at: str = Field(..., alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")

    class Config:
        from_attributes = True
        populate_by_name = True

class ProfilePermissions(BaseModel):
    can_edit_basic_details: bool = Field(..., alias="canEditBasicDetails")
    can_upload_documents: bool = Field(..., alias="canUploadDocuments")
    can_delete_documents: bool = Field(..., alias="canDeleteDocuments")

    class Config:
        from_attributes = True
        populate_by_name = True

class ProfileValidationResponse(BaseModel):
    is_complete: bool = Field(..., alias="isComplete")
    missing_basic_fields: List[str] = Field(..., alias="missingBasicFields")
    missing_mandatory_documents: List[Dict[str, Any]] = Field(..., alias="missingMandatoryDocuments")
    pending_document_verification: List[Dict[str, Any]] = Field(..., alias="pendingDocumentVerification")
    completion_percentage: float = Field(..., alias="completionPercentage")
    next_steps: List[str] = Field(..., alias="nextSteps")

    class Config:
        from_attributes = True
        populate_by_name = True

class ProfileResponse(BaseModel):
    basic_details: ProfileBasicDetails = Field(..., alias="basicDetails")
    documents: Optional[List[ProfileDocumentResponse]] = None
    validation: Optional[ProfileValidationResponse]= None
    permissions: Optional[ProfilePermissions] = None

    class Config:
        from_attributes = True
        populate_by_name = True