# app/routers/profile/minimal_profile_v1.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import get_db
from app.dependencies.auth import get_current_user
from app.services.dal.dto.user_dto import UserDTO
from app.utils.vx_api_perms_utils import VxAPIPermsUtils, VxAPIPermsEnum

router = APIRouter(
    prefix="/v1/profile",
    tags=["profile"],
    responses={404: {"description": "Not Found"}}
)

# Direct import in function to avoid import issues
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/me', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/me")
async def get_my_profile(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's complete profile including basic details and documents"""
    
    try:
        # Import here to avoid early import issues
        from app.services.dal.user_dal import UserDal
        
        user = UserDal.get_user_by_id(db, current_user.user_id)
        if not user:
            return {"error": f"User with ID {current_user.user_id} not found"}
        
        # Return basic profile structure that matches your React component
        return {
            "basicDetails": {
                "userId": user.user_id,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "designation": str(user.designation) if user.designation else None,
                "district": user.district.to_camel() if user.district else None,
                "block": user.block.to_camel() if user.block else None,
                "gramPanchayat": user.gram_panchayat.to_camel() if user.gram_panchayat else None,
                "mobileNumber": user.mobile_number,
                "whatsappNumber": user.whatsapp_number,
                "email": user.email,
                "status": str(user.status),
                "createdAt": user.created_at.isoformat() if user.created_at else None,
                "updatedAt": user.updated_at.isoformat() if user.updated_at else None
            },
            "documents": [],  # Empty for now
            "validation": {
                "isComplete": False,
                "missingBasicFields": [],
                "missingMandatoryDocuments": [],
                "pendingDocumentVerification": [],
                "completionPercentage": 75.0,
                "nextSteps": ["Complete profile setup"]
            },
            "permissions": {
                "canEditBasicDetails": True,
                "canUploadDocuments": True,
                "canDeleteDocuments": True
            }
        }
        
    except ImportError as e:
        return {"error": f"Import error: {str(e)}"}
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }

# Test endpoint
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/test', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/test")
async def test_profile_endpoint(
    current_user: UserDTO = Depends(get_current_user)
):
    """Simple test endpoint"""
    return {
        "success": True,
        "message": "Profile router is working",
        "currentUserId": current_user.user_id
    }