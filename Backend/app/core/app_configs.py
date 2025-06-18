from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from app.core.http_errors import HttpErrors
from app.routers import file_search_poc
from app.routers.auth import auth_v1
from app.routers.blocks import blocks_v1
from app.routers.districts import districts_v1
from app.routers.gram_sevaks import gram_sevaks_v1
from app.routers.preset import preset_v1
from app.routers.users import users_v1
from app.core.api_checks_mw import ApiChecksMW
from app.core.core_exceptions import UnauthorizedException, InvalidRequestException, \
    NotFoundException, ConflictException, NotAcceptable
from app.routers.upload import upload_v1
from app.routers.government_docs import government_docs


# todo check whether we need API Support
# api_key_header = APIKeyHeader()


# todo check auth
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")


def create_app() -> FastAPI:
    '''
        For creating and configuring the FastAPI application
    '''

    app = FastAPI(
        title="GramSevak Seva",
        description="APIs for management",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origin_regex=None,
        expose_headers=["*"]
    )

    # Include routers with optional prefixes
    app.include_router(auth_v1.router)
    app.include_router(blocks_v1.router)
    app.include_router(districts_v1.router)
    app.include_router(gram_sevaks_v1.router)
    app.include_router(preset_v1.router)
    app.include_router(users_v1.router)
    app.include_router(upload_v1.router)
    app.include_router(government_docs.router)

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
