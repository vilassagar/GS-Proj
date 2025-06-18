# app/services/dal/otp_dal.py
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.otp import UserOTP
from app.services.dal.dto.otp_dto import UserOTPDTO

class UserOTPDal:
    @staticmethod
    def create_otp(db: Session, user_id: int, otp: str, expires_at: datetime) -> UserOTP:
        new_otp = UserOTP(user_id=user_id, otp=otp, expires_at=expires_at)
        db.add(new_otp)
        db.commit()
        db.refresh(new_otp)
        return new_otp

    @staticmethod
    def get_valid_otp(db: Session, user_id: int) -> Optional[UserOTPDTO]:
        otp = db.query(UserOTP).filter(
            UserOTP.user_id == user_id,
            UserOTP.expires_at > datetime.now()
        ).first()
        return UserOTPDTO.to_dto(otp) if otp else None