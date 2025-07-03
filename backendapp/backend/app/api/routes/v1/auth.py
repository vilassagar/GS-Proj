from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import get_db
from app.models.enums.approval_status import ApprovalStatus
from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.schemas.user_schema import LoginRequestSchema, SendOtpRequestSchema, MessageResponse, UserRegisterRequest
from app.services.auth_service import AuthService
from app.utils.vx_api_perms_utils import VxAPIPermsUtils

router = APIRouter(
    prefix="/v1/auth",
    tags=["auth"],
    responses={404: {"description": "Not Found"}}
)

# This is how we are explicitly setting up the permissions for routers
VxAPIPermsUtils.set_perm_post(path=router.prefix + '/sendOtp', perm=VxAPIPermsEnum.PUBLIC)
@router.post(path="/sendOtp", summary="Login a user",
             description="Authentication of a user. Returns a JWT Token")
async def send_otp(user: SendOtpRequestSchema, db: Session = Depends(get_db)):
    AuthService.send_otp(ph_no=user.mobile_number, db=db)

    # return {"Message: ": "OTP generated successfully"}
    return MessageResponse(message="OTP generated successfully")


VxAPIPermsUtils.set_perm_post(path=router.prefix + '/login', perm=VxAPIPermsEnum.PUBLIC)
@router.post(path="/login", summary="Login a user",
             description="Authentication of a user. Returns a JWT Token")
async def login(login_info: LoginRequestSchema, db: Session = Depends(get_db)):
    access_token, user_with_details = AuthService.verify_otp(mobile_number=login_info.mobile_number,
                                                               otp=login_info.otp,
                                                               db=db)

    if user_with_details is None:
        return {"message": "User not found or invalid OTP"}, 404

    return {"message: ": "Logged in Successfully",
            "userId": user_with_details.id,
            "accessToken": access_token,
            "roleId": user_with_details.role.id if user_with_details.role else None,
            "roleName": user_with_details.role.name if user_with_details.role else None,
            "userEmail": user_with_details.email,
            "blockId": user_with_details.block_id,
            "blockName": user_with_details.block.block_name if user_with_details.block else None,
            "districtId": user_with_details.district_id,
            "distrcictName": user_with_details.district.district_name if user_with_details.district else None,
            "isApprovalPending": user_with_details.status != ApprovalStatus.APPROVED,
            "isDocumentUploadComplete": user_with_details.documents_uploaded,
            # Todo take necessary details later
            # "User": user_with_details
            }


VxAPIPermsUtils.set_perm_post(path=router.prefix + '/register', perm=VxAPIPermsEnum.PUBLIC)
@router.post("/register", response_model=MessageResponse, description="Registering Gram Sevak User ")
def register_user(user_data: UserRegisterRequest, db: Session = Depends(get_db)):
    AuthService.register_user(user_data=user_data, db=db)

    return MessageResponse(message="User registration successful")
