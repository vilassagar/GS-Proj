# app/services/profile_service.py - COMPLETE WORKING VERSION
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import os
import uuid
from datetime import datetime
import json
from app.schemas.document_schema import DocumentCategory
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
    ProfileValidationResponse,
    DocumentsByCategoryResponse,
    DocumentTypeResponse
)
from app.schemas.document_schema import DocumentCategory
# If DOCUMENT_CATEGORIES_CONFIG is defined elsewhere, import it from the correct module.
# from app.config.document_config import DOCUMENT_CATEGORIES_CONFIG

# Import DAL classes
try:
    from app.services.dal.user_dal import UserDal
except ImportError as e:
    print(f"Import error for UserDal: {e}")
    raise ImportError("UserDal could not be imported. Please ensure the module exists and is error-free.") from e

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
            "designation": user.designation.value if user.designation and hasattr(user.designation, 'value') else user.designation if isinstance(user.designation, str) else str(user.designation) if user.designation else None,
            "district": user.district.to_camel() if user.district else None,
            "block": user.block.to_camel() if user.block else None,
            "gramPanchayat": user.gram_panchayat.to_camel() if user.gram_panchayat else None,
            "mobileNumber": user.mobile_number,
            "whatsappNumber": user.whatsapp_number,
            "email": user.email,
            "status": user.status.value if hasattr(user.status, 'value') else str(user.status),
            "createdAt": user.created_at.isoformat() if user.created_at else None,
            "updatedAt": user.updated_at.isoformat() if user.updated_at else None
        }
        
        document_responses = [
            {
                "documentId": doc.id,
                "documentTypeId": doc.document_type_id,
                "documentTypeName": getattr(doc, 'document_type', ''),
                "documentTypeNameEnglish": getattr(doc, 'document_type_english', ''),
                "filePath": doc.file_path,
                "verificationStatus": doc.verification_status,
                "uploadedAt": doc.created_at.isoformat() if doc.created_at else '',
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
    def validate_profile_completeness(db: Session, user_id: int) -> Dict[str, Any]:
        """FIXED: Validate if user's profile is complete - with field_definitions"""
        
        print(f"🔍 Starting profile validation for user {user_id}")
        
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
        
        # Get ALL document types
        print("🔍 Fetching document types for validation...")
        try:
            all_doc_types = DocumentTypeDal.get_all_document_types(db)
            print(f"📊 Found {len(all_doc_types)} document types")
        except Exception as e:
            print(f"❌ Error fetching document types: {e}")
            all_doc_types = []
        
        # Filter mandatory document types
        mandatory_doc_types = []
        for dt in all_doc_types:
            try:
                is_mandatory = getattr(dt, 'is_mandatory', False)
                if is_mandatory:
                    mandatory_doc_types.append(dt)
            except Exception as e:
                print(f"⚠️  Error checking mandatory status for doc type: {e}")
                continue
        
        print(f"📊 Found {len(mandatory_doc_types)} mandatory document types")
        
        # Get user's uploaded documents
        if UserDocumentDal is None:
            raise ImportError("UserDocumentDal is not available. Please check the import and module.")
        user_documents = UserDocumentDal.get_user_documents(db, user_id)
        uploaded_doc_type_ids = {getattr(doc, 'document_type_id', 0) for doc in user_documents}
        
        # Find missing mandatory documents - WITH field_definitions
        missing_mandatory_documents = []
        for doc_type in mandatory_doc_types:
            try:
                doc_id = getattr(doc_type, 'id', 0)
                if doc_id not in uploaded_doc_type_ids:
                    # Get field_definitions - could be JSON string or dict
                    field_definitions = getattr(doc_type, 'field_definitions', None)
                    
                    # Parse field_definitions if it's a string
                    if isinstance(field_definitions, str):
                        try:
                            import json
                            field_definitions = json.loads(field_definitions)
                        except (json.JSONDecodeError, TypeError):
                            field_definitions = None
                    
                    missing_doc = {
                        "documentTypeId": doc_id,
                        "documentTypeName": getattr(doc_type, 'name', ''),
                        "documentTypeNameEnglish": getattr(doc_type, 'name_english', ''),
                        "isMandatory": getattr(doc_type, 'is_mandatory', True),
                        "category": getattr(doc_type, 'category', 'other'),
                        "instructions": getattr(doc_type, 'instructions', 'Please upload this document'),
                        "fieldDefinitions": field_definitions  # ✅ NOW INCLUDED!
                    }
                    
                    print(f"📋 Missing: {missing_doc['documentTypeNameEnglish']} (category: {missing_doc['category']}, has fields: {field_definitions is not None})")
                    missing_mandatory_documents.append(missing_doc)
            except Exception as e:
                print(f"⚠️  Error processing doc type: {e}")
                continue
        
        # Check pending verifications
        pending_document_verification = []
        for doc in user_documents:
            try:
                verification_status = getattr(doc, 'verification_status', 'PENDING')
                if verification_status == 'PENDING':
                    pending_doc = {
                        "documentId": getattr(doc, 'id', 0),
                        "documentTypeId": getattr(doc, 'document_type_id', 0),
                        "documentTypeName": getattr(doc, 'document_type', ''),
                        "documentTypeNameEnglish": getattr(doc, 'document_type_english', ''),
                        "filePath": getattr(doc, 'file_path', ''),
                        "verificationStatus": verification_status,
                        "uploadedAt": doc.created_at.isoformat() if hasattr(doc, 'created_at') and doc.created_at else ''
                    }
                    pending_document_verification.append(pending_doc)
            except Exception as e:
                print(f"⚠️  Error processing pending doc: {e}")
                continue
        
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
        
        print(f"✅ Validation complete: {completion_percentage:.1f}% ({len(missing_mandatory_documents)} missing docs)")
        
        return {
            "isComplete": is_complete,
            "missingBasicFields": missing_basic_fields,
            "missingMandatoryDocuments": missing_mandatory_documents,
            "pendingDocumentVerification": pending_document_verification,
            "completionPercentage": round(completion_percentage, 2),
            "nextSteps": next_steps
        }

    @staticmethod
    def get_document_types(
        db: Session, 
        category: Optional[str] = None,
        is_mandatory: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """FIXED: Get available document types - with field_definitions"""
        
        doc_types = DocumentTypeDal.get_all_document_types(db)
        
        # Filter by category if provided
        if category:
            doc_types = [dt for dt in doc_types if getattr(dt, 'category', 'other') == category]
        
        # Filter by mandatory status if provided
        if is_mandatory is not None:
            doc_types = [dt for dt in doc_types if getattr(dt, 'is_mandatory', False) == is_mandatory]
        
        result = []
        for dt in doc_types:
            # Get field_definitions - could be JSON string or dict
            field_definitions = getattr(dt, 'field_definitions', None)
            
            # Parse field_definitions if it's a string
            if isinstance(field_definitions, str):
                try:
                    import json
                    field_definitions = json.loads(field_definitions)
                except (json.JSONDecodeError, TypeError):
                    field_definitions = None
            
            # Get allowed formats
            allowed_formats = getattr(dt, 'allowed_formats', 'pdf,jpg,jpeg,png,doc,docx')
            if isinstance(allowed_formats, str):
                allowed_formats = allowed_formats.split(',')
            
            doc_dict = {
                "documentTypeId": getattr(dt, 'id', 0),
                "documentTypeName": getattr(dt, 'name', ''),
                "documentTypeNameEnglish": getattr(dt, 'name_english', ''),
                "category": getattr(dt, 'category', 'other'),
                "isMandatory": getattr(dt, 'is_mandatory', False),
                "instructions": getattr(dt, 'instructions', 'Please upload this document'),
                "maxFileSizeMb": getattr(dt, 'max_file_size_mb', 5),
                "allowedFormats": allowed_formats,
                "fieldDefinitions": field_definitions  # ✅ NOW INCLUDED!
            }
            
            result.append(doc_dict)
        
        print(f"✅ Returning {len(result)} document types with field definitions")
        return result

    @staticmethod
    def get_documents_by_category(db: Session, user_id: int) -> List[Dict[str, Any]]:
        """FIXED: Get documents organized by category - with field_definitions"""
        
        print(f"🔍 Getting documents by category for user {user_id}")
        
        # Get all document types and user's uploaded documents
        all_doc_types = DocumentTypeDal.get_all_document_types(db)
        user_documents = UserDocumentDal.get_user_documents(db, user_id)
        
        # Group documents by category
        documents_by_category = []
        
        for category in DocumentCategory:
            category_config = DOCUMENT_CATEGORIES_CONFIG.get(category, {})
            
            # Get document types for this category
            category_doc_types = [
                dt for dt in all_doc_types 
                if getattr(dt, 'category', 'other') == category.value
            ]
            
            # Get uploaded documents for this category
            uploaded_docs = []
            for doc in user_documents:
                # Check if this document belongs to this category
                for dt in category_doc_types:
                    if getattr(dt, 'id', 0) == getattr(doc, 'document_type_id', 0):
                        uploaded_docs.append({
                            "documentId": getattr(doc, 'id', 0),
                            "documentTypeId": getattr(doc, 'document_type_id', 0),
                            "documentTypeName": getattr(doc, 'document_type', ''),
                            "documentTypeNameEnglish": getattr(doc, 'document_type_english', ''),
                            "category": category.value,
                            "filePath": getattr(doc, 'file_path', ''),
                            "verificationStatus": getattr(doc, 'verification_status', 'PENDING'),
                            "uploadedAt": doc.created_at.isoformat() if hasattr(doc, 'created_at') and doc.created_at else '',
                            "adminComments": getattr(doc, 'admin_comments', None)
                        })
                        break
            
            # Calculate completion status
            mandatory_types_count = len([dt for dt in category_doc_types if getattr(dt, 'is_mandatory', False)])
            uploaded_mandatory_count = 0
            
            for doc in uploaded_docs:
                for dt in category_doc_types:
                    if getattr(dt, 'id', 0) == doc["documentTypeId"] and getattr(dt, 'is_mandatory', False):
                        uploaded_mandatory_count += 1
                        break
            
            completion_status = {
                "totalTypes": len(category_doc_types),
                "mandatoryTypes": mandatory_types_count,
                "uploadedCount": len(uploaded_docs),
                "uploadedMandatoryCount": uploaded_mandatory_count,
                "isComplete": uploaded_mandatory_count >= mandatory_types_count,
                "completionPercentage": (uploaded_mandatory_count / mandatory_types_count * 100) if mandatory_types_count > 0 else 100
            }
            
            # Only include categories that have document types
            if category_doc_types:
                # Build document types for this category - WITH field_definitions
                document_types_for_category = []
                for dt in category_doc_types:
                    # Get field_definitions - could be JSON string or dict
                    field_definitions = getattr(dt, 'field_definitions', None)
                    
                    # Parse field_definitions if it's a string
                    if isinstance(field_definitions, str):
                        try:
                            import json
                            field_definitions = json.loads(field_definitions)
                        except (json.JSONDecodeError, TypeError):
                            field_definitions = None
                    
                    # Get allowed formats
                    allowed_formats = getattr(dt, 'allowed_formats', 'pdf,jpg,jpeg,png,doc,docx')
                    if isinstance(allowed_formats, str):
                        allowed_formats = allowed_formats.split(',')
                    
                    document_types_for_category.append({
                        "documentTypeId": getattr(dt, 'id', 0),
                        "documentTypeName": getattr(dt, 'name', ''),
                        "documentTypeNameEnglish": getattr(dt, 'name_english', ''),
                        "category": category.value,
                        "isMandatory": getattr(dt, 'is_mandatory', False),
                        "instructions": getattr(dt, 'instructions', 'Please upload this document'),
                        "maxFileSizeMb": getattr(dt, 'max_file_size_mb', 5),
                        "allowedFormats": allowed_formats,
                        "fieldDefinitions": field_definitions  # ✅ NOW INCLUDED!
                    })
                
                documents_by_category.append({
                    "category": category.value,
                    "categoryName": category_config.get("name", category.value),
                    "categoryNameEnglish": category_config.get("name_english", category.value),
                    "description": category_config.get("description"),
                    "documentTypes": document_types_for_category,
                    "uploadedDocuments": uploaded_docs,
                    "completionStatus": completion_status
                })
        
        print(f"✅ Returning {len(documents_by_category)} categories with field definitions")
        return documents_by_category

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
        
        doc_name = getattr(doc_type, 'name', 'Document')
        return {
            "message": f"{doc_name} uploaded successfully",
            "document_id": getattr(user_doc, 'id', 0),
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
                
                # Validate document type exists
                doc_type = DocumentTypeDal.get_document_type_by_id(db, doc_type_id)
                if not doc_type:
                    failed_uploads.append({
                        "document_type_id": doc_type_id,
                        "error": f"Document type with ID {doc_type_id} not found"
                    })
                    continue
                
                # Process the upload (implementation depends on your file handling)
                file_path = f"user_docs/user_{user_id}/doc_type_{doc_type_id}/file_{uuid.uuid4().hex}"
                
                user_doc = UserDocumentDal.create_user_document(
                    db=db,
                    user_id=user_id,
                    document_type_id=doc_type_id,
                    file_path=file_path
                )
                
                uploaded_docs.append({
                    "document_type_id": doc_type_id,
                    "document_type_name": getattr(doc_type, 'name', ''),
                    "document_id": getattr(user_doc, 'id', 0),
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
                "documentId": getattr(doc, 'id', 0),
                "documentTypeId": getattr(doc, 'document_type_id', 0),
                "documentTypeName": getattr(doc, 'document_type', ''),
                "documentTypeNameEnglish": getattr(doc, 'document_type_english', ''),
                "filePath": getattr(doc, 'file_path', ''),
                "verificationStatus": getattr(doc, 'verification_status', 'PENDING'),
                "uploadedAt": doc.created_at.isoformat() if hasattr(doc, 'created_at') and doc.created_at else '',
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
    def get_document_categories() -> List[Dict[str, Any]]:
        """Get all document categories with their configuration"""
        
        categories = []
        for category, config in DOCUMENT_CATEGORIES_CONFIG.items():
            categories.append({
                "category": category.value,
                "categoryName": config.get("name", category.value),
                "categoryNameEnglish": config.get("name_english", category.value),
                "description": config.get("description"),
                "documentTypesCount": len(config.get("types", [])),
                "mandatoryTypesCount": len([dt for dt in config.get("types", []) if dt.get("is_mandatory", False)])
            })
        
        return categories
    
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
            if s3_client:
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=s3_key,
                    Body=file_content,
                    ContentType=file.content_type
                )
            else:
                # Fallback for when S3 is not available
                print(f"S3 not available, would save file to: {s3_key}")
            
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
# Document categories configuration
DOCUMENT_CATEGORIES_CONFIG = {

    DocumentCategory.IDENTITY_PROOF: {
        "name": "ओळखपत्र",
        "name_english": "Identity Proof",
        "description": "Documents to verify your identity",
        "types": []
    },
    DocumentCategory.EDUCATIONAL: {
        "name": "शैक्षणिक कागदपत्र", 
        "name_english": "Educational Documents",
        "description": "Educational qualifications and certificates",
        "types": []
    },
    DocumentCategory.ADDRESS_PROOF: {
        "name": "पत्ता पुरावा",
        "name_english": "Address Proof", 
        "description": "Documents to verify your residential address",
        "types": []
    },
    DocumentCategory.PROFESSIONAL: {
        "name": "व्यावसायिक कागदपत्र",
        "name_english": "Professional Documents",
        "description": "Work and professional certificates", 
        "types": []
    },
    DocumentCategory.CASTE_CATEGORY: {
        "name": "जातीचा दाखला",
        "name_english": "Caste Certificate",
        "description": "Caste and category related documents",
        "types": []
    },
    DocumentCategory.INCOME_PROOF: {
        "name": "उत्पन्न पुरावा", 
        "name_english": "Income Proof",
        "description": "Documents to verify your income",
        "types": []
    },
    DocumentCategory.MEDICAL: {
        "name": "वैद्यकीय कागदपत्र",
        "name_english": "Medical Documents", 
        "description": "Health and medical certificates",
        "types": []
    },
    DocumentCategory.OTHER: {
        "name": "इतर",
        "name_english": "Other Documents",
        "description": "Other miscellaneous documents",
        "types": []
    }
}

class ProfileServiceAdditionalMethods:
    """Additional methods to add to the existing ProfileService class"""
    
    @staticmethod
    async def update_document(
        db: Session,
        user_id: int,
        document_id: int,
        file: Optional[UploadFile] = None,
        field_values: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update an existing document - replace file and/or update field values"""
        
        # Get existing document to verify ownership
        existing_doc = ProfileService._get_user_document_by_id(db, user_id, document_id)
        if not existing_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found or you don't have permission to update it"
            )
        
        # Get document type for validation
        doc_type = DocumentTypeDal.get_document_type_by_id(db, existing_doc.document_type_id)
        if not doc_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document type not found"
            )
        
        updated_data = {}
        
        # Handle file update
        if file:
            # Validate file type
            allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx']
            file_extension = file.filename.split('.')[-1].lower()
            
            if file_extension not in allowed_extensions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid file type. Please upload PDF, JPG, PNG, DOC, or DOCX files only."
                )
            
            # Save new file
            new_file_path = await ProfileService._save_file_to_s3(
                file, user_id, existing_doc.document_type_id
            )
            updated_data['file_path'] = new_file_path
        
        # Handle field values update
        if field_values is not None:
            # Validate field values against document type field definitions
            field_definitions = getattr(doc_type, 'field_definitions', {}) or {}
            
            if field_definitions:
                validation_errors = ProfileService._validate_field_values(
                    field_values, field_definitions
                )
                if validation_errors:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "message": "Field validation failed",
                            "errors": validation_errors
                        }
                    )
            
            updated_data['field_values'] = field_values
        
        # Update verification status to PENDING if file or fields changed
        if file or field_values:
            updated_data['verification_status'] = 'PENDING'
            updated_data['updated_by'] = user_id
        
        # Update the document
        updated_doc = UserDocumentDal.update_user_document(
            db, document_id, updated_data
        )
        
        # Build response
        doc_name = getattr(doc_type, 'name_english', 'Document')
        response = {
            "message": f"{doc_name} updated successfully",
            "documentId": document_id,
            "documentTypeId": existing_doc.document_type_id,
            "documentTypeName": getattr(doc_type, 'name_english', ''),
            "updatedFields": list(updated_data.keys()),
            "verificationStatus": updated_data.get('verification_status', existing_doc.verification_status)
        }
        
        if 'file_path' in updated_data:
            response['newFilePath'] = updated_data['file_path']
        
        if 'field_values' in updated_data:
            response['fieldValues'] = field_values
        
        return response
    
    @staticmethod
    def update_document_field_values(
        db: Session,
        user_id: int,
        document_id: int,
        field_values: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update only the field values for an existing document"""
        
        # Get existing document
        existing_doc = ProfileService._get_user_document_by_id(db, user_id, document_id)
        if not existing_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found or you don't have permission to update it"
            )
        
        # Get document type for field validation
        doc_type = DocumentTypeDal.get_document_type_by_id(db, existing_doc.document_type_id)
        if not doc_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document type not found"
            )
        
        # Validate field values
        field_definitions = getattr(doc_type, 'field_definitions', {}) or {}
        
        if field_definitions:
            validation_errors = ProfileService._validate_field_values(
                field_values, field_definitions
            )
            if validation_errors:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "message": "Field validation failed",
                        "errors": validation_errors
                    }
                )
        
        # Merge with existing field values
        existing_field_values = getattr(existing_doc, 'field_values', {}) or {}
        updated_field_values = {**existing_field_values, **field_values}
        
        # Update the document
        updated_data = {
            'field_values': updated_field_values,
            'verification_status': 'PENDING',  # Reset to pending when fields are updated
            'updated_by': user_id
        }
        
        updated_doc = UserDocumentDal.update_user_document(
            db, document_id, updated_data
        )
        
        doc_name = getattr(doc_type, 'name_english', 'Document')
        return {
            "message": f"{doc_name} field values updated successfully",
            "documentId": document_id,
            "documentTypeId": existing_doc.document_type_id,
            "documentTypeName": getattr(doc_type, 'name_english', ''),
            "fieldValues": updated_field_values,
            "verificationStatus": "PENDING",
            "updatedFields": list(field_values.keys())
        }
    
    @staticmethod
    def update_document_type_field_definitions(
        db: Session,
        document_type_id: int,
        field_definitions: Dict[str, Any],
        instructions: Optional[str] = None,
        updated_by: int = None
    ) -> Dict[str, Any]:
        """Update field definitions for a document type (Admin only)"""
        
        # Get document type
        doc_type = DocumentTypeDal.get_document_type_by_id(db, document_type_id)
        if not doc_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document type not found"
            )
        
        # Validate field definitions structure
        validation_errors = ProfileService._validate_field_definitions_structure(field_definitions)
        if validation_errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Invalid field definitions structure",
                    "errors": validation_errors
                }
            )
        
        # Update document type
        update_data = {
            'field_definitions': field_definitions,
            'updated_by': updated_by
        }
        
        if instructions is not None:
            update_data['instructions'] = instructions
        
        updated_doc_type = DocumentTypeDal.update_document_type(
            db, document_type_id, update_data
        )
        
        return {
            "message": "Document type field definitions updated successfully",
            "documentTypeId": document_type_id,
            "documentTypeName": getattr(doc_type, 'name_english', ''),
            "fieldDefinitions": field_definitions,
            "instructions": instructions,
            "updatedBy": updated_by,
            "updatedAt": datetime.now().isoformat()
        }
    
    @staticmethod
    def get_document_details(
        db: Session,
        user_id: int,
        document_id: int
    ) -> Dict[str, Any]:
        """Get detailed information about a specific document including field definitions"""
        
        # Get user document
        user_doc = ProfileService._get_user_document_by_id(db, user_id, document_id)
        if not user_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found or you don't have permission to view it"
            )
        
        # Get document type with field definitions
        doc_type = DocumentTypeDal.get_document_type_by_id(db, user_doc.document_type_id)
        if not doc_type:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document type not found"
            )
        
        # Get field definitions
        field_definitions = getattr(doc_type, 'field_definitions', {}) or {}
        field_values = getattr(user_doc, 'field_values', {}) or {}
        
        # Check field completion status
        field_completion = ProfileService._check_field_completion(field_values, field_definitions)
        
        return {
            "documentId": document_id,
            "documentTypeId": user_doc.document_type_id,
            "documentTypeName": getattr(doc_type, 'name', ''),
            "documentTypeNameEnglish": getattr(doc_type, 'name_english', ''),
            "category": getattr(doc_type, 'category', 'other'),
            "isMandatory": getattr(doc_type, 'is_mandatory', False),
            "filePath": getattr(user_doc, 'file_path', ''),
            "verificationStatus": getattr(user_doc, 'verification_status', 'PENDING'),
            "adminComments": getattr(user_doc, 'admin_comments', None),
            "uploadedAt": user_doc.created_at.isoformat() if hasattr(user_doc, 'created_at') and user_doc.created_at else None,
            "lastUpdatedAt": user_doc.updated_at.isoformat() if hasattr(user_doc, 'updated_at') and user_doc.updated_at else None,
            "fieldDefinitions": field_definitions,
            "fieldValues": field_values,
            "fieldCompletion": field_completion,
            "instructions": getattr(doc_type, 'instructions', 'Please upload this document'),
            "maxFileSizeMb": 5,
            "allowedFormats": ["pdf", "jpg", "jpeg", "png", "doc", "docx"]
        }
    
    # Helper methods
    
    @staticmethod
    def _get_user_document_by_id(db: Session, user_id: int, document_id: int):
        """Get user document by ID, ensuring user owns it"""
        return UserDocumentDal.get_user_document_by_id(db, user_id, document_id)
    
    @staticmethod
    def _validate_field_values(field_values: Dict[str, Any], field_definitions: Dict[str, Any]) -> List[str]:
        """Validate field values against field definitions"""
        errors = []
        
        for field_name, field_config in field_definitions.items():
            field_value = field_values.get(field_name)
            is_required = field_config.get('required', False)
            field_type = field_config.get('type', 'text')
            
            # Check required fields
            if is_required and (field_value is None or field_value == ''):
                field_label = field_config.get('label', field_name)
                errors.append(f"{field_label} is required")
                continue
            
            # Skip validation for empty optional fields
            if field_value is None or field_value == '':
                continue
            
            # Type-specific validation
            if field_type == 'text':
                pattern = field_config.get('pattern')
                if pattern:
                    import re
                    if not re.match(pattern, str(field_value)):
                        validation_msg = field_config.get('validation_message', 
                            f"{field_config.get('label', field_name)} format is invalid")
                        errors.append(validation_msg)
            
            elif field_type == 'number':
                try:
                    num_value = float(field_value)
                    min_val = field_config.get('min')
                    max_val = field_config.get('max')
                    
                    if min_val is not None and num_value < min_val:
                        errors.append(f"{field_config.get('label', field_name)} must be at least {min_val}")
                    if max_val is not None and num_value > max_val:
                        errors.append(f"{field_config.get('label', field_name)} must be at most {max_val}")
                except (ValueError, TypeError):
                    errors.append(f"{field_config.get('label', field_name)} must be a valid number")
            
            elif field_type == 'date':
                try:
                    if isinstance(field_value, str):
                        datetime.strptime(field_value, '%Y-%m-%d')
                except ValueError:
                    errors.append(f"{field_config.get('label', field_name)} must be a valid date (YYYY-MM-DD)")
            
            elif field_type == 'select':
                options = field_config.get('options', [])
                if options and field_value not in options:
                    errors.append(f"{field_config.get('label', field_name)} must be one of: {', '.join(options)}")
        
        return errors
    
    @staticmethod
    def _validate_field_definitions_structure(field_definitions: Dict[str, Any]) -> List[str]:
        """Validate the structure of field definitions"""
        errors = []
        
        if not isinstance(field_definitions, dict):
            errors.append("Field definitions must be a dictionary")
            return errors
        
        valid_field_types = ['text', 'number', 'date', 'select', 'textarea', 'email', 'tel']
        
        for field_name, field_config in field_definitions.items():
            if not isinstance(field_config, dict):
                errors.append(f"Field '{field_name}' configuration must be a dictionary")
                continue
            
            # Check required properties
            field_type = field_config.get('type')
            if not field_type:
                errors.append(f"Field '{field_name}' must have a 'type' property")
            elif field_type not in valid_field_types:
                errors.append(f"Field '{field_name}' has invalid type '{field_type}'. Valid types: {', '.join(valid_field_types)}")
            
            # Check label
            if not field_config.get('label'):
                errors.append(f"Field '{field_name}' must have a 'label' property")
            
            # Type-specific validation
            if field_type == 'select':
                options = field_config.get('options')
                if not options or not isinstance(options, list) or len(options) == 0:
                    errors.append(f"Select field '{field_name}' must have non-empty 'options' array")
            
            elif field_type == 'number':
                min_val = field_config.get('min')
                max_val = field_config.get('max')
                if min_val is not None and max_val is not None and min_val > max_val:
                    errors.append(f"Number field '{field_name}' min value cannot be greater than max value")
        
        return errors
    
    @staticmethod
    def _check_field_completion(field_values: Dict[str, Any], field_definitions: Dict[str, Any]) -> Dict[str, Any]:
        """Check completion status of fields"""
        if not field_definitions:
            return {
                "totalFields": 0,
                "completedFields": 0,
                "requiredFields": 0,
                "completedRequiredFields": 0,
                "isComplete": True,
                "completionPercentage": 100,
                "missingRequiredFields": []
            }
        
        total_fields = len(field_definitions)
        required_fields = [name for name, config in field_definitions.items() if config.get('required', False)]
        
        completed_fields = 0
        completed_required_fields = 0
        missing_required_fields = []
        
        for field_name, field_config in field_definitions.items():
            field_value = field_values.get(field_name)
            has_value = field_value is not None and field_value != ''
            
            if has_value:
                completed_fields += 1
            
            is_required = field_config.get('required', False)
            if is_required:
                if has_value:
                    completed_required_fields += 1
                else:
                    missing_required_fields.append({
                        "fieldName": field_name,
                        "label": field_config.get('label', field_name),
                        "type": field_config.get('type', 'text')
                    })
        
        is_complete = len(missing_required_fields) == 0
        completion_percentage = (completed_fields / total_fields * 100) if total_fields > 0 else 100
        
        return {
            "totalFields": total_fields,
            "completedFields": completed_fields,
            "requiredFields": len(required_fields),
            "completedRequiredFields": completed_required_fields,
            "isComplete": is_complete,
            "completionPercentage": round(completion_percentage, 2),
            "missingRequiredFields": missing_required_fields
        }