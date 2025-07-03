import random
import string

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from twilio.rest import Client

from app.config import settings
from app.core.core_exceptions import InvalidRequestException, NotFoundException
from app.models.enums.approval_status import ApprovalStatus
from app.schemas.user_schema import UserRegisterRequest
from app.services.dal.auth_dal import AuthDal
from app.services.dal.user_dal import UserDal
from app.services.dal.user_hierarchy_dal import GramPanchayatDal, BlockDal, DistrictDal
from app.utils.jwt_utils import VxJWTUtils


def send_otp_twilio(phone_number: str, otp: str):
    account_sid = "your_account_sid"
    auth_token = "your_auth_token"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Your OTP is {otp}. It is valid for 5 minutes.",
        from_="+your_twilio_number",
        to=phone_number
    )
    return message.sid


class AuthService:

    @staticmethod
    def send_otp(ph_no: str, db: Session):
        """
            Sending OTP for logging in - Development Mode (No SMS)
        """

        print("🔧 DEVELOPMENT MODE: OTP Service")

        user = UserDal.get_user_by_mobile(mobile_number=ph_no, db=db)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if we're in development mode
        is_development = (
            getattr(settings, 'environment', 'development') == 'development' or
            settings.twilio_account_sid == "your_twilio_account_sid_here" or
            settings.twilio_account_sid.startswith("your_")
        )

        if is_development:
            print(f"📱 DEVELOPMENT: Bypassing OTP for {ph_no}")
            print("💡 Using default OTP: 1111")
            
            # Store a fixed OTP for development
            AuthDal.store_otp(db, ph_no, "1111", "dev_bypass_mode")
            
            return {
                "message": "OTP bypassed in development mode", 
                "dev_otp": "1111",
                "message_id": "dev_bypass"
            }
        else:
            # Production mode - would use real Twilio
            # Generate a 6-digit OTP
            otp = ''.join(random.choices(string.digits, k=6))
            print("OTP generated: ", otp)
            
            try:
                # Import here to avoid errors if Twilio is not configured
                from app.utils.twilio_utils import send_sms
                message_sid = send_sms(ph_no, otp)
                AuthDal.store_otp(db, ph_no, otp, message_sid)
                
                return {"message": "OTP sent successfully", "message_id": message_sid}
                
            except Exception as e:
                print("Twilio Exception: ", e)
                raise HTTPException(status_code=500, detail="SMS service error")

    @staticmethod
    def verify_otp(mobile_number: str, otp: str, db: Session):

        user = UserDal.get_user_by_mobile_or_whatsapp_number(db=db, mobile_number=mobile_number)

        # In development, always accept "1111" as valid OTP
        is_development = (
            getattr(settings, 'environment', 'development') == 'development' or
            settings.twilio_account_sid == "your_twilio_account_sid_here"
        )
        
        if is_development and otp == "1111":
            print("🔧 DEVELOPMENT: Accepting default OTP 1111")
            otp_valid = True
        else:
            otp_valid = AuthDal.verify_user_otp(db=db, user_id=user.id, otp=otp)

        if not otp_valid:
            raise HTTPException(400, "Invalid or Expired OTP provided")

        access_token = VxJWTUtils.create_access_token(
            data={
                "user_id": user.id,
                "login": True,
            },
            expiry_delta=settings.access_token_expiry
        )

        return access_token, UserDal.get_user_details_by_id(db=db, user_id=user.id)

    @staticmethod
    def register_user(user_data: UserRegisterRequest, db: Session):

        print("User Data: ", user_data.__dict__)

        if UserDal.get_user_by_mobile_or_whatsapp_number(user_data.mobile_number, db):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with phone number {user_data.mobile_number} Already exists"
            )

        district = DistrictDal.get_district_by_id(db=db, district_id=user_data.district_id)

        if not district:
            raise NotFoundException(f"District with district id {user_data.district_id} Not Found")

        block = BlockDal.get_block_by_id(db=db, block_id=user_data.block_id)

        if not block:
            raise NotFoundException(f"block with block id {user_data.block_id} Not Found")

        # Checking if provided District ID is indeed the parent of provided block
        if district.district_id != block.district_id:
            HTTPException(403, "Provided block does not belong to the provided district")

        gram_panchayat = GramPanchayatDal.get_gram_panchayat_by_id(db=db, gp_id=user_data.gram_panchayat_id)

        block = BlockDal.get_block_by_id(db=db, block_id=user_data.block_id)
        if not block:
            raise NotFoundException(f"block with block id {user_data.block_id} Not Found")

        # Checking if provided block is indeed parent of grampanchayat
        if not gram_panchayat:
            raise NotFoundException(f"Gram Panchayat with id {user_data.gram_panchayat_id} Not Found")
        if gram_panchayat.block_id != block.block_id:
            raise HTTPException(403, "Provided gram panchayat does not belong to the provided block(Panchayat Samiti)")

        UserDal.create_user(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            mobile_number=user_data.mobile_number,
            whatsapp_number=user_data.whatsapp_number,
            designation=user_data.designation,
            district_id=user_data.district_id,
            block_id=user_data.block_id,
            gram_panchayat_id=user_data.gram_panchayat_id,
            # By default we are sending Approved
            status=ApprovalStatus.PENDING,
            db=db
        )
