# app/routers/document_status/document_status_v1.py - Document Status Tracking Router
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.config import get_db
from app.dependencies.auth import get_current_user
from app.services.dal.dto.user_dto import UserDTO
from app.utils.vx_api_perms_utils import VxAPIPermsUtils, VxAPIPermsEnum

# Import the document progress service
try:
    from app.services.document_status_service import DocumentProgressService, DocumentStatus
except ImportError as e:
    print(f"Could not import DocumentProgressService: {e}")
    DocumentProgressService = None
    DocumentStatus = None

router = APIRouter(
    prefix="/v1/document-status",
    tags=["document_status"],
    responses={404: {"description": "Not Found"}}
)

# Get comprehensive document progress
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/progress', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/progress")
async def get_document_progress(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive document upload progress for current user
    Shows: uploaded, missing, updated, completion status, and next steps
    """
    try:
        if not DocumentProgressService:
            return {"error": "DocumentProgressService not available"}
        
        return DocumentProgressService.get_user_document_progress(db, current_user.user_id)
    
    except Exception as e:
        print(f"Error in get_document_progress: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving document progress: {str(e)}"
        )

# Get quick summary of document requirements
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/summary', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/summary")
async def get_document_requirements_summary(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a quick summary of document requirements and completion status
    Perfect for dashboard widgets or quick status checks
    """
    try:
        if not DocumentProgressService:
            return {"error": "DocumentProgressService not available"}
        
        return DocumentProgressService.get_document_requirements_summary(db, current_user.user_id)
    
    except Exception as e:
        print(f"Error in get_document_requirements_summary: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving document summary: {str(e)}"
        )

# Get documents by status
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/by-status', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/by-status")
async def get_documents_by_status(
    status_filter: Optional[str] = Query(None, description="Filter by status: NOT_UPLOADED, UPLOADED, PENDING, APPROVED, REJECTED, UPDATED"),
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get documents filtered by their upload/verification status
    Useful for showing specific document lists (e.g., only rejected documents)
    """
    try:
        if not DocumentProgressService or not DocumentStatus:
            return {"error": "DocumentProgressService not available"}
        
        # Validate status filter
        parsed_status = None
        if status_filter:
            try:
                parsed_status = DocumentStatus(status_filter.upper())
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status filter. Valid options: {[s.value for s in DocumentStatus]}"
                )
        
        documents = DocumentProgressService.get_documents_by_status(
            db, current_user.user_id, parsed_status
        )
        
        return {
            "userId": current_user.user_id,
            "statusFilter": status_filter,
            "totalDocuments": len(documents),
            "documents": documents
        }
    
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        print(f"Error in get_documents_by_status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving documents by status: {str(e)}"
        )

# Get category-wise progress
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/by-category', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/by-category")
async def get_category_wise_progress(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get document progress organized by category
    Shows completion status for each document category
    """
    try:
        if not DocumentProgressService:
            return {"error": "DocumentProgressService not available"}
        
        return DocumentProgressService.get_category_wise_progress(db, current_user.user_id)
    
    except Exception as e:
        print(f"Error in get_category_wise_progress: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving category-wise progress: {str(e)}"
        )

# Get missing required documents
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/missing', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/missing")
async def get_missing_required_documents(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of missing required/mandatory documents
    Shows what the user still needs to upload
    """
    try:
        if not DocumentProgressService:
            return {"error": "DocumentProgressService not available"}
        
        progress = DocumentProgressService.get_user_document_progress(db, current_user.user_id)
        
        return {
            "userId": current_user.user_id,
            "missingCount": len(progress["missingRequired"]),
            "missingDocuments": progress["missingRequired"],
            "nextSteps": progress["nextSteps"],
            "canSubmitProfile": progress["canSubmitProfile"]
        }
    
    except Exception as e:
        print(f"Error in get_missing_required_documents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving missing documents: {str(e)}"
        )

# Get pending verification documents
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/pending', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/pending")
async def get_pending_verification_documents(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of documents pending admin verification
    Shows what's been uploaded but waiting for approval
    """
    try:
        if not DocumentProgressService:
            return {"error": "DocumentProgressService not available"}
        
        progress = DocumentProgressService.get_user_document_progress(db, current_user.user_id)
        
        return {
            "userId": current_user.user_id,
            "pendingCount": len(progress["pendingVerification"]),
            "pendingDocuments": progress["pendingVerification"],
            "estimatedVerificationTime": "2-3 business days"  # You can make this configurable
        }
    
    except Exception as e:
        print(f"Error in get_pending_verification_documents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving pending documents: {str(e)}"
        )

# Get rejected documents that need re-upload
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/rejected', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/rejected")
async def get_rejected_documents(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of rejected documents that need to be re-uploaded
    Shows what was rejected and why (admin comments)
    """
    try:
        if not DocumentProgressService:
            return {"error": "DocumentProgressService not available"}
        
        progress = DocumentProgressService.get_user_document_progress(db, current_user.user_id)
        
        return {
            "userId": current_user.user_id,
            "rejectedCount": len(progress["rejectedDocuments"]),
            "rejectedDocuments": progress["rejectedDocuments"],
            "actionRequired": "Please re-upload rejected documents with corrections"
        }
    
    except Exception as e:
        print(f"Error in get_rejected_documents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving rejected documents: {str(e)}"
        )

# Admin endpoint: Get document progress for any user
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/admin/{user_id}/progress', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/admin/{user_id}/progress")
async def get_user_document_progress_admin(
    user_id: int,
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Admin endpoint: Get document progress for any user
    Requires admin permissions
    """
    # Check admin permissions
    if current_user.role_id not in [1, 2, 3]:  # Super admin, district admin, block admin
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Admin access required."
        )
    
    try:
        if not DocumentProgressService:
            return {"error": "DocumentProgressService not available"}
        
        return DocumentProgressService.get_user_document_progress(db, user_id)
    
    except Exception as e:
        print(f"Error in get_user_document_progress_admin: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user document progress: {str(e)}"
        )

# Get completion statistics
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/statistics', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/statistics")
async def get_completion_statistics(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed completion statistics
    Perfect for progress bars and completion widgets
    """
    try:
        if not DocumentProgressService:
            return {"error": "DocumentProgressService not available"}
        
        progress = DocumentProgressService.get_user_document_progress(db, current_user.user_id)
        
        return {
            "userId": current_user.user_id,
            "profileStatus": progress["profileStatus"],
            "statistics": progress["statistics"],
            "progressBreakdown": {
                "mandatoryDocuments": {
                    "completed": progress["statistics"]["mandatoryDocuments"]["uploaded"],
                    "total": progress["statistics"]["mandatoryDocuments"]["total"],
                    "percentage": progress["statistics"]["mandatoryDocuments"]["completionPercentage"]
                },
                "optionalDocuments": {
                    "completed": progress["statistics"]["optionalDocuments"]["uploaded"],
                    "total": progress["statistics"]["optionalDocuments"]["total"],
                    "percentage": progress["statistics"]["optionalDocuments"]["completionPercentage"]
                },
                "overall": {
                    "percentage": progress["statistics"]["overallCompletion"]
                }
            },
            "canSubmitProfile": progress["canSubmitProfile"],
            "lastUpdated": progress["lastUpdated"]
        }
    
    except Exception as e:
        print(f"Error in get_completion_statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving completion statistics: {str(e)}"
        )