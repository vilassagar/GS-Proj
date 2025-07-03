from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import get_db
from app.services.dal.user_dal import UserDal
from app.services.dal.dto.user_dto import UserDTO


# Note for using below function as a dependency injection the router must be set to Authenticated Permissions.
async def get_current_user(
        request: Request,
        db: Session = Depends(get_db)
) -> UserDTO:
    """
    Dependency to get current authenticated user from JWT token
    Requires the middleware to have set request.state.user_id
    """
    # Get user_id from request state set by middleware
    # user_id = getattr(request.state, "user_id", None)

    user_id = request.state.user_id

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    user = UserDal.get_user_by_id(db, user_id=user_id)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or inactive"
        )

    return user