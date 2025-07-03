# app/schemas/document_update_schemas.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from app.schemas.base import CamelCaseModel

class DocumentFieldValuesUpdate(CamelCaseModel):
    """Schema for updating document field values"""
    field_values: Dict[str, Any] = Field(..., description="Field values to update")
    
    class Config:
        schema_extra = {
            "example": {
                "fieldValues": {
                    "aadhaar_number": "123456789012",
                    "name_on_aadhaar": "John Doe",
                    "date_of_birth": "1990-01-01"
                }
            }
        }

class DocumentTypeFieldDefinitionsUpdate(CamelCaseModel):
    """Schema for updating document type field definitions (Admin only)"""
    field_definitions: Dict[str, Any] = Field(..., description="Field definitions structure")
    instructions: Optional[str] = Field(None, description="Updated instructions for users")
    
    class Config:
        schema_extra = {
            "example": {
                "fieldDefinitions": {
                    "aadhaar_number": {
                        "type": "text",
                        "label": "Aadhaar Number",
                        "label_marathi": "आधार नंबर",
                        "pattern": "^[0-9]{12}$",
                        "required": True,
                        "validation_message": "Please enter a valid 12-digit Aadhaar number"
                    },
                    "name_on_aadhaar": {
                        "type": "text",
                        "label": "Name on Aadhaar",
                        "label_marathi": "आधार कार्डवरील नाव",
                        "required": True
                    }
                },
                "instructions": "Please upload clear copy of Aadhaar card"
            }
        }

class DocumentUpdateResponse(CamelCaseModel):
    """Response schema for document updates"""
    message: str
    document_id: int = Field(..., alias="documentId")
    document_type_id: int = Field(..., alias="documentTypeId")
    document_type_name: str = Field(..., alias="documentTypeName")
    updated_fields: List[str] = Field(..., alias="updatedFields")
    verification_status: str = Field(..., alias="verificationStatus")
    new_file_path: Optional[str] = Field(None, alias="newFilePath")
    field_values: Optional[Dict[str, Any]] = Field(None, alias="fieldValues")

class DocumentFieldValuesUpdateResponse(CamelCaseModel):
    """Response schema for field values updates"""
    message: str
    document_id: int = Field(..., alias="documentId")
    document_type_id: int = Field(..., alias="documentTypeId")
    document_type_name: str = Field(..., alias="documentTypeName")
    field_values: Dict[str, Any] = Field(..., alias="fieldValues")
    verification_status: str = Field(..., alias="verificationStatus")
    updated_fields: List[str] = Field(..., alias="updatedFields")

class DocumentTypeUpdateResponse(CamelCaseModel):
    """Response schema for document type updates"""
    message: str
    document_type_id: int = Field(..., alias="documentTypeId")
    document_type_name: str = Field(..., alias="documentTypeName")
    field_definitions: Dict[str, Any] = Field(..., alias="fieldDefinitions")
    instructions: Optional[str] = None
    updated_by: Optional[int] = Field(None, alias="updatedBy")
    updated_at: str = Field(..., alias="updatedAt")

class FieldCompletion(CamelCaseModel):
    """Schema for field completion status"""
    total_fields: int = Field(..., alias="totalFields")
    completed_fields: int = Field(..., alias="completedFields")
    required_fields: int = Field(..., alias="requiredFields")
    completed_required_fields: int = Field(..., alias="completedRequiredFields")
    is_complete: bool = Field(..., alias="isComplete")
    completion_percentage: float = Field(..., alias="completionPercentage")
    missing_required_fields: List[Dict[str, Any]] = Field(..., alias="missingRequiredFields")

class DocumentDetailsResponse(CamelCaseModel):
    """Response schema for detailed document information"""
    document_id: int = Field(..., alias="documentId")
    document_type_id: int = Field(..., alias="documentTypeId")
    document_type_name: str = Field(..., alias="documentTypeName")
    document_type_name_english: str = Field(..., alias="documentTypeNameEnglish")
    category: str
    is_mandatory: bool = Field(..., alias="isMandatory")
    file_path: str = Field(..., alias="filePath")
    verification_status: str = Field(..., alias="verificationStatus")
    admin_comments: Optional[str] = Field(None, alias="adminComments")
    uploaded_at: Optional[str] = Field(None, alias="uploadedAt")
    last_updated_at: Optional[str] = Field(None, alias="lastUpdatedAt")
    field_definitions: Dict[str, Any] = Field(..., alias="fieldDefinitions")
    field_values: Dict[str, Any] = Field(..., alias="fieldValues")
    field_completion: FieldCompletion = Field(..., alias="fieldCompletion")
    instructions: str
    max_file_size_mb: int = Field(..., alias="maxFileSizeMb")
    allowed_formats: List[str] = Field(..., alias="allowedFormats")

