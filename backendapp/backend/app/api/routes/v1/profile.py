# app/api/routes/v1/profile.py - Updated with document update endpoints
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import json

from app.config import get_db
from app.dependencies.auth import get_current_user
from app.services.dal.dto.user_dto import UserDTO
from app.utils.vx_api_perms_utils import VxAPIPermsUtils, VxAPIPermsEnum
from app.schemas.profile_schema import ProfileBasicDetailsUpdate
from app.schemas.document_schema import DocumentCategory

# Import the enhanced ProfileService
from app.services.profile_service import ProfileService

router = APIRouter(
    prefix="/v1/profile",
    tags=["profile"],
    responses={404: {"description": "Not Found"}}
)

# Test endpoint
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/test', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/test")
async def test_profile_endpoint(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Simple test endpoint to verify profile service works"""
    try:
        return {
            "success": True,
            "userId": current_user.user_id,
            "message": "Profile service is working"
        }
    except Exception as e:
        return {
            "error": str(e),
            "user_id": getattr(current_user, 'user_id', 'unknown')
        }

# Enhanced profile endpoint with ALL documents and their status
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/me', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/me")
async def get_my_profile(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's complete profile including:
    - Basic details
    - ALL document types (mandatory and optional)
    - Document submission status for each type
    - Completion statistics
    """
    try:
        profile_data = ProfileService.get_user_profile(db, current_user.user_id)
        
        return {
            "success": True,
            "data": profile_data
        }
    except Exception as e:
        print(f"Error in get_my_profile: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving profile: {str(e)}"
        )

# Get documents by status (PENDING, SUBMITTED, APPROVED, REJECTED)
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/documents/status', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/documents/status")
async def get_documents_by_status(
    status_filter: Optional[str] = Query(None, description="Filter by status: PENDING, SUBMITTED, APPROVED, REJECTED"),
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get documents filtered by their submission/verification status"""
    try:
        return ProfileService.get_documents_by_status(db, current_user.user_id, status_filter)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving documents: {str(e)}"
        )

# Get only pending documents that need to be uploaded
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/documents/pending', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/documents/pending")
async def get_pending_documents(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all pending documents that need to be uploaded (both mandatory and optional)"""
    try:
        return ProfileService.get_pending_documents(db, current_user.user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving pending documents: {str(e)}"
        )

# Get only mandatory documents with their status
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/documents/mandatory', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/documents/mandatory")
async def get_mandatory_documents(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all mandatory documents with their submission status"""
    try:
        profile_data = ProfileService.get_user_profile(db, current_user.user_id)
        
        return {
            "userId": current_user.user_id,
            "totalMandatoryDocuments": len(profile_data["mandatoryDocuments"]),
            "mandatoryDocuments": profile_data["mandatoryDocuments"],
            "pendingMandatoryDocuments": profile_data["pendingMandatoryDocuments"],
            "statistics": profile_data["documentStatistics"]["mandatoryDocuments"],
            "canSubmitProfile": len(profile_data["pendingMandatoryDocuments"]) == 0
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving mandatory documents: {str(e)}"
        )

# Get only optional documents with their status
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/documents/optional', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/documents/optional")
async def get_optional_documents(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all optional documents with their submission status"""
    try:
        profile_data = ProfileService.get_user_profile(db, current_user.user_id)
        
        return {
            "userId": current_user.user_id,
            "totalOptionalDocuments": len(profile_data["optionalDocuments"]), 
            "optionalDocuments": profile_data["optionalDocuments"],
            "statistics": profile_data["documentStatistics"]["optionalDocuments"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving optional documents: {str(e)}"
        )

# Get profile completion summary
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/completion-summary', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/completion-summary")
async def get_profile_completion_summary(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a quick summary of profile completion status"""
    try:
        profile_data = ProfileService.get_user_profile(db, current_user.user_id)
        
        return {
            "userId": current_user.user_id,
            "profileCompletionStatus": profile_data["profileCompletionStatus"],
            "documentStatistics": profile_data["documentStatistics"],
            "nextSteps": profile_data["nextSteps"],
            "pendingMandatoryCount": len(profile_data["pendingMandatoryDocuments"]),
            "canSubmitProfile": len(profile_data["pendingMandatoryDocuments"]) == 0,
            "lastUpdated": profile_data["lastUpdated"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving completion summary: {str(e)}"
        )

# Get specific user profile by ID (for admin use)
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/{user_id}', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/{user_id}")
async def get_user_profile(
    user_id: int,
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get any user's profile by ID (admin only)"""
    # Check if current user has permission to view other profiles
    if current_user.role_id not in [1, 2, 3] and current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to view this profile"
        )
    
    try:
        profile_data = ProfileService.get_user_profile(db, user_id)
        return {
            "success": True,
            "data": profile_data
        }
    except Exception as e:
        print(f"Error in get_user_profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Update basic profile details
VxAPIPermsUtils.set_perm_put(path=router.prefix + '/basic-details', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.put("/basic-details")
async def update_basic_details(
    profile_data: ProfileBasicDetailsUpdate,
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's basic profile details"""
    try:
        return ProfileService.update_basic_details(db, current_user.user_id, profile_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Upload single document
VxAPIPermsUtils.set_perm_post(path=router.prefix + '/documents/upload', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.post("/documents/upload")
async def upload_document(
    document_type_id: int = Form(...),
    field_values: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a single document for the current user"""
    
    # Parse field values if provided
    parsed_field_values = {}
    if field_values:
        try:
            parsed_field_values = json.loads(field_values)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON in field_values"
            )
    
    try:
        return await ProfileService.upload_document(
            db, current_user.user_id, document_type_id, file, parsed_field_values
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# NEW: Update existing document
VxAPIPermsUtils.set_perm_put(path=router.prefix + '/documents/{document_id}/update', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.put("/documents/{document_id}/update")
async def update_document(
    document_id: int,
    field_values: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing document (replace file and/or update field values)"""
    
    # Parse field values if provided
    parsed_field_values = {}
    if field_values:
        try:
            parsed_field_values = json.loads(field_values)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON in field_values"
            )
    
    try:
        return await ProfileService.update_document(
            db, current_user.user_id, document_id, file, parsed_field_values
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# NEW: Update only field values for a document
VxAPIPermsUtils.set_perm_patch(path=router.prefix + '/documents/{document_id}/fields', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.patch("/documents/{document_id}/fields")
async def update_document_field_values(
    document_id: int,
    field_values: Dict[str, Any],
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update only the field values for an existing document"""
    try:
        return ProfileService.update_document_field_values(
            db, current_user.user_id, document_id, field_values
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Get user's uploaded documents
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/documents', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/documents")
async def get_my_documents(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's uploaded documents"""
    try:
        return ProfileService.get_user_documents(db, current_user.user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Delete a document
VxAPIPermsUtils.set_perm_delete(path=router.prefix + '/documents/{document_id}', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific document"""
    try:
        return ProfileService.delete_document(db, current_user.user_id, document_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Get document master list
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/document-types', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/document-types")
async def get_document_types(
    category: Optional[str] = Query(None, description="Filter by document category"),
    is_mandatory: Optional[bool] = Query(None, description="Filter by mandatory status"),
    db: Session = Depends(get_db)
):
    """Get available document types, optionally filtered by category"""
    try:
        return ProfileService.get_document_types(db, category, is_mandatory)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# NEW: Admin endpoint to update document type field definitions
VxAPIPermsUtils.set_perm_put(path=router.prefix + '/admin/document-types/{document_type_id}/fields', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.put("/admin/document-types/{document_type_id}/fields")
async def update_document_type_field_definitions(
    document_type_id: int,
    field_definitions: Dict[str, Any],
    instructions: Optional[str] = None,
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update field definitions for a document type (Admin only)"""
    
    # Check admin permissions
    if current_user.role_id not in [1]:  # Only super admin
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Admin access required."
        )
    
    try:
        return ProfileService.update_document_type_field_definitions(
            db, document_type_id, field_definitions, instructions, current_user.user_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# NEW: Get document with its field definition requirements
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/documents/{document_id}/details', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/documents/{document_id}/details")
async def get_document_details(
    document_id: int,
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific document including field definitions"""
    try:
        return ProfileService.get_document_details(db, current_user.user_id, document_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Validate profile completeness
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/validation', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/validation")
async def validate_profile(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if user's profile is complete and valid"""
    try:
        return ProfileService.validate_profile_completeness(db, current_user.user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )