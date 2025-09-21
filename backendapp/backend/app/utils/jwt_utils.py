from copy import deepcopy
from datetime import timedelta, datetime, timezone

import jwt
from app.config import settings
from app.core.core_exceptions import UnauthorizedException

# JWT secret key and algorithm
JWT_SECRET = settings.jwt_secret_key
JWT_ALGO = settings.jwt_algorithm

class JWTError(Exception):
    """Custom JWT Error that properly inherits from Exception"""
    pass

class VxJWTUtils:

    @staticmethod
    def create_access_token(data: dict, expiry_delta: int = None) -> str:
        """
            Function to create a JWT token
        """

        to_encode = deepcopy(data)

        if expiry_delta:
            expiry_in = datetime.now(timezone.utc) + timedelta(minutes=expiry_delta)
        else:
            expiry_in = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expiry)

        print("Creating access token", expiry_in)
        print("Creating access token", expiry_in.isoformat())

        to_encode.update({"exp": expiry_in})  

        encoded_jwt = jwt.encode(payload=to_encode, key=JWT_SECRET, algorithm=JWT_ALGO)
        return encoded_jwt

    @staticmethod
    async def verify_access_token(token: str) -> dict:
        """
            Verifying JWT token and returning payload
        """

        try:
            print("\n In Verify access token: \n")
            print("\n In Verify access token: \n")
            payload = jwt.decode(jwt=token, key=JWT_SECRET, algorithms=[JWT_ALGO])
            return payload
        except jwt.ExpiredSignatureError:
            raise UnauthorizedException("JWT Token has expired")
        except jwt.DecodeError:
            raise UnauthorizedException("Invalid or Malformed token")
        except jwt.InvalidTokenError:
            raise UnauthorizedException("Invalid or Malformed token")
        except Exception as e:
            print(f"Unexpected JWT error: {e}")
            raise UnauthorizedException("Token verification failed")