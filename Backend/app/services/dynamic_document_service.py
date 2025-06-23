from typing import Dict, Any, List, Optional
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import json
import os

from app.services.dal.dynamic_document_dal import DynamicDocumentDal
from app.services.dal.dto.dynamic_document_dto import DocumentTypeWithFieldsDTO, UserDocumentWithFieldsDTO
from app.schemas.dynamic_document_schema import DocumentUploadSchema, DocumentVerificationSchema

class DynamicDocumentService:
    
    @staticmethod
    def get_document_types_with_fields(
        db: Session,
        category: Optional[str] = None,
        is_mandatory: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        doc_types = DynamicDocumentDal.get_all_document_types_with_fields(
            db, category=category, is_mandatory=is_mandatory
        )
        return [dt.to_camel() for dt in doc_types]
    
    @staticmethod
    def get_document_type_fields(db: Session, doc_type_id: int) -> Dict[str, Any]:
        doc_type = DynamicDocumentDal.get_document_type_with_fields(db, doc_type_id)
        if not doc_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document type not found"
            )
        return doc_type.to_camel()
    
    @staticmethod
    def validate_field_values(
        field_definitions: List[Any], 
        field_values: Dict[str, Any]
    ) -> Dict[str, str]:
        """Validate field values against field definitions"""
        errors = {}
        
        for field_def in field_definitions:
            field_name = field_def.field_name
            is_required = field_def.is_required
            field_type = field_def.field_type
            
            value = field_values.get(field_name)
            
            # Check required fields
            if is_required and (value is None or value == ""):
                errors[field_name] = f"{field_def.label} is required"
                continue
            
            # Skip validation if field is empty and not required
            if value is None or value == "":
                continue
            
            # Type-specific validation
            if field_type == "NUMBER":
                try:
                    float(value)
                except (ValueError, TypeError):
                    errors[field_name] = f"{field_def.label} must be a valid number"
            
            elif field_type == "EMAIL":
                import re
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, str(value)):
                    errors[field_name] = f"{field_def.label} must be a valid email"
            
            elif field_type == "PHONE":
                # Basic phone validation
                phone_str = str(value).replace("+", "").replace("-", "").replace(" ", "")
                if not phone_str.isdigit() or len(phone_str) < 10:
                    errors[field_name] = f"{field_def.label} must be a valid phone number"
            
            elif field_type == "DATE":
                try:
                    datetime.strptime(str(value), "%Y-%m-%d")
                except ValueError:
                    errors[field_name] = f"{field_def.label} must be in YYYY-MM-DD format"
            
            elif field_type == "PERCENTAGE":
                try:
                    percent_val = float(value)
                    if percent_val < 0 or percent_val > 100:
                        errors[field_name] = f"{field_def.label} must be between 0 and 100"
                except (ValueError, TypeError):
                    errors[field_name] = f"{field_def.label} must be a valid percentage"
        
        return errors
    
    @staticmethod
    async def upload_document_with_fields(
        db: Session,
        user_id: int,
        document_data: DocumentUploadSchema,
        file: UploadFile
    ) -> Dict[str, Any]:
        # Get document type with field definitions
        doc_type = DynamicDocumentDal.get_document_type_with_fields(
            db, document_data.document_type_id
        )
        
        if not doc_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document type not found"
            )
        
        # Validate field values
        validation_errors = DynamicDocumentService.validate_field_values(
            doc_type.field_definitions, document_data.field_values
        )
        
        if validation_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"field_errors": validation_errors}
            )
        
        # Save file (implement your file saving logic here)
        file_path = await DynamicDocumentService._save_document_file(
            file, user_id, document_data.document_type_id
        )
        
        # Create document record
        user_doc = DynamicDocumentDal.create_user_document_with_fields(
            db=db,
            user_id=user_id,
            document_type_id=document_data.document_type_id,
            file_path=file_path,
            field_values=document_data.field_values
        )
        
        return {
            "message": "Document uploaded successfully",
            "document_id": user_doc.id,
            "verification_status": user_doc.verification_status.value
        }
    
    @staticmethod
    async def _save_document_file(
        file: UploadFile, 
        user_id: int, 
        document_type_id: int
    ) -> str:
        """Save uploaded file and return file path"""
        # Implement your file saving logic here
        # This could save to S3, local storage, etc.
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = f"user_docs/user_{user_id}/doc_type_{document_type_id}/{filename}"
        
        # For now, return the path - implement actual saving based on your setup
        return file_path
    
    @staticmethod
    def get_user_documents_with_fields(db: Session, user_id: int) -> List[Dict[str, Any]]:
        user_docs = DynamicDocumentDal.get_user_documents_with_fields(db, user_id)
        return [doc.to_camel() for doc in user_docs]
    
    @staticmethod
    def verify_document(
        db: Session,
        verification_data: DocumentVerificationSchema,
        admin_user_id: int
    ) -> Dict[str, Any]:
        updated_doc = DynamicDocumentDal.update_document_verification(
            db=db,
            document_id=verification_data.user_document_id,
            verification_status=verification_data.verification_status,
            admin_comments=verification_data.admin_comments,
            admin_user_id=admin_user_id
        )
        
        if not updated_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        return {
            "message": "Document verification updated successfully",
            "verification_status": updated_doc.verification_status.value
        }   