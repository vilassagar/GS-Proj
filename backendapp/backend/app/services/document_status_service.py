# app/services/document_status_service.py - Document Upload Status and Progress Tracking
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

from app.services.dal.document_dal import DocumentTypeDal, UserDocumentDal
from app.services.dal.user_dal import UserDal
# from app.services.profile_service import safe_get_field_definitions

def safe_get_field_definitions(doc_type):
    """
    Dummy implementation for safe_get_field_definitions.
    Replace this with the actual logic or import if available.
    """
    return getattr(doc_type, 'field_definitions', {}) or {}

class DocumentStatus(str, Enum):
    NOT_UPLOADED = "NOT_UPLOADED"
    UPLOADED = "UPLOADED" 
    UPDATED = "UPDATED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"

class DocumentProgressService:
    
    @staticmethod
    def get_user_document_progress(db: Session, user_id: int) -> Dict[str, Any]:
        """
        Get comprehensive document upload progress for a user
        Shows: uploaded, missing, updated, and completion status
        """
        
        # Get user details
        user = UserDal.get_user_by_id(db, user_id)
        if not user:
            raise Exception(f"User with ID {user_id} not found")
        
        # Get all document types
        all_doc_types = DocumentTypeDal.get_all_document_types(db)
        mandatory_doc_types = [dt for dt in all_doc_types if getattr(dt, 'is_mandatory', False)]
        optional_doc_types = [dt for dt in all_doc_types if not getattr(dt, 'is_mandatory', False)]
        
        # Get user's uploaded documents
        user_documents = UserDocumentDal.get_user_documents(db, user_id)
        
        # Create document status mapping
        uploaded_docs_map = {}
        for doc in user_documents:
            doc_type_id = getattr(doc, 'document_type_id', 0)
            uploaded_docs_map[doc_type_id] = doc
        
        # Analyze mandatory documents
        mandatory_progress = DocumentProgressService._analyze_document_types(
            mandatory_doc_types, uploaded_docs_map, is_mandatory=True
        )
        
        # Analyze optional documents  
        optional_progress = DocumentProgressService._analyze_document_types(
            optional_doc_types, uploaded_docs_map, is_mandatory=False
        )
        
        # Calculate overall statistics
        total_mandatory = len(mandatory_doc_types)
        uploaded_mandatory = len([doc for doc in mandatory_progress if doc['status'] != DocumentStatus.NOT_UPLOADED])
        approved_mandatory = len([doc for doc in mandatory_progress if doc['status'] == DocumentStatus.APPROVED])
        
        total_optional = len(optional_doc_types)
        uploaded_optional = len([doc for doc in optional_progress if doc['status'] != DocumentStatus.NOT_UPLOADED])
        
        # Calculate completion percentages
        mandatory_completion = (uploaded_mandatory / total_mandatory * 100) if total_mandatory > 0 else 100
        approved_completion = (approved_mandatory / total_mandatory * 100) if total_mandatory > 0 else 100
        overall_completion = ((uploaded_mandatory + uploaded_optional) / (total_mandatory + total_optional) * 100) if (total_mandatory + total_optional) > 0 else 100
        
        # Get missing required documents
        missing_required = [doc for doc in mandatory_progress if doc['status'] == DocumentStatus.NOT_UPLOADED]
        
        # Get pending documents
        pending_documents = [doc for doc in mandatory_progress + optional_progress if doc['status'] == DocumentStatus.PENDING]
        
        # Get rejected documents that need re-upload
        rejected_documents = [doc for doc in mandatory_progress + optional_progress if doc['status'] == DocumentStatus.REJECTED]
        
        # Determine next steps
        next_steps = DocumentProgressService._generate_next_steps(
            missing_required, pending_documents, rejected_documents, approved_mandatory, total_mandatory
        )
        
        # Determine overall profile status
        profile_status = DocumentProgressService._determine_profile_status(
            missing_required, pending_documents, rejected_documents, approved_mandatory, total_mandatory
        )
        
        return {
            "userId": user_id,
            "profileStatus": profile_status,
            "lastUpdated": datetime.now().isoformat(),
            "statistics": {
                "totalDocumentTypes": total_mandatory + total_optional,
                "mandatoryDocuments": {
                    "total": total_mandatory,
                    "uploaded": uploaded_mandatory,
                    "approved": approved_mandatory,
                    "missing": len(missing_required),
                    "pending": len([doc for doc in pending_documents if doc['isMandatory']]),
                    "rejected": len([doc for doc in rejected_documents if doc['isMandatory']]),
                    "completionPercentage": round(mandatory_completion, 2),
                    "approvalPercentage": round(approved_completion, 2)
                },
                "optionalDocuments": {
                    "total": total_optional,
                    "uploaded": uploaded_optional,
                    "completionPercentage": round((uploaded_optional / total_optional * 100) if total_optional > 0 else 100, 2)
                },
                "overallCompletion": round(overall_completion, 2)
            },
            "mandatoryDocuments": mandatory_progress,
            "optionalDocuments": optional_progress,
            "missingRequired": missing_required,
            "pendingVerification": pending_documents,
            "rejectedDocuments": rejected_documents,
            "nextSteps": next_steps,
            "canSubmitProfile": len(missing_required) == 0 and len(rejected_documents) == 0
        }
    
    @staticmethod
    def _analyze_document_types(doc_types: List, uploaded_docs_map: Dict, is_mandatory: bool) -> List[Dict[str, Any]]:
        """Analyze document types and their upload status"""
        
        result = []
        
        for doc_type in doc_types:
            doc_type_id = getattr(doc_type, 'id', 0)
            uploaded_doc = uploaded_docs_map.get(doc_type_id)
            
            # Determine status
            if uploaded_doc:
                verification_status = getattr(uploaded_doc, 'verification_status', 'PENDING')
                if verification_status == 'APPROVED':
                    status = DocumentStatus.APPROVED
                elif verification_status == 'REJECTED':
                    status = DocumentStatus.REJECTED
                else:
                    status = DocumentStatus.PENDING
                
                # Check if document was updated (you can enhance this with update tracking)
                created_at = getattr(uploaded_doc, 'created_at', None)
                updated_at = getattr(uploaded_doc, 'updated_at', None)
                is_updated = updated_at and created_at and updated_at > created_at
                
                if is_updated and status != DocumentStatus.REJECTED:
                    status = DocumentStatus.UPDATED
            else:
                status = DocumentStatus.NOT_UPLOADED
                uploaded_doc = None
            
            # Get field definitions
            field_definitions = safe_get_field_definitions(doc_type)
            
            # Build document info
            doc_info = {
                "documentTypeId": doc_type_id,
                "documentTypeName": getattr(doc_type, 'name', ''),
                "documentTypeNameEnglish": getattr(doc_type, 'name_english', ''),
                "category": getattr(doc_type, 'category', 'other'),
                "isMandatory": is_mandatory,
                "status": status,
                "instructions": getattr(doc_type, 'instructions', 'Please upload this document'),
                "fieldDefinitions": field_definitions,
                "maxFileSizeMb": getattr(doc_type, 'max_file_size_mb', 5),
                "allowedFormats": getattr(doc_type, 'allowed_formats', 'pdf,jpg,jpeg,png,doc,docx').split(',') if isinstance(getattr(doc_type, 'allowed_formats', ''), str) else ["pdf", "jpg", "jpeg", "png", "doc", "docx"]
            }
            
            # Add upload details if document exists
            if uploaded_doc:
                doc_info.update({
                    "documentId": getattr(uploaded_doc, 'id', 0),
                    "filePath": getattr(uploaded_doc, 'file_path', ''),
                    "uploadedAt": uploaded_doc.created_at.isoformat() if hasattr(uploaded_doc, 'created_at') and uploaded_doc.created_at else '',
                    "lastUpdatedAt": uploaded_doc.updated_at.isoformat() if hasattr(uploaded_doc, 'updated_at') and uploaded_doc.updated_at else '',
                    "verificationStatus": getattr(uploaded_doc, 'verification_status', 'PENDING'),
                    "adminComments": getattr(uploaded_doc, 'admin_comments', None),
                    "fieldValues": getattr(uploaded_doc, 'field_values', {}) or {},
                    "hasFieldValues": bool(getattr(uploaded_doc, 'field_values', {})),
                    "isCompletelyFilled": DocumentProgressService._check_if_completely_filled(field_definitions, getattr(uploaded_doc, 'field_values', {}))
                })
            else:
                doc_info.update({
                    "documentId": None,
                    "filePath": None,
                    "uploadedAt": None,
                    "lastUpdatedAt": None,
                    "verificationStatus": None,
                    "adminComments": None,
                    "fieldValues": {},
                    "hasFieldValues": False,
                    "isCompletelyFilled": False
                })
            
            result.append(doc_info)
        
        return result
    
    @staticmethod
    def _check_if_completely_filled(field_definitions: Dict, field_values: Dict) -> bool:
        """Check if all required fields are filled"""
        if not field_definitions:
            return True  # No fields required
        
        field_values = field_values or {}
        
        for field_name, field_config in field_definitions.items():
            is_required = field_config.get('required', False)
            value = field_values.get(field_name)
            
            if is_required and (value is None or value == ""):
                return False
        
        return True
    
    @staticmethod
    def _generate_next_steps(missing_required: List, pending_documents: List, rejected_documents: List, approved_mandatory: int, total_mandatory: int) -> List[str]:
        """Generate actionable next steps for the user"""
        
        steps = []
        
        if missing_required:
            steps.append(f"Upload {len(missing_required)} missing mandatory documents")
        
        if rejected_documents:
            rejected_mandatory = [doc for doc in rejected_documents if doc['isMandatory']]
            if rejected_mandatory:
                steps.append(f"Re-upload {len(rejected_mandatory)} rejected mandatory documents")
        
        if pending_documents:
            pending_mandatory = [doc for doc in pending_documents if doc['isMandatory']]
            if pending_mandatory:
                steps.append(f"Wait for verification of {len(pending_mandatory)} pending documents")
        
        # Check for incomplete field values
        incomplete_docs = []
        for doc_list in [pending_documents, rejected_documents]:
            for doc in doc_list:
                if doc.get('documentId') and not doc.get('isCompletelyFilled', True):
                    incomplete_docs.append(doc['documentTypeNameEnglish'])
        
        if incomplete_docs:
            steps.append(f"Complete missing field information for: {', '.join(incomplete_docs[:3])}{'...' if len(incomplete_docs) > 3 else ''}")
        
        if not steps:
            if approved_mandatory == total_mandatory:
                steps.append("All mandatory documents approved! Profile is complete.")
            else:
                steps.append("Continue uploading optional documents to complete your profile.")
        
        return steps
    
    @staticmethod
    def _determine_profile_status(missing_required: List, pending_documents: List, rejected_documents: List, approved_mandatory: int, total_mandatory: int) -> str:
        """Determine overall profile status"""
        
        if missing_required or rejected_documents:
            return "INCOMPLETE"
        elif pending_documents:
            return "PENDING_VERIFICATION"
        elif approved_mandatory == total_mandatory:
            return "COMPLETE"
        else:
            return "IN_PROGRESS"
    
    @staticmethod
    def get_document_requirements_summary(db: Session, user_id: int) -> Dict[str, Any]:
        """Get a quick summary of document requirements"""
        
        progress = DocumentProgressService.get_user_document_progress(db, user_id)
        
        return {
            "userId": user_id,
            "profileStatus": progress["profileStatus"],
            "completionPercentage": progress["statistics"]["mandatoryDocuments"]["completionPercentage"],
            "totalRequired": progress["statistics"]["mandatoryDocuments"]["total"],
            "uploadedRequired": progress["statistics"]["mandatoryDocuments"]["uploaded"],
            "approvedRequired": progress["statistics"]["mandatoryDocuments"]["approved"],
            "missingCount": len(progress["missingRequired"]),
            "pendingCount": len(progress["pendingVerification"]),
            "rejectedCount": len(progress["rejectedDocuments"]),
            "nextSteps": progress["nextSteps"][:3],  # Top 3 next steps
            "canSubmitProfile": progress["canSubmitProfile"]
        }
    
    @staticmethod
    def get_documents_by_status(db: Session, user_id: int, status_filter: Optional[DocumentStatus] = None) -> List[Dict[str, Any]]:
        """Get documents filtered by status"""
        
        progress = DocumentProgressService.get_user_document_progress(db, user_id)
        all_docs = progress["mandatoryDocuments"] + progress["optionalDocuments"]
        
        if status_filter:
            return [doc for doc in all_docs if doc["status"] == status_filter]
        
        return all_docs
    
    @staticmethod
    def get_category_wise_progress(db: Session, user_id: int) -> Dict[str, Any]:
        """Get document progress organized by category"""
        
        progress = DocumentProgressService.get_user_document_progress(db, user_id)
        all_docs = progress["mandatoryDocuments"] + progress["optionalDocuments"]
        
        # Group by category
        categories = {}
        for doc in all_docs:
            category = doc["category"]
            if category not in categories:
                categories[category] = {
                    "categoryName": category,
                    "documents": [],
                    "stats": {
                        "total": 0,
                        "uploaded": 0,
                        "approved": 0,
                        "missing": 0,
                        "pending": 0,
                        "rejected": 0
                    }
                }
            
            categories[category]["documents"].append(doc)
            categories[category]["stats"]["total"] += 1
            
            if doc["status"] != DocumentStatus.NOT_UPLOADED:
                categories[category]["stats"]["uploaded"] += 1
            if doc["status"] == DocumentStatus.APPROVED:
                categories[category]["stats"]["approved"] += 1
            elif doc["status"] == DocumentStatus.NOT_UPLOADED:
                categories[category]["stats"]["missing"] += 1
            elif doc["status"] == DocumentStatus.PENDING:
                categories[category]["stats"]["pending"] += 1
            elif doc["status"] == DocumentStatus.REJECTED:
                categories[category]["stats"]["rejected"] += 1
        
        # Calculate completion percentages
        for category_data in categories.values():
            stats = category_data["stats"]
            stats["completionPercentage"] = round(
                (stats["uploaded"] / stats["total"] * 100) if stats["total"] > 0 else 100, 2
            )
        
        return {
            "userId": user_id,
            "categories": list(categories.values()),
            "summary": {
                "totalCategories": len(categories),
                "categoriesWithUploads": len([cat for cat in categories.values() if cat["stats"]["uploaded"] > 0])
            }
        }