import os
import sys
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your Base from the models
from app.config import Base

# IMPORTANT: Import ALL your model files here so they register with Base.metadata
from app.models.users import User
from app.models.roles import Role
from app.models.users_hierarchy import District, Block, GramPanchayat
from app.models.department import Department
from app.models.gr_yojana import Yojana, GR
from app.models.books import Book
from app.models.documents import DocumentType, UserDocument
from app.models.otp import UserOTP

# Load environment variables from .env file
load_dotenv()

# Get the Alembic configuration
config = context.config

# Interpret the config file for logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Get the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Set the sqlalchemy.url in alembic config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Set the metadata of models for auto-generation of migrations
target_metadata = Base.metadata

# Debug: Print detected tables
print(f"Detected tables: {list(target_metadata.tables.keys())}")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()