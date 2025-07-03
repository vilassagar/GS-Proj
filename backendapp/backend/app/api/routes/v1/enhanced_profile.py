# app/api/routes/v1/enhanced_profile.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import json

from app.config import get_db
from app.dependencies.auth import get_current_user
from app.services.dal.dto.user_dto import UserDTO
from app.utils.vx_api_perms_utils import VxAPIPermsUtils, VxAPIPermsEnum

# Import the enhanced service
try:
    from app.services.enhanced_profile_service import EnhancedProfileService
except ImportError as e:
    print(f"Could not import EnhancedProfileService: {e}")
    EnhancedProfileService = None

router = APIRouter(
    prefix="/v1/profile",
    tags=["enhanced_profile"],
    responses={404: {"description": "Not Found"}}
)

# Get comprehensive profile with all documents
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/comprehensive', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/comprehensive")
async def get_comprehensive_profile(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive user profile with ALL document types and their status"""
    try:
        if not EnhancedProfileService:
            return {"error": "EnhancedProfileService not available"}
        
        return EnhancedProfileService.get_comprehensive_user_profile(db, current_user.user_id)
    except Exception as e:
        print(f"Error in get_comprehensive_profile: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving comprehensive profile: {str(e)}"
        )

# Get documents by status filter
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/documents/status', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/documents/status")
async def get_documents_by_status(
    status_filter: Optional[str] = Query(None, description="Filter by status: NOT_UPLOADED, UPLOADED, PENDING_VERIFICATION, APPROVED, REJECTED"),
    category: Optional[str] = Query(None, description="Filter by category"),
    mandatory_only: Optional[bool] = Query(False, description="Show only mandatory documents"),
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get documents filtered by status, category, or mandatory flag"""
    try:
        if not EnhancedProfileService:
            return {"error": "EnhancedProfileService not available"}
        
        # Get comprehensive profile
        profile = EnhancedProfileService.get_comprehensive_user_profile(db, current_user.user_id)
        documents = profile["allDocuments"]
        
        # Apply filters
        if status_filter:
            documents = [doc for doc in documents if doc["status"] == status_filter.upper()]
        
        if category:
            documents = [doc for doc in documents if doc["category"] == category]
        
        if mandatory_only:
            documents = [doc for doc in documents if doc["isMandatory"]]
        
        return {
            "userId": current_user.user_id,
            "filters": {
                "status": status_filter,
                "category": category,
                "mandatoryOnly": mandatory_only
            },
            "totalDocuments": len(documents),
            "documents": documents
        }
    
    except Exception as e:
        print(f"Error in get_documents_by_status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving documents: {str(e)}"
        )

# Get action items for the user
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/action-items', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/action-items")
async def get_user_action_items(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get action items and next steps for the user"""
    try:
        if not EnhancedProfileService:
            return {"error": "EnhancedProfileService not available"}
        
        profile = EnhancedProfileService.get_comprehensive_user_profile(db, current_user.user_id)
        
        return {
            "userId": current_user.user_id,
            "actionItems": profile["actionItems"],
            "summary": profile["documentsSummary"],
            "canSubmitProfile": profile["canSubmitProfile"],
            "profileCompletionPercentage": profile["documentsSummary"]["overallCompletionPercentage"]
        }
    
    except Exception as e:
        print(f"Error in get_user_action_items: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving action items: {str(e)}"
        )

# Get documents by category
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/documents/categories', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/documents/categories")
async def get_documents_by_categories(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get documents organized by categories with completion status"""
    try:
        if not EnhancedProfileService:
            return {"error": "EnhancedProfileService not available"}
        
        profile = EnhancedProfileService.get_comprehensive_user_profile(db, current_user.user_id)
        
        return {
            "userId": current_user.user_id,
            "documentsByCategory": profile["documentsByCategory"],
            "summary": profile["documentsSummary"]
        }
    
    except Exception as e:
        print(f"Error in get_documents_by_categories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving documents by category: {str(e)}"
        )

# Get missing documents (both mandatory and optional)
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/documents/missing', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/documents/missing")
async def get_missing_documents(
    include_optional: bool = Query(True, description="Include optional documents"),
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all missing documents (not uploaded)"""
    try:
        if not EnhancedProfileService:
            return {"error": "EnhancedProfileService not available"}
        
        profile = EnhancedProfileService.get_comprehensive_user_profile(db, current_user.user_id)
        documents = profile["allDocuments"]
        
        # Filter for missing documents
        missing_docs = [doc for doc in documents if doc["status"] == "NOT_UPLOADED"]
        
        if not include_optional:
            missing_docs = [doc for doc in missing_docs if doc["isMandatory"]]
        
        # Separate mandatory and optional
        mandatory_missing = [doc for doc in missing_docs if doc["isMandatory"]]
        optional_missing = [doc for doc in missing_docs if not doc["isMandatory"]]
        
        return {
            "userId": current_user.user_id,
            "summary": {
                "totalMissing": len(missing_docs),
                "mandatoryMissing": len(mandatory_missing),
                "optionalMissing": len(optional_missing)
            },
            "mandatoryDocuments": mandatory_missing,
            "optionalDocuments": optional_missing,
            "canSubmitProfile": len(mandatory_missing) == 0,
            "nextSteps": [
                "Upload mandatory documents" if mandatory_missing else "All mandatory documents uploaded",
                f"Consider uploading {len(optional_missing)} optional documents" if optional_missing else "All documents uploaded"
            ]
        }
    
    except Exception as e:
        print(f"Error in get_missing_documents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving missing documents: {str(e)}"
        )

# Dashboard summary endpoint
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/dashboard', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/dashboard")
async def get_profile_dashboard(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get profile dashboard with key metrics and action items"""
    try:
        if not EnhancedProfileService:
            return {"error": "EnhancedProfileService not available"}
        
        profile = EnhancedProfileService.get_comprehensive_user_profile(db, current_user.user_id)
        
        # Get high-priority action items only
        high_priority_actions = [action for action in profile["actionItems"] if action["priority"] == "HIGH"]
        
        return {
            "userId": current_user.user_id,
            "userName": f"{profile['basicDetails']['firstName']} {profile['basicDetails']['lastName']}",
            "profileStatus": profile["basicDetails"]["status"],
            "summary": profile["documentsSummary"],
            "highPriorityActions": high_priority_actions,
            "canSubmitProfile": profile["canSubmitProfile"],
            "quickStats": {
                "totalDocuments": profile["documentsSummary"]["totalDocumentTypes"],
                "uploadedDocuments": profile["documentsSummary"]["totalUploaded"],
                "pendingVerification": profile["documentsSummary"]["pendingVerification"],
                "approvedDocuments": profile["documentsSummary"]["approved"],
                "completionPercentage": profile["documentsSummary"]["overallCompletionPercentage"]
            },
            "lastUpdated": profile["lastUpdated"]
        }
    
    except Exception as e:
        print(f"Error in get_profile_dashboard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving profile dashboard: {str(e)}"
        )