## app/core/app_factory.py

from fastapi import FastAPI, Request
#Rate Limiter Middelware 
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
#end of rate_limit 
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

from fastapi_cache2 import FastAPICache
from fastapi_cache2.backends.redis import RedisBackend
import redis.asyncio as redis

from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
from app.core.http_errors import HttpErrors
from app.core.api_checks_mw import ApiChecksMW
from app.core.core_exceptions import UnauthorizedException, InvalidRequestException, \
    NotFoundException, ConflictException, NotAcceptable

# Import routers
from app.api.routes.v1 import auth, blocks, districts, gram_sevaks
from app.api.routes.v1 import  preset, profile, document_status, government_docs
from app.api.routes.v1 import upload,document_validation,enhanced_profile
# Try to import additional routers with error handling
import importlib

try:
    users_module = importlib.import_module("app.api.routes.v1.users")
    users_available = True
except ImportError as e:
    print(f"Warning: Could not import users router: {e}")
    users_available = False

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

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log incoming request
        logger.info(f"➡️ {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        process_time = round((time.time() - start_time) * 1000, 2)
        
        # Log response status and duration
        logger.info(f"⬅️ {request.method} {request.url.path} - {response.status_code} ({process_time} ms)")
        
        return response

def create_app() -> FastAPI:
    app = FastAPI(
        title="GramSevak Seva API",
        description="APIs for GramSevak management with JWT authentication and document status tracking",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    # Initialize Limiter
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_middleware(LoggingMiddleware)
    # Add exception handler
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
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

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origin_regex=None,
        expose_headers=["*"]
    )

    # Include routers
    app.include_router(auth.router)
    app.include_router(blocks.router)
    app.include_router(districts.router)
    app.include_router(gram_sevaks.router)
    app.include_router(preset.router)
    app.include_router(profile.router)
    app.include_router(document_status.router)
    app.include_router(government_docs.router)
    app.include_router(upload.router)
    app.include_router(document_validation.router)
    app.include_router(enhanced_profile.router)

    # Include users router if available
    if users_available:
        app.include_router(users_module.router)

    # Add API checks middleware after CORS middleware
    app.add_middleware(ApiChecksMW)

    # Exception handlers
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