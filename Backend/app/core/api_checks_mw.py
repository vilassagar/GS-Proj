from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from app.core.core_exception import UnauthorizedException
from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.utils.jwt_utils import VxJWTUtils
from app.utils.vx_api_perms_utils import VxAPIPermsUtils

# Explicitly adding these two below paths to public
VxAPIPermsUtils.set_perm_get(path='/', perm=VxAPIPermsEnum.PUBLIC)
VxAPIPermsUtils.set_perm_get(path="/docs", perm=VxAPIPermsEnum.PUBLIC)
VxAPIPermsUtils.set_perm_get(path="/openapi.json", perm=VxAPIPermsEnum.PUBLIC)


class ApiChecksMW(BaseHTTPMiddleware):

    def __int__(self, app: ASGIApp):
        print("IN Middleware Initializing middleware")
        super().__init__(app)

    @staticmethod
    async def __read_jwt(request: Request):
        """
            Reading and verifying the JWT token from request header
            Returns user_id from the decoded token
        """

        try:
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer"):
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

        # Todo handle appr errors
        except ValueError as e:
            raise ValueError(str(e))
        except UnauthorizedException:
            raise Exception("Authorization failed")

    async def dispatch(self, request: Request, call_next):
        """
            This is an overridden method to define a custom logic to process incoming requests.
            i.e Middleware
        """
        method = request.method
        path = request.url.path

        print("In Middleware: ", method, path)

        if request.method == "OPTIONS":
            print("Calling Options method")
            return await call_next(request)

        try:
            print("Processing Middleware")

            if VxAPIPermsUtils.is_api_public(method=method, path=path):
                return await call_next(request)

            auth_header = request.headers.get("Authorization")

            if auth_header and not auth_header.startswith("Bearer "):
                raise UnauthorizedException("Invalid Token")

            print("Printing request: ", request.headers.get("Authorization"))

            # Todo refactor and optimize below
            # Validating JWT and getting user_id
            user_id = await ApiChecksMW.__read_jwt(request)
            request.state.user_id = user_id

            print("Request Received: ", request.state.user_id)

            response = await call_next(request)

            print("Response Recieved: ", response.__dict__)

            return response

        except UnauthorizedException:
            return HTTPException(401, "UnAuthorized Exception")

        # finally:
        #     db.close()