class DocumentValidationError(CamelCaseModel):
    """Schema for document validation errors"""
    field_name: str = Field(..., alias="fieldName")
    error_message: str = Field(..., alias="errorMessage")
    field_type: str = Field(..., alias="fieldType")
    required: bool

class DocumentValidationResponse(CamelCaseModel):
    """Response schema for document validation"""
    is_valid: bool = Field(..., alias="isValid")
    errors: List[DocumentValidationError] = []
    field_results: Dict[str, Any] = Field(..., alias="fieldResults")
    document_type_info: Dict[str, Any] = Field(..., alias="documentTypeInfo")

class DocumentsSummaryResponse(CamelCaseModel):
    """Response schema for user documents summary"""
    user_id: int = Field(..., alias="userId")
    total_documents: int = Field(..., alias="totalDocuments")
    approved_documents: int = Field(..., alias="approvedDocuments")
    pending_documents: int = Field(..., alias="pendingDocuments")
    rejected_documents: int = Field(..., alias="rejectedDocuments")
    mandatory_documents: int = Field(..., alias="mandatoryDocuments")
    optional_documents: int = Field(..., alias="optionalDocuments")
    approval_rate: float = Field(..., alias="approvalRate")
    last_upload_date: Optional[str] = Field(None, alias="lastUploadDate")

class DocumentTypeUsageStats(CamelCaseModel):
    """Schema for document type usage statistics"""
    total_uploads: int = Field(..., alias="totalUploads")
    approved_uploads: int = Field(..., alias="approvedUploads")
    pending_uploads: int = Field(..., alias="pendingUploads")
    rejected_uploads: int = Field(..., alias="rejectedUploads")
    approval_rate: float = Field(..., alias="approvalRate")

class DocumentTypeWithStats(CamelCaseModel):
    """Schema for document type with usage statistics"""
    document_type_id: int = Field(..., alias="documentTypeId")
    document_type_name: str = Field(..., alias="documentTypeName")
    document_type_name_english: str = Field(..., alias="documentTypeNameEnglish")
    category: str
    is_mandatory: bool = Field(..., alias="isMandatory")
    field_definitions: Dict[str, Any] = Field(..., alias="fieldDefinitions")
    instructions: str
    usage_stats: DocumentTypeUsageStats = Field(..., alias="usageStats")

class BulkDocumentUpdateRequest(CamelCaseModel):
    """Schema for bulk document updates"""
    document_updates: List[Dict[str, Any]] = Field(..., alias="documentUpdates")
    
    class Config:
        schema_extra = {
            "example": {
                "documentUpdates": [
                    {
                        "documentId": 1,
                        "fieldValues": {
                            "aadhaar_number": "123456789012",
                            "name_on_aadhaar": "John Doe"
                        }
                    },
                    {
                        "documentId": 2,
                        "fieldValues": {
                            "pan_number": "ABCDE1234F"
                        }
                    }
                ]
            }
        }

class BulkDocumentUpdateResponse(CamelCaseModel):
    """Response schema for bulk document updates"""
    message: str
    total_requested: int = Field(..., alias="totalRequested")
    successful_updates: int = Field(..., alias="successfulUpdates")
    failed_updates: int = Field(..., alias="failedUpdates")
    updated_documents: List[DocumentUpdateResponse] = Field(..., alias="updatedDocuments")
    failed_documents: List[Dict[str, Any]] = Field(..., alias="failedDocuments")

class DocumentsRequiringUpdateResponse(CamelCaseModel):
    """Response schema for documents requiring field updates"""
    user_id: int = Field(..., alias="userId")
    total_documents_requiring_update: int = Field(..., alias="totalDocumentsRequiringUpdate")
    documents: List[Dict[str, Any]]
    
    class Config:
        schema_extra = {
            "example": {
                "userId": 123,
                "totalDocumentsRequiringUpdate": 2,
                "documents": [
                    {
                        "documentId": 1,
                        "documentTypeName": "Aadhaar Card",
                        "missingRequiredFields": ["aadhaar_number", "date_of_birth"],
                        "fieldCompletion": {
                            "isComplete": False,
                            "completionPercentage": 50.0
                        }
                    }
                ]
            }
        }