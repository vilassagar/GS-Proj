from datetime import datetime
from app.models.otp import UserOTP
from app.services.dal.dto.to_camel import ToCamel


class UserOTPDTO(ToCamel):
    def __init__(
        self,
        id: int,
        user_id: int,
        otp: str,
        expires_at: datetime,
        message_sid: str
    ):
        self.id = id
        self.user_id = user_id
        self.otp = otp
        self.expires_at = expires_at
        self.message_sid = message_sid

    @staticmethod
    def to_dto(otp: UserOTP) -> "UserOTPDTO":
        return UserOTPDTO(
            id=otp.id,
            user_id=otp.user_id,
            otp=otp.otp,
            expires_at=otp.expires_at,
            message_sid=otp.message_sid
        )