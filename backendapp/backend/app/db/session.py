# app/db/session.py
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the declarative base
Base = declarative_base()

# Get the database URI from settings
db_uri = settings.SQLALCHEMY_DATABASE_URI
logger.info(f"Using database URI: {db_uri}")

# Create engine with echo for SQL debugging
engine = create_engine(db_uri, pool_pre_ping=True, echo=True)
logger.info("SQLAlchemy engine created successfully")

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.info("SessionLocal created successfully")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()