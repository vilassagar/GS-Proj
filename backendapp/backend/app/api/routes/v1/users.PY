from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_db
from app.services.user_service import UserService

from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.utils.vx_api_perms_utils import VxAPIPermsUtils

router = APIRouter(
    prefix="/v1/user",
    tags=["user"],
    responses={404: {"description": "Not Found"}}
)


VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getUsersByBlockID', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getUsersByBlockID")
def get_users_by_block_id(blockId: int, db: Session = Depends(get_db)):
    """
    Get all users associated with a given block ID.
    """
    users = UserService.get_users_by_block_id(block_id=blockId, db=db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found for this block id")
    return [user.to_camel() for user in users if user.role_id == 4]


VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getUsersByDistrictID', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getUsersByDistrictID")
def get_users_by_district_id(districtId: int, db: Session = Depends(get_db)):
    """
    Get all users associated with a given district ID.
    """
    users = UserService.get_users_by_district_id(districtId, db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found for this district id")
    return [user.to_camel() for user in users if user.role_id == 4]
