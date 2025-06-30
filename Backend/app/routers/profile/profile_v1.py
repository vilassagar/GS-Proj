# app/routers/profile/profile_v1.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import json

from app.config import get_db
from app.dependencies.auth import get_current_user
from app.services.dal.dto.user_dto import UserDTO
from app.utils.vx_api_perms_utils import VxAPIPermsUtils, VxAPIPermsEnum
from app.schemas.profile_schema import (
    ProfileBasicDetailsUpdate,
    ProfileResponse, 
    ProfileValidationResponse
)
from app.schemas.profile_schema import (
    ProfileBasicDetailsUpdate,
    ProfileResponse, 
    ProfileValidationResponse,
    ProfileDocumentResponse  # Add this missing import
)
# Try importing the service and DALs
try:
    from app.services.profile_service import ProfileService
except ImportError as e:
    print(f"Could not import ProfileService: {e}")
    ProfileService = None

try:
    from app.services.dal.user_dal import UserDal
except ImportError as e:
    print(f"Could not import UserDal: {e}")
    UserDal = None


#end of imports

router = APIRouter(
    prefix="/v1/profile",
    tags=["profile"],
    responses={404: {"description": "Not Found"}}
)

# Simple test endpoint
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/test', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/test")
async def test_profile_endpoint(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Simple test endpoint to verify profile service works"""
    try:
        if not UserDal:
            return {"error": "UserDal not available", "imports": "failed"}
        
        user = UserDal.get_user_by_id(db, current_user.user_id)
        if not user:
            return {"error": "User not found", "user_id": current_user.user_id}
        
        return {
            "success": True,
            "userId": user.user_id,
            "name": f"{user.first_name} {user.last_name}",
            "status": str(user.status),
            "imports": "working"
        }
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "user_id": getattr(current_user, 'user_id', 'unknown')
        }

# Get current user's profile with all details
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/me', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/me")
async def get_my_profile(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's complete profile including basic details and documents"""
    try:
        if not ProfileService:
            return {"error": "ProfileService not available"}
        
        return ProfileService.get_user_profile(db, current_user.user_id)
    except Exception as e:
        print(f"Error in get_my_profile: {e}")
        import traceback
        traceback.print_exc()
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "user_id": current_user.user_id
        }

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
        return ProfileService.get_user_profile(db, user_id)
    except Exception as e:
        print(f"Error in get_user_profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Update basic profile details
VxAPIPermsUtils.set_perm_put(path=router.prefix + '/basic-details', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.put("/basic-details")
async def update_basic_details(
    profile_data: ProfileBasicDetailsUpdate,
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's basic profile details"""
    return ProfileService.update_basic_details(
        db, current_user.user_id, profile_data
    )

# Upload single document
VxAPIPermsUtils.set_perm_post(path=router.prefix + '/documents/upload', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.post("/documents/upload")
async def upload_document(
    document_type_id: int = Form(...),
    additional_data: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a single document for the current user"""
    
    # Parse additional data if provided
    extra_data = {}
    if additional_data:
        try:
            extra_data = json.loads(additional_data)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON in additional_data"
            )
    
    return await ProfileService.upload_document(
        db, current_user.user_id, document_type_id, file, extra_data
    )

# Upload multiple documents (matching your React component)
VxAPIPermsUtils.set_perm_post(path=router.prefix + '/documents/upload-multiple', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.post("/documents/upload-multiple")
async def upload_multiple_documents(
    files_data: str = Form(..., description="JSON mapping document_type_id to file data"),
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload multiple documents at once
    files_data should be JSON like: {"1": "file1_data", "2": "file2_data"}
    """
    try:
        # Parse the files mapping
        files_mapping = json.loads(files_data)
        
        return await ProfileService.upload_multiple_documents(
            db, current_user.user_id, files_mapping
        )
        
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON in files_data"
        )

# Get user's uploaded documents
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/documents', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/documents", response_model=List[ProfileDocumentResponse])
async def get_my_documents(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's uploaded documents"""
    return ProfileService.get_user_documents(db, current_user.user_id)

# Delete a document
VxAPIPermsUtils.set_perm_delete(path=router.prefix + '/documents/{document_id}', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific document"""
    return ProfileService.delete_document(db, current_user.user_id, document_id)

# Get document master list (for dropdowns)
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/document-types', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/document-types")
async def get_document_types(
    category: Optional[str] = None,
    is_mandatory: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get available document types"""
    return ProfileService.get_document_types(db, category, is_mandatory)

# Validate profile completeness
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/validation', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/validation")
async def validate_profile(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if user's profile is complete and valid"""
    return ProfileService.validate_profile_completeness(db, current_user.user_id)