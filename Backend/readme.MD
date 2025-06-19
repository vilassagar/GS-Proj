Setup Instructions
To run your application, follow these steps:
1. Create a Virtual Environment

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

2. Install Dependencies
pip install -r requirements.txt

3. Environment Setup

Edit the .env file with your actual configuration values:

Database: Set up your PostgreSQL database connection
Twilio: Add your Twilio credentials for SMS functionality
JWT: Generate a secure secret key
AWS: Add your AWS credentials for S3 file storage

4. Database Setup
# Initialize Alembic (if not already done)
alembic init alembic

# Run database migrations
alembic upgrade head

5. Run the Application
# Development server
python app/main.py

# Or using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload


Key Dependencies Explained:

FastAPI: Web framework for building APIs
SQLAlchemy: ORM for database operations
Alembic: Database migration tool
Pydantic: Data validation and settings management
PyJWT: JWT token handling for authentication
Twilio: SMS service for OTP functionality
Boto3: AWS SDK for S3 file storage
Aiofiles: Async file operations
Python-dotenv: Environment variable management

Important Notes:

Database: Your app uses PostgreSQL. Make sure you have it installed and running.
Environment Variables: All sensitive configuration is loaded from the .env file. Never commit this file to version control.
File Storage: The app uses AWS S3 for file storage. Make sure your AWS credentials are properly configured.
SMS Service: Twilio is used for sending OTP messages. You'll need a Twilio account.
CORS: The app is configured to allow requests from http://localhost:5173 (likely your frontend).

