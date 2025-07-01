# app/core/app_configs.py - Updated to include document status router
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi

from app.core.http_errors import HttpErrors
from app.routers import file_search_poc
from app.routers.auth import auth_v1
from app.routers.blocks import blocks_v1
from app.routers.districts import districts_v1
from app.routers.gram_sevaks import gram_sevaks_v1
from app.routers.preset import preset_v1
from app.routers.users import users_v1
from app.routers.profile import profile_v1
from app.core.api_checks_mw import ApiChecksMW
from app.core.core_exceptions import UnauthorizedException, InvalidRequestException, \
    NotFoundException, ConflictException, NotAcceptable
from app.routers.upload import upload_v1
from app.routers.government_docs import government_docs
from app.routers.dynamic_documents import dynamic_documents_v1

# Import the new document status router
try:
    from app.routers.document_status import document_status_v1
    DOCUMENT_STATUS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import document status router: {e}")
    DOCUMENT_STATUS_AVAILABLE = False

# OAuth2 scheme for Swagger UI
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/v1/auth/login",
    description="JWT token authentication"
)

# Bearer token scheme
bearer_scheme = HTTPBearer(
    scheme_name="Bearer Token",
    description="Enter your JWT token"
)

def create_app() -> FastAPI:
    """
    For creating and configuring the FastAPI application
    """

    app = FastAPI(
        title="GramSevak Seva API",
        description="APIs for GramSevak management with JWT authentication and document status tracking",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Custom OpenAPI schema with security
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        openapi_schema = get_openapi(
            title="GramSevak Seva API",
            version="1.0.0",
            description="APIs for GramSevak management with document upload progress tracking",
            routes=app.routes,
        )
        
        # Add security schemes
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter your JWT token"
            },
            "OAuth2PasswordBearer": {
                "type": "oauth2",
                "flows": {
                    "password": {
                        "tokenUrl": "/v1/auth/login",
                        "scopes": {}
                    }
                }
            }
        }
        
        # Apply security to all protected routes
        for path, path_item in openapi_schema["paths"].items():
            for method, operation in path_item.items():
                if method.lower() in ["get", "post", "put", "patch", "delete"]:
                    # Skip public endpoints
                    if any(tag in operation.get("tags", []) for tag in ["auth"]) and "login" in path:
                        continue
                    if any(tag in operation.get("tags", []) for tag in ["auth"]) and "sendOtp" in path:
                        continue
                    
                    # Add security to protected endpoints
                    operation["security"] = [{"BearerAuth": []}]
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origin_regex=None,
        expose_headers=["*"]
    )

    # Include existing routers
    app.include_router(auth_v1.router)
    app.include_router(blocks_v1.router)
    app.include_router(districts_v1.router)
    app.include_router(gram_sevaks_v1.router)
    app.include_router(preset_v1.router)
    app.include_router(users_v1.router)
    app.include_router(profile_v1.router)
    app.include_router(upload_v1.router)
    app.include_router(government_docs.router)
    app.include_router(dynamic_documents_v1.router)
    
    # Include the new document status router
    if DOCUMENT_STATUS_AVAILABLE:
        app.include_router(document_status_v1.router)
        print("✅ Document status router loaded successfully")
    else:
        print("⚠️  Document status router not available - some features may be limited")

    # Add API checks middleware after CORS middleware
    app.add_middleware(ApiChecksMW)

    @app.exception_handler(InvalidRequestException)
    async def invalid_exception_handler(request: Request, e: InvalidRequestException):
        return await HttpErrors.http_400(e)

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_exception_handler(request: Request, e: UnauthorizedException):
        return await HttpErrors.http_401(e)

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, e: NotFoundException):
        return await HttpErrors.http_404(e)

    @app.exception_handler(NotAcceptable)
    async def not_acceptable_exception_handler(request: Request, e: NotAcceptable):
        return await HttpErrors.http_406(e)

    @app.exception_handler(ConflictException)
    async def conflict_exception_handler(request: Request, e: ConflictException):
        return await HttpErrors.http_409(e)

    return app

# Add this file: app/routers/document_status/__init__.py
"""
# app/routers/document_status/__init__.py
Document status tracking router package
"""

# Create the router file structure:
# app/
#   routers/
#     document_status/
#       __init__.py
#       document_status_v1.py  # The router code I provided earlier