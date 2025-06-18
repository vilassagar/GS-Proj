from twilio.rest import Client
from app.config import settings
import os

# Load credentials from environment variables
TWILIO_ACCOUNT_SID = settings.twilio_account_sid
TWILIO_AUTH_TOKEN = settings.twilio_auth_token
TWILIO_PHONE_NUMBER = settings.twilio_phone_number
# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

def send_sms(phone_number: str, otp: str):
    """
    Sends an OTP via Twilio SMS
    """
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
        raise ValueError("Twilio credentials are missing. Set them in environment variables.")

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f"Your OTP is {otp}. It is valid for 5 minutes.",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )

    return message.sid  # Twilio returns a unique message ID
