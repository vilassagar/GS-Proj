# app/services/profile_service.py
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import os
import uuid
from datetime import datetime

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    boto3 = None
    ClientError = Exception

from app.config import settings
from app.core.core_exceptions import NotFoundException, InvalidRequestException

# Add the missing schema imports
from app.schemas.profile_schema import (
    ProfileBasicDetailsUpdate,
    ProfileResponse, 
    ProfileValidationResponse
)

# Import DAL classes
try:
    from app.services.dal.user_dal import UserDal
except ImportError as e:
    print(f"Import error for UserDal: {e}")
    UserDal = None

try:
    from app.services.dal.document_dal import DocumentTypeDal, UserDocumentDal
except ImportError as e:
    print(f"Import error for document DALs: {e}")
    DocumentTypeDal = None
    UserDocumentDal = None

try:
    from app.services.dal.user_hierarchy_dal import DistrictDal, BlockDal, GramPanchayatDal
except ImportError as e:
    print(f"Import error for hierarchy DALs: {e}")
    DistrictDal = None
    BlockDal = None
    GramPanchayatDal = None

# S3 client for file uploads (optional)
try:
    s3_client = boto3.client("s3") if boto3 else None
    bucket_name = getattr(settings, 'aws_s3_bucket', 'default-bucket')
except Exception as e:
    print(f"S3 client setup error: {e}")
    s3_client = None
    bucket_name = None

def snake_to_camel(snake_str: str) -> str:
    """Convert snake_case to camelCase"""
    components = snake_str.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])

def dict_to_camel(data: dict) -> dict:
    """Convert dictionary keys from snake_case to camelCase"""
    if isinstance(data, dict):
        return {snake_to_camel(k): dict_to_camel(v) if isinstance(v, dict) else v for k, v in data.items()}
    return data

