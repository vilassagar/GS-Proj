from app.core.core_exceptions import CommonException
from fastapi.responses import JSONResponse
from fastapi import status


class HttpErrors:

    @staticmethod
    async def http_400(e: CommonException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": e.message}
        )

    @staticmethod
    async def http_401(e: CommonException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": e.message}
        )

    @staticmethod
    async def http_403(e: CommonException):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": e.message}
        )

    @staticmethod
    async def http_404(e: CommonException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": e.message}
        )

    @staticmethod
    async def http_406(e: CommonException):
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={"message": e.message}
        )

    @staticmethod
    async def http_409(e: CommonException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": e.message}
        )
