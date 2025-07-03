from typing import Optional



from app.models.enums.user_designation import UserDesignation
from pydantic import EmailStr, Field,BaseModel
from app.schemas.base import CamelCaseModel

from pydantic import field_validator, EmailStr


class SendOtpRequestSchema(CamelCaseModel):
    """
        Send OTP Request schema for getting otp.
        Here We are validating the mobile number
    """
    mobile_number: str

    @field_validator('mobile_number')
    def validate_mobile_number(cls, value: str) -> str:
        """
            This will validate whether the number starts with + or it has only numbers
            todo check req.
        """

        if not value.startswith('+91'):
            raise ValueError("Phone number must start with '+91' and contain only digits")

        if not value[1:].isdigit():
            raise ValueError("Phone number must start with '+' and contain only digits")

        return value


class LoginRequestSchema(SendOtpRequestSchema):
    """ Login Schema """
    otp: str


class UserRegisterRequest(SendOtpRequestSchema):
    """
        Register User details
    """
    # districtId: 1,
    # blockId: 1,
    first_name: str
    last_name: str

    designation: UserDesignation

    # District
    district_id: int

    # Block
    block_id: int

    # gram_panchayats
    gram_panchayat_id: int

    mobile_number: str
    whatsapp_number: str

    # As discussed with Avdhoot keep email compulsory
    email: EmailStr


class MessageResponse(CamelCaseModel):
    message: str

