# app/services/dal/dto/document_dto.py
from typing import Optional, Dict, Any
from datetime import datetime

class DocumentTypeDTO:
    """DTO for DocumentType model with all necessary attributes"""
    
    def __init__(self, id: int, name: str, name_english: str, is_mandatory: bool,
                 category: Optional[str] = None, instructions: Optional[str] = None,
                 field_definitions: Optional[Dict[str, Any]] = None,
                 created_by: Optional[int] = None, updated_by: Optional[int] = None,
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None,
                 is_active: bool = True):
        self.id = id
        self.name = name
        self.name_english = name_english
        self.is_mandatory = is_mandatory
        self.category = category.lower() if category else 'other'  # Normalize to lowercase
        self.instructions = instructions
        self.field_definitions = field_definitions
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
        
        # Add attributes for backward compatibility
        self.max_file_size_mb = 5
        self.allowed_formats = 'pdf,jpg,jpeg,png,doc,docx'
    
    @classmethod
    def to_dto(cls, model):
        """Convert DocumentType model to DTO"""
        if not model:
            return None
            
        return cls(
            id=model.id,
            name=model.name,
            name_english=model.name_english,
            is_mandatory=model.is_mandatory,
            category=model.category,
            instructions=model.instructions,
            field_definitions=model.field_definitions,
            created_by=model.created_by,
            updated_by=model.updated_by,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_active=getattr(model, 'is_active', True)
        )
    
    def to_dict(self):
        """Convert to dictionary for API response"""
        return {
            "documentTypeId": self.id,
            "documentTypeName": self.name,
            "documentTypeNameEnglish": self.name_english,
            "category": self.category,
            "isMandatory": self.is_mandatory,
            "instructions": self.instructions,
            "maxFileSizeMb": self.max_file_size_mb,
            "allowedFormats": self.allowed_formats.split(',') if isinstance(self.allowed_formats, str) else self.allowed_formats,
            "fieldDefinitions": self.field_definitions
        }

class UserDocumentDTO:
    """DTO for UserDocument model"""
    
    def __init__(self, id: int, user_id: int, document_type_id: int, file_path: str,
                 verification_status: str, admin_comments: Optional[str] = None,
                 field_values: Optional[Dict[str, Any]] = None,
                 created_at: Optional[datetime] = None, updated_at: Optional[datetime] = None,
                 document_type_name: Optional[str] = None,
                 document_type_english: Optional[str] = None,
                 document_type_category: Optional[str] = None,
                 is_mandatory: Optional[bool] = None):
        self.id = id
        self.user_id = user_id
        self.document_type_id = document_type_id
        self.file_path = file_path
        self.verification_status = verification_status
        self.admin_comments = admin_comments
        self.field_values = field_values
        self.created_at = created_at
        self.updated_at = updated_at
        
        # Document type information (from joined query)
        self.document_type = document_type_name
        self.document_type_english = document_type_english
        self.category = document_type_category
        self.is_mandatory = is_mandatory
    
    @classmethod
    def to_dto(cls, model):
        """Convert UserDocument model to DTO"""
        if not model:
            return None
            
        # Get document type info if available (from eager loading)
        doc_type = getattr(model, 'document_type', None)
        
        return cls(
            id=model.id,
            user_id=model.user_id,
            document_type_id=model.document_type_id,
            file_path=model.file_path,
            verification_status=model.verification_status.value if hasattr(model.verification_status, 'value') else str(model.verification_status),
            admin_comments=model.admin_comments,
            field_values=model.field_values,
            created_at=model.created_at,
            updated_at=model.updated_at,
            document_type_name=doc_type.name if doc_type else None,
            document_type_english=doc_type.name_english if doc_type else None,
            document_type_category=doc_type.category if doc_type else None,
            is_mandatory=doc_type.is_mandatory if doc_type else None
        )
    
    def to_dict(self):
        """Convert to dictionary for API response"""
        return {
            "documentId": self.id,
            "documentTypeId": self.document_type_id,
            "documentTypeName": self.document_type,
            "documentTypeNameEnglish": self.document_type_english,
            "category": self.category,
            "filePath": self.file_path,
            "verificationStatus": self.verification_status,
            "uploadedAt": self.created_at.isoformat() if self.created_at else None,
            "adminComments": self.admin_comments,
            "fieldValues": self.field_values
        }