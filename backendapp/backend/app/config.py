from pydantic_settings import BaseSettings
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool, StaticPool
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import time

# Load environment variables
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

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

# Setting up database
DATABASE_URL = settings.database_url

# Determine database type from URL
def get_database_type(url: str) -> str:
    if url.startswith("sqlite"):
        return "sqlite"
    elif url.startswith("postgresql") or url.startswith("postgres"):
        return "postgresql"
    elif url.startswith("mysql"):
        return "mysql"
    else:
        return "unknown"

DB_TYPE = get_database_type(DATABASE_URL)

# Configure engine based on database type
if DB_TYPE == "sqlite":
    engine = create_engine(
        DATABASE_URL,
        poolclass=StaticPool,
        connect_args={
            "check_same_thread": False,  # SQLite specific
            "timeout": 10
        },
        echo=settings.debug  # Log SQL queries in debug mode
    )
else:
    # PostgreSQL/MySQL configuration
    engine = create_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
        connect_args={"connect_timeout": 10},
        echo=settings.debug
    )

print(f"Connection to {DB_TYPE.upper()} database established. Database URL: {DATABASE_URL}")

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


def check_database_health() -> Dict[str, Any]:
    """
    Comprehensive database health check
    Returns detailed information about database connectivity and performance
    """
    health_info = {
        "status": "unknown",
        "connection": False,
        "response_time_ms": None,
        "database_type": DB_TYPE,
        "database_url": DATABASE_URL[:20] + "..." if DATABASE_URL and len(DATABASE_URL) > 20 else DATABASE_URL,
        "error": None
    }
    
    # Check if DATABASE_URL is configured
    if not DATABASE_URL:
        health_info["status"] = "unhealthy"
        health_info["error"] = "DATABASE_URL is not configured"
        return health_info
    
    try:
        # Create a separate engine for health checks
        if DB_TYPE == "sqlite":
            health_engine = create_engine(
                DATABASE_URL,
                poolclass=StaticPool,
                connect_args={
                    "check_same_thread": False,
                    "timeout": 5
                }
            )
        else:
            health_engine = create_engine(
                DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=300,
                connect_args={"connect_timeout": 5}
            )
        
        start_time = time.time()
        
        # Test basic connectivity
        with health_engine.connect() as connection:
            # Simple connectivity test
            result = connection.execute(text("SELECT 1 as health_check"))
            row = result.fetchone()
            
            if row is None:
                health_info["status"] = "unhealthy"
                health_info["error"] = "Database query returned no results"
                return health_info
                
            if len(row) == 0 or row[0] != 1:
                health_info["status"] = "unhealthy"
                health_info["error"] = "Database connectivity test failed"
                return health_info
                
            health_info["connection"] = True
            
            # Test database responsiveness with appropriate query for DB type
            try:
                if DB_TYPE == "sqlite":
                    table_result = connection.execute(text("SELECT COUNT(*) FROM sqlite_master WHERE type='table'"))
                else:
                    table_result = connection.execute(text("SELECT COUNT(*) FROM information_schema.tables"))
                
                table_row = table_result.fetchone()
                if table_row is not None:
                    health_info["table_count"] = table_row[0]
            except Exception as table_error:
                # Don't fail the whole health check if table count fails
                health_info["table_count_error"] = str(table_error)
            
            # Calculate response time
            response_time = (time.time() - start_time) * 1000
            health_info["response_time_ms"] = round(response_time, 2)
            
            # Determine status based on response time
            if response_time < 100:
                health_info["status"] = "healthy"
            elif response_time < 500:
                health_info["status"] = "warning"
            else:
                health_info["status"] = "slow"
                
        health_engine.dispose()  # Clean up the health check engine
        
    except SQLAlchemyError as e:
        health_info["status"] = "unhealthy"
        health_info["error"] = f"Database error: {str(e)}"
    except Exception as e:
        health_info["status"] = "unhealthy" 
        health_info["error"] = f"Connection error: {str(e)}"
    
    return health_info


def check_database_connection() -> bool:
    """
    Simple boolean check for database connectivity
    Used for basic health checks
    """
    if not DATABASE_URL:
        return False
        
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            row = result.fetchone()
            return row is not None and len(row) > 0 and row[0] == 1
    except Exception:
        return False


def get_database_info() -> Dict[str, Any]:
    """
    Get basic database information
    """
    if not DATABASE_URL:
        return {
            "type": "none",
            "error": "DATABASE_URL not configured"
        }
    
    try:
        with engine.connect() as connection:
            if DB_TYPE == "sqlite":
                version_result = connection.execute(text("SELECT sqlite_version()"))
                version_row = version_result.fetchone()
                version = version_row[0] if version_row else "unknown"
                
                tables_result = connection.execute(text(
                    "SELECT COUNT(*) FROM sqlite_master WHERE type='table'"
                ))
                tables_row = tables_result.fetchone()
                table_count = tables_row[0] if tables_row else 0
                
            else:
                version_result = connection.execute(text("SELECT version()"))
                version_row = version_result.fetchone()
                version = version_row[0].split()[0] if version_row else "unknown"
                
                tables_result = connection.execute(text("""
                    SELECT COUNT(*) FROM information_schema.tables 
                    WHERE table_schema = 'public'
                """))
                tables_row = tables_result.fetchone()
                table_count = tables_row[0] if tables_row else 0
            
            return {
                "type": DB_TYPE,
                "version": version,
                "table_count": table_count,
                "url_masked": DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else "local"
            }
            
    except Exception as e:
        return {
            "type": DB_TYPE,
            "error": str(e)
        }