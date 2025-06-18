from datetime import datetime, timedelta, timezone

from pytz import UTC
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.config import settings
from app.models.otp import UserOTP
from app.services.dal.user_dal import UserDal


class AuthDal:

    @staticmethod
    def store_otp(db: Session, mobile_number: str, otp: str, message_sid: str) -> None:
        """
            Storing OTP for the user with the OTP current time
            Only One OTP record will be present per User
        """

        # using the get user just for defensive programming strategy
        user = UserDal.get_user_by_mobile_or_whatsapp_number(db=db, mobile_number=mobile_number)

        if not user:
            raise Exception("User not found for OTP storage.")

        expires_at = datetime.now(UTC) + timedelta(minutes=settings.otp_expiry_time)

        # Look for an existing OTP entry for the user.
        otp_record = db.query(UserOTP).filter(UserOTP.user_id == user.id).first()

        # If user already has an entry in the OTP table, OTP will be updated
        if otp_record:
            # Update the existing OTP record.
            otp_record.otp = otp
            otp_record.expires_at_utc = expires_at
            otp_record.message_sid = message_sid

        else:
            # Create a new OTP record.
            otp_record = UserOTP(
                user_id=user.id,
                otp=otp,
                expires_at=expires_at,
                message_sid=message_sid
            )

            db.add(otp_record)

        # Commit the changes and refresh the record.
        db.commit()
        db.refresh(otp_record)

    @staticmethod
    def verify_user_otp(user_id: int, otp: str, db: Session) -> bool:

        otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.otp_expiry_time)

        # query = db.query(UserOTP)
        #
        # query = query.filter(and_(
        #     UserOTP.user_id == user_id,
        #     UserOTP.otp == otp,
        #     UserOTP.expires_at_utc < otp_expiry
        # )).scalar()
        return db.query(UserOTP).filter(and_(
            UserOTP.user_id == user_id,
            UserOTP.otp == otp,
            UserOTP.expires_at < otp_expiry
        )).scalar()
