from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp
from starlette.responses import JSONResponse

from app.core.core_exceptions import UnauthorizedException
from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.utils.jwt_utils import VxJWTUtils
from app.utils.vx_api_perms_utils import VxAPIPermsUtils

# Explicitly adding these paths to public
VxAPIPermsUtils.set_perm_get(path='/', perm=VxAPIPermsEnum.PUBLIC)
VxAPIPermsUtils.set_perm_get(path="/docs", perm=VxAPIPermsEnum.PUBLIC)
VxAPIPermsUtils.set_perm_get(path="/openapi.json", perm=VxAPIPermsEnum.PUBLIC)
VxAPIPermsUtils.set_perm_get(path="/.well-known/gpc.json", perm=VxAPIPermsEnum.PUBLIC)
VxAPIPermsUtils.set_perm_get(path="/favicon.ico", perm=VxAPIPermsEnum.PUBLIC)


class ApiChecksMW(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp):
        print("Initializing middleware")
        super().__init__(app)

    @staticmethod
    async def __read_jwt(request: Request):
        """
            Reading and verifying the JWT token from request header
            Returns user_id from the decoded token
        """

        try:
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                raise ValueError("Invalid Auth Header")

            # Getting the part after Bearer
            token = auth_header.split(" ")[1]

            print("Token: ", token)

            payload = await VxJWTUtils.verify_access_token(token=token)

            # Getting subject. Normally its User_id
            sub = int(payload.get("user_id"))

            print("Printing Sub: ", sub)

            if not sub:
                raise UnauthorizedException("Token is missing Subject claims. i.e user_id")
            return sub

        except ValueError as e:
            raise ValueError(str(e))
        except UnauthorizedException:
            raise UnauthorizedException("Authorization failed")
        except Exception as e:
            print(f"Unexpected error in JWT processing: {e}")
            raise UnauthorizedException("Token processing failed")

    async def dispatch(self, request: Request, call_next):
        """
            This is an overridden method to define a custom logic to process incoming requests.
            i.e Middleware
        """
        method = request.method
        path = request.url.path

        print("In Middleware: ", method, path)

        # Handle OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            print("Calling Options method")
            return await call_next(request)

        try:
            print("Processing Middleware")

            # Check if API is public
            if VxAPIPermsUtils.is_api_public(method=method, path=path):
                print(f"Public API: {method} {path}")
                return await call_next(request)

            # Check for authentication header
            auth_header = request.headers.get("Authorization")
            print("Printing request auth header: ", auth_header)

            # If no auth header for protected route, return 401
            if not auth_header:
                print("No Authorization header found for protected route")
                return JSONResponse(
                    status_code=401,
                    content={"message": "Authorization header required"}
                )

            # Validate auth header format
            if not auth_header.startswith("Bearer "):
                print("Invalid Authorization header format")
                return JSONResponse(
                    status_code=401,
                    content={"message": "Invalid Authorization header format"}
                )

            # Validate JWT and get user_id
            user_id = await ApiChecksMW.__read_jwt(request)
            request.state.user_id = user_id

            print("Request Received with user_id: ", request.state.user_id)

            response = await call_next(request)

            print("Response Received: ", response.status_code)

            return response

        except ValueError as e:
            print(f"ValueError in middleware: {e}")
            return JSONResponse(
                status_code=401,
                content={"message": "Invalid authorization token"}
            )
        except UnauthorizedException as e:
            print(f"UnauthorizedException in middleware: {e}")
            return JSONResponse(
                status_code=401,
                content={"message": "Unauthorized"}
            )
        except Exception as e:
            print(f"Unexpected error in middleware: {e}")
            return JSONResponse(
                status_code=500,
                content={"message": "Internal server error"}
            )