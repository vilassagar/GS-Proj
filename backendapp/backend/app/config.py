from pydantic_settings import BaseSettings
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
from typing import Optional

# Todo add modifications as per the working env
load_dotenv(".env", override=True)


class Settings(BaseSettings):
    '''
        Settings class to set the environment variables
    '''
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Gram Sevak Seva portal"

    # Database Details
    database_url: str = os.getenv("DATABASE_URL", "")

    # Twilio details
    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_phone_number: str = os.getenv("TWILIO_PHONE_NUMBER", "")

    # AUTH - JWT and Access Token
    access_token_expiry: int = int(os.getenv("ACCESS_TOKEN_EXPIRY", "15"))
    refresh_token_expiry: int = int(os.getenv("REFRESH_TOKEN_EXPIRY", "60"))

    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")

    # Common Utils vars
    otp_expiry_time: int = 5

    aws_s3_bucket: str = "egramdisha-files"

    # AWS Configuration (optional fields)
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_default_region: Optional[str] = None

    # Application Environment (optional fields)
    environment: Optional[str] = "development"
    debug: Optional[bool] = True
    
    # Development settings
    bypass_otp: Optional[bool] = True  # Set to False in production

    # UPLOAD_FOLDER: str = "upload/"
    # ALLOWED_EXTENSIONS: set = {"pdf", "jpg", "jpeg", "png"}

    class Config:
        env_file = ".env"
        # Allow extra fields that might be in .env but not defined in the model
        extra = "ignore"


settings = Settings()


# Setting up database
DATABASE_URL = settings.database_url


engine = create_engine(
    # Todo check other parameters
    DATABASE_URL
)

print("Connection to DB established. Database URL: ", DATABASE_URL)

# Creating DB session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Creating Base for models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()