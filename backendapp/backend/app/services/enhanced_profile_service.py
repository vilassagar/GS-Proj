# app/services/enhanced_profile_service.py
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import os
import uuid
from datetime import datetime
import json

from app.config import settings
from app.core.core_exceptions import NotFoundException, InvalidRequestException
from app.schemas.document_schema import DocumentCategory

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

# Import DAL classes
try:
    from app.services.dal.user_dal import UserDal
    from app.services.dal.document_dal import DocumentTypeDal, UserDocumentDal
    from app.services.dal.user_hierarchy_dal import DistrictDal, BlockDal, GramPanchayatDal
except ImportError as e:
    print(f"Import error: {e}")

def safe_get_field_definitions(doc_type):
    """Safely get field definitions from document type"""
    return getattr(doc_type, 'field_definitions', {}) or {}

class EnhancedProfileService:
    
    @staticmethod
    def get_comprehensive_user_profile(db: Session, user_id: int) -> Dict[str, Any]:
        """Get complete user profile with ALL document types and their status"""
        
        # Get user with details
        user = UserDal.get_user_details_by_id(db, user_id)
        if not user:
            raise NotFoundException(f"User with ID {user_id} not found")
        
        # Get ALL document types available in the system
        all_doc_types = DocumentTypeDal.get_all_document_types(db)
        
        # Get user's uploaded documents
        user_documents = UserDocumentDal.get_user_documents(db, user_id)
        
        # Create a map of uploaded documents by document_type_id
        uploaded_docs_map = {}
        for doc in user_documents:
            doc_type_id = getattr(doc, 'document_type_id', 0)
            uploaded_docs_map[doc_type_id] = doc
        
        # Build comprehensive document list
        all_documents_with_status = []
        mandatory_missing = 0
        total_mandatory = 0
        total_uploaded = 0
        
        for doc_type in all_doc_types:
            doc_type_id = getattr(doc_type, 'id', 0)
            is_mandatory = getattr(doc_type, 'is_mandatory', False)
            uploaded_doc = uploaded_docs_map.get(doc_type_id)
            
            # Count mandatory documents
            if is_mandatory:
                total_mandatory += 1
                if not uploaded_doc:
                    mandatory_missing += 1
            
            # Count uploaded documents
            if uploaded_doc:
                total_uploaded += 1
            
            # Determine document status
            if uploaded_doc:
                verification_status = getattr(uploaded_doc, 'verification_status', 'PENDING')
                if hasattr(verification_status, 'value'):
                    verification_status = verification_status.value
                else:
                    verification_status = str(verification_status)
                
                doc_status = "UPLOADED"
                if verification_status == 'APPROVED':
                    doc_status = "APPROVED"
                elif verification_status == 'REJECTED':
                    doc_status = "REJECTED"
                elif verification_status == 'PENDING':
                    doc_status = "PENDING_VERIFICATION"
            else:
                doc_status = "NOT_UPLOADED"
            
            # Get field definitions
            field_definitions = safe_get_field_definitions(doc_type)
            
            # Build document info
            doc_info = {
                "documentTypeId": doc_type_id,
                "documentTypeName": getattr(doc_type, 'name', ''),
                "documentTypeNameEnglish": getattr(doc_type, 'name_english', ''),
                "category": getattr(doc_type, 'category', 'other'),
                "isMandatory": is_mandatory,
                "status": doc_status,
                "instructions": getattr(doc_type, 'instructions', 'Please upload this document'),
                "fieldDefinitions": field_definitions,
                "maxFileSizeMb": 5,
                "allowedFormats": ["pdf", "jpg", "jpeg", "png", "doc", "docx"]
            }
            
            # Add upload details if document exists
            if uploaded_doc:
                doc_info.update({
                    "documentId": getattr(uploaded_doc, 'id', 0),
                    "filePath": getattr(uploaded_doc, 'file_path', ''),
                    "uploadedAt": uploaded_doc.created_at.isoformat() if hasattr(uploaded_doc, 'created_at') and uploaded_doc.created_at else '',
                    "lastUpdatedAt": uploaded_doc.updated_at.isoformat() if hasattr(uploaded_doc, 'updated_at') and uploaded_doc.updated_at else '',
                    "verificationStatus": verification_status,
                    "adminComments": getattr(uploaded_doc, 'admin_comments', None),
                    "fieldValues": getattr(uploaded_doc, 'field_values', {}) or {}
                })
            else:
                doc_info.update({
                    "documentId": None,
                    "filePath": None,
                    "uploadedAt": None,
                    "lastUpdatedAt": None,
                    "verificationStatus": None,
                    "adminComments": None,
                    "fieldValues": {}
                })
            
            all_documents_with_status.append(doc_info)
        
        # Group documents by category
        documents_by_category = EnhancedProfileService._group_documents_by_category(all_documents_with_status)
        
        # Calculate completion percentages
        mandatory_completion = ((total_mandatory - mandatory_missing) / total_mandatory * 100) if total_mandatory > 0 else 100
        overall_completion = (total_uploaded / len(all_doc_types) * 100) if len(all_doc_types) > 0 else 100
        
        # Build basic details
        basic_details = {
            "userId": user.user_id,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "designation": user.designation.value if user.designation and hasattr(user.designation, 'value') else str(user.designation) if user.designation else None,
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
        
        # Determine permissions
        user_status = user.status.value if hasattr(user.status, 'value') else str(user.status)
        permissions = {
            "canEditBasicDetails": user_status in ['PENDING', 'REJECTED'],
            "canUploadDocuments": True,
            "canDeleteDocuments": user_status != 'APPROVED'
        }
        
        # Generate action items
        action_items = EnhancedProfileService._generate_action_items(all_documents_with_status)
        
        return {
            "basicDetails": basic_details,
            "documentsSummary": {
                "totalDocumentTypes": len(all_doc_types),
                "totalMandatory": total_mandatory,
                "totalUploaded": total_uploaded,
                "mandatoryMissing": mandatory_missing,
                "pendingVerification": len([d for d in all_documents_with_status if d["status"] == "PENDING_VERIFICATION"]),
                "approved": len([d for d in all_documents_with_status if d["status"] == "APPROVED"]),
                "rejected": len([d for d in all_documents_with_status if d["status"] == "REJECTED"]),
                "mandatoryCompletionPercentage": round(mandatory_completion, 2),
                "overallCompletionPercentage": round(overall_completion, 2)
            },
            "allDocuments": all_documents_with_status,
            "documentsByCategory": documents_by_category,
            "actionItems": action_items,
            "permissions": permissions,
            "canSubmitProfile": mandatory_missing == 0,
            "lastUpdated": datetime.now().isoformat()
        }
    
    @staticmethod
    def _group_documents_by_category(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Group documents by category with category metadata"""
        
        categories = {}
        
        for doc in documents:
            category = doc.get("category", "other")
            
            if category not in categories:
                # Get category config
                category_enum = None
                for cat_enum in DocumentCategory:
                    if cat_enum.value == category:
                        category_enum = cat_enum
                        break
                
                category_config = DOCUMENT_CATEGORIES_CONFIG.get(category_enum, {
                    "name": category,
                    "name_english": category,
                    "description": f"Documents in {category} category"
                })
                
                categories[category] = {
                    "categoryId": category,
                    "categoryName": category_config.get("name", category),
                    "categoryNameEnglish": category_config.get("name_english", category),
                    "description": category_config.get("description", ""),
                    "documents": [],
                    "summary": {
                        "total": 0,
                        "mandatory": 0,
                        "uploaded": 0,
                        "approved": 0,
                        "pending": 0,
                        "rejected": 0,
                        "notUploaded": 0
                    }
                }
            
            # Add document to category
            categories[category]["documents"].append(doc)
            
            # Update category summary
            summary = categories[category]["summary"]
            summary["total"] += 1
            
            if doc["isMandatory"]:
                summary["mandatory"] += 1
            
            if doc["status"] == "NOT_UPLOADED":
                summary["notUploaded"] += 1
            elif doc["status"] == "APPROVED":
                summary["uploaded"] += 1
                summary["approved"] += 1
            elif doc["status"] == "PENDING_VERIFICATION":
                summary["uploaded"] += 1
                summary["pending"] += 1
            elif doc["status"] == "REJECTED":
                summary["uploaded"] += 1
                summary["rejected"] += 1
            elif doc["status"] == "UPLOADED":
                summary["uploaded"] += 1
        
        # Calculate completion percentages for each category
        for category_data in categories.values():
            summary = category_data["summary"]
            if summary["total"] > 0:
                summary["completionPercentage"] = round((summary["uploaded"] / summary["total"]) * 100, 2)
            else:
                summary["completionPercentage"] = 0
        
        return categories
    
    @staticmethod
    def _generate_action_items(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate actionable items for the user"""
        
        action_items = []
        
        # Find mandatory documents not uploaded
        mandatory_missing = [d for d in documents if d["isMandatory"] and d["status"] == "NOT_UPLOADED"]
        if mandatory_missing:
            action_items.append({
                "priority": "HIGH",
                "action": "UPLOAD_MANDATORY",
                "title": "Upload Mandatory Documents",
                "description": f"Please upload {len(mandatory_missing)} mandatory documents to complete your profile",
                "count": len(mandatory_missing),
                "documents": [{"id": d["documentTypeId"], "name": d["documentTypeNameEnglish"]} for d in mandatory_missing[:3]]
            })
        
        # Find rejected documents
        rejected_docs = [d for d in documents if d["status"] == "REJECTED"]
        if rejected_docs:
            action_items.append({
                "priority": "HIGH",
                "action": "REUPLOAD_REJECTED",
                "title": "Re-upload Rejected Documents",
                "description": f"Please re-upload {len(rejected_docs)} rejected documents with corrections",
                "count": len(rejected_docs),
                "documents": [{"id": d["documentTypeId"], "name": d["documentTypeNameEnglish"]} for d in rejected_docs[:3]]
            })
        
        # Find pending verification
        pending_docs = [d for d in documents if d["status"] == "PENDING_VERIFICATION"]
        if pending_docs:
            action_items.append({
                "priority": "MEDIUM",
                "action": "WAIT_VERIFICATION",
                "title": "Documents Under Verification",
                "description": f"{len(pending_docs)} documents are pending admin verification",
                "count": len(pending_docs),
                "documents": [{"id": d["documentTypeId"], "name": d["documentTypeNameEnglish"]} for d in pending_docs[:3]]
            })
        
        # Find optional documents not uploaded
        optional_missing = [d for d in documents if not d["isMandatory"] and d["status"] == "NOT_UPLOADED"]
        if optional_missing and not mandatory_missing:  # Only suggest if mandatory is complete
            action_items.append({
                "priority": "LOW",
                "action": "UPLOAD_OPTIONAL",
                "title": "Upload Optional Documents",
                "description": f"Consider uploading {len(optional_missing)} optional documents to strengthen your profile",
                "count": len(optional_missing),
                "documents": [{"id": d["documentTypeId"], "name": d["documentTypeNameEnglish"]} for d in optional_missing[:3]]
            })
        
        return action_items