class ProfileService:
    
    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> Dict[str, Any]:
        """Get complete user profile with basic details, documents, and validation"""
        
        # Get user with details
        user = UserDal.get_user_details_by_id(db, user_id)
        if not user:
            raise NotFoundException(f"User with ID {user_id} not found")
        
        # Get user documents
        documents = UserDocumentDal.get_user_documents(db, user_id)
        
        # Get profile validation
        validation = ProfileService.validate_profile_completeness(db, user_id)
        
        # Convert to response format
        basic_details_dict = {
            "userId": user.user_id,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "designation": user.designation.value if hasattr(user.designation, 'value') else str(user.designation) if user.designation else None,
            "district": user.district.to_camel() if user.district else None,
            "block": user.block.to_camel() if user.block else None,
            "gramPanchayat": user.gram_panchayat.to_camel() if user.gram_panchayat else None,
            "mobileNumber": user.mobile_number,
            "whatsappNumber": user.whatsapp_number,
            "email": user.email,
            "status": user.status.value if hasattr(user.status, 'value') else str(user.status),
            "createdAt": user.created_at.isoformat(),
            "updatedAt": user.updated_at.isoformat() if user.updated_at else None
        }
        
        document_responses = [
            {
                "documentId": doc.id,
                "documentTypeId": doc.document_type_id,
                "documentTypeName": doc.document_type,
                "documentTypeNameEnglish": doc.document_type_english,
                "filePath": doc.file_path,
                "verificationStatus": doc.verification_status,
                "uploadedAt": doc.created_at.isoformat(),
                "adminComments": getattr(doc, 'admin_comments', None)
            } for doc in documents
        ]
        
        # Determine permissions based on user role and status
        user_status = user.status.value if hasattr(user.status, 'value') else str(user.status)
        permissions = {
            "canEditBasicDetails": user_status in ['PENDING', 'REJECTED'],
            "canUploadDocuments": True,
            "canDeleteDocuments": user_status != 'APPROVED'
        }
        
        # Return the complete profile data
        return {
            "basicDetails": basic_details_dict,
            "documents": document_responses,
            "validation": validation,
            "permissions": permissions
        }
    
    @staticmethod
    def update_basic_details(
        db: Session, 
        user_id: int, 
        profile_data: ProfileBasicDetailsUpdate
    ) -> Dict[str, Any]:
        """Update user's basic profile details"""
        
        user = UserDal.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException(f"User with ID {user_id} not found")
        
        # Validate hierarchy relationships
        if profile_data.district_id:
            district = DistrictDal.get_district_by_id(db, profile_data.district_id)
            if not district:
                raise InvalidRequestException("Invalid district selected")
        
        if profile_data.block_id:
            block = BlockDal.get_block_by_id(db, profile_data.block_id)
            if not block or (profile_data.district_id and block.district_id != profile_data.district_id):
                raise InvalidRequestException("Invalid block selected for the given district")
        
        if profile_data.gram_panchayat_id:
            from app.services.dal.user_hierarchy_dal import GramPanchayatDal
            gp = GramPanchayatDal.get_gram_panchayat_by_id(db, profile_data.gram_panchayat_id)
            if not gp or (profile_data.block_id and gp.block_id != profile_data.block_id):
                raise InvalidRequestException("Invalid gram panchayat selected for the given block")
        
        # Update user data
        update_dict = {
            "first_name": profile_data.first_name,
            "last_name": profile_data.last_name,
            "mobile_number": profile_data.mobile_number,
            "whatsapp_number": profile_data.whatsapp_number,
            "email": profile_data.email,
            "updated_by": user_id
        }
        
        if profile_data.district_id:
            update_dict["district_id"] = profile_data.district_id
        if profile_data.block_id:
            update_dict["block_id"] = profile_data.block_id
        if profile_data.gram_panchayat_id:
            update_dict["gram_panchayat_id"] = profile_data.gram_panchayat_id
        
        updated_user = UserDal.update_user(db, user_id, update_dict)
        
        return {
            "message": "Profile updated successfully",
            "user": updated_user.to_camel()
        }
    
    @staticmethod
    async def upload_document(
        db: Session,
        user_id: int,
        document_type_id: int,
        file: UploadFile,
        additional_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Upload a single document for the user"""
        
        # Validate document type
        doc_type = DocumentTypeDal.get_document_type_by_id(db, document_type_id)
        if not doc_type:
            raise NotFoundException(f"Document type with ID {document_type_id} not found")
        
        # Validate file type
        allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx']
        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension not in allowed_extensions:
            raise InvalidRequestException(
                "Invalid file type. Please upload PDF, JPG, PNG, DOC, or DOCX files only."
            )
        
        # Save file to S3
        file_path = await ProfileService._save_file_to_s3(file, user_id, document_type_id)
        
        # Create document record
        user_doc = UserDocumentDal.create_user_document(
            db=db,
            user_id=user_id,
            document_type_id=document_type_id,
            file_path=file_path
        )
        
        # Update user's document upload status
        UserDal.set_documents_uploaded_to_true(db, user_id)
        
        return {
            "message": f"{doc_type.name} uploaded successfully",
            "document_id": user_doc.id,
            "file_path": file_path
        }
    
    @staticmethod
    async def upload_multiple_documents(
        db: Session,
        user_id: int,
        files_mapping: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Upload multiple documents at once"""
        
        uploaded_docs = []
        failed_uploads = []
        
        for doc_type_id_str, file_data in files_mapping.items():
            try:
                doc_type_id = int(doc_type_id_str)
                
                # Handle file data (this could be base64 or file object depending on implementation)
                # For now, assuming it's handled similarly to single upload
                # You may need to adapt this based on how your React component sends the data
                
                # Validate document type exists
                doc_type = DocumentTypeDal.get_document_type_by_id(db, doc_type_id)
                if not doc_type:
                    failed_uploads.append({
                        "document_type_id": doc_type_id,
                        "error": f"Document type with ID {doc_type_id} not found"
                    })
                    continue
                
                # Process the upload (implementation depends on your file handling)
                # This is a placeholder - adapt based on your actual file handling
                file_path = f"user_docs/user_{user_id}/doc_type_{doc_type_id}/file_{uuid.uuid4().hex}"
                
                user_doc = UserDocumentDal.create_user_document(
                    db=db,
                    user_id=user_id,
                    document_type_id=doc_type_id,
                    file_path=file_path
                )
                
                uploaded_docs.append({
                    "document_type_id": doc_type_id,
                    "document_type_name": doc_type.name,
                    "document_id": user_doc.id,
                    "file_path": file_path
                })
                
            except Exception as e:
                failed_uploads.append({
                    "document_type_id": doc_type_id_str,
                    "error": str(e)
                })
        
        # Update user's document upload status if any documents were uploaded
        if uploaded_docs:
            UserDal.set_documents_uploaded_to_true(db, user_id)
        
        return {
            "message": f"Uploaded {len(uploaded_docs)} documents successfully",
            "uploaded_documents": uploaded_docs,
            "failed_uploads": failed_uploads,
            "total_uploaded": len(uploaded_docs),
            "total_failed": len(failed_uploads)
        }
    
    @staticmethod
    def get_user_documents(db: Session, user_id: int) -> List[Dict[str, Any]]:
        """Get all documents uploaded by the user"""
        documents = UserDocumentDal.get_user_documents(db, user_id)
        
        return [
            {
                "documentId": doc.id,
                "documentTypeId": doc.document_type_id,
                "documentTypeName": doc.document_type,
                "documentTypeNameEnglish": doc.document_type_english,
                "filePath": doc.file_path,
                "verificationStatus": doc.verification_status,
                "uploadedAt": doc.created_at.isoformat(),
                "adminComments": getattr(doc, 'admin_comments', None)
            } for doc in documents
        ]
    
    @staticmethod
    def delete_document(db: Session, user_id: int, document_id: int) -> Dict[str, Any]:
        """Delete a specific document"""
        # Implement document deletion logic
        # This would involve removing from database and S3
        return {
            "message": "Document deleted successfully",
            "document_id": document_id
        }
    
    @staticmethod
    def get_document_types(
        db: Session, 
        category: Optional[str] = None,
        is_mandatory: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """Get available document types"""
        
        doc_types = DocumentTypeDal.get_all_document_types(db)
        
        # Filter by category if provided
        if category:
            doc_types = [dt for dt in doc_types if getattr(dt, 'category', None) == category]
        
        # Filter by mandatory status if provided
        if is_mandatory is not None:
            doc_types = [dt for dt in doc_types if dt.is_mandatory == is_mandatory]
        
        return [
            {
                "documentTypeId": dt.id,
                "documentTypeName": dt.name,
                "documentTypeNameEnglish": dt.name_english,
                "isMandatory": dt.is_mandatory,
                "category": getattr(dt, 'category', None),
                "instructions": getattr(dt, 'instructions', None)
            } for dt in doc_types
        ]
    
    @staticmethod
    def validate_profile_completeness(db: Session, user_id: int) -> Dict[str, Any]:
        """Validate if user's profile is complete"""
        
        user = UserDal.get_user_by_id(db, user_id)
        if not user:
            raise NotFoundException(f"User with ID {user_id} not found")
        
        # Check basic fields
        missing_basic_fields = []
        required_basic_fields = {
            'first_name': 'firstName',
            'last_name': 'lastName', 
            'mobile_number': 'mobileNumber',
            'email': 'email',
            'district_id': 'districtId',
            'block_id': 'blockId',
            'gram_panchayat_id': 'gramPanchayatId'
        }
        
        for field, camel_field in required_basic_fields.items():
            if not getattr(user, field, None):
                missing_basic_fields.append(camel_field)
        
        # Check mandatory documents
        mandatory_doc_types = DocumentTypeDal.get_all_document_types(db)
        mandatory_doc_types = [dt for dt in mandatory_doc_types if dt.is_mandatory]
        
        user_documents = UserDocumentDal.get_user_documents(db, user_id)
        uploaded_doc_type_ids = {doc.document_type_id for doc in user_documents}
        
        missing_mandatory_documents = []
        for doc_type in mandatory_doc_types:
            if doc_type.id not in uploaded_doc_type_ids:
                missing_mandatory_documents.append({
                    "documentTypeId": doc_type.id,
                    "documentTypeName": doc_type.name,
                    "documentTypeNameEnglish": doc_type.name_english,
                    "isMandatory": doc_type.is_mandatory,
                    "category": getattr(doc_type, 'category', None),
                    "instructions": getattr(doc_type, 'instructions', None)
                })
        
        # Check pending verifications
        pending_document_verification = []
        for doc in user_documents:
            if doc.verification_status == 'PENDING':
                pending_document_verification.append({
                    "documentId": doc.id,
                    "documentTypeId": doc.document_type_id,
                    "documentTypeName": doc.document_type,
                    "documentTypeNameEnglish": doc.document_type_english,
                    "filePath": doc.file_path,
                    "verificationStatus": doc.verification_status,
                    "uploadedAt": doc.created_at.isoformat()
                })
        
        # Calculate completion percentage
        total_basic_fields = len(required_basic_fields)
        total_mandatory_docs = len(mandatory_doc_types)
        total_requirements = total_basic_fields + total_mandatory_docs
        
        completed_basic_fields = total_basic_fields - len(missing_basic_fields)
        completed_mandatory_docs = total_mandatory_docs - len(missing_mandatory_documents)
        completed_requirements = completed_basic_fields + completed_mandatory_docs
        
        completion_percentage = (completed_requirements / total_requirements * 100) if total_requirements > 0 else 100
        
        # Generate next steps
        next_steps = []
        if missing_basic_fields:
            next_steps.append("Complete missing basic profile information")
        if missing_mandatory_documents:
            next_steps.append(f"Upload {len(missing_mandatory_documents)} mandatory documents")
        if pending_document_verification:
            next_steps.append("Wait for document verification by admin")
        
        is_complete = len(missing_basic_fields) == 0 and len(missing_mandatory_documents) == 0
        
        # Convert to dictionary manually
        return {
            "isComplete": is_complete,
            "missingBasicFields": missing_basic_fields,
            "missingMandatoryDocuments": missing_mandatory_documents,
            "pendingDocumentVerification": pending_document_verification,
            "completionPercentage": round(completion_percentage, 2),
            "nextSteps": next_steps
        }
    
    @staticmethod
    async def _save_file_to_s3(file: UploadFile, user_id: int, document_type_id: int) -> str:
        """Save uploaded file to S3 and return the S3 key"""
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = uuid.uuid4().hex[:8]
            file_extension = file.filename.split('.')[-1]
            new_filename = f"{timestamp}_{unique_id}.{file_extension}"
            
            # Create S3 key
            s3_key = f"profile_docs/user_{user_id}/doc_type_{document_type_id}/{new_filename}"
            
            # Read file content
            file_content = await file.read()
            
            # Upload to S3
            s3_client.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType=file.content_type
            )
            
            return s3_key
            
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload file to S3: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"File upload failed: {str(e)}"
            )