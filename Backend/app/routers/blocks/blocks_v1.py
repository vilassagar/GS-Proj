from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.config import get_db
from app.core.core_exceptions import InvalidRequestException
from app.services.block_service import BlockService
from app.schemas.block_schema import BlockAdminResponseSchema, BlockAdminUpdateResponse, BlockAdminUpdateRequest
from app.services.dal.dto.user_dto import UserDTO
from app.utils.vx_api_perms_utils import VxAPIPermsUtils, VxAPIPermsEnum
from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/v1/block",
    tags=["blocks"],
    responses={404: {"description": "Not Found"}}
)

# VxAPIPermsUtils.set_perm_get(path=router.prefix + '/get-block-admins', perm=VxAPIPermsEnum.ADMIN_READ)
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getBlockAdmins', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getBlockAdmins", response_model=List[BlockAdminResponseSchema],
            summary="Get block admins by district",
            description="Returns list of districts with their block admins")
async def get_block_admins(db: Session = Depends(get_db),
                           searcTerm=Query(default=None, description="Searching by block name")
                           # requesting_user: UserDTO = Depends(get_current_user)
                           ):
    # Todo check requirements who can call?

    # if requesting_user.role_id not in (1, 2):
    #     raise InvalidRequestException("Requesting User not authorized")

    return BlockService.get_block_admins(db, search_term=searcTerm)


# Todo make this perm and then we can remove the is_admin check `ADMIN_WRITE`
VxAPIPermsUtils.set_perm_post(path=router.prefix + '/updateBlockAdmin', perm=VxAPIPermsEnum.AUTHENTICATED)
# VxAPIPermsUtils.set_perm_post(path=router.prefix + '/updateblockadmin', perm=VxAPIPermsEnum.PUBLIC)
@router.post("/updateBlockAdmin", response_model=BlockAdminUpdateResponse,
             summary="Update block admin for district",
             description="Assign/update block admin for a specific district")
async def update_block_admin(
        update_data: BlockAdminUpdateRequest,
        db: Session = Depends(get_db),
        requesting_user: UserDTO = Depends(get_current_user)
):
    '''
        Router to assign a new block admin to provided block.
    '''
    # if requesting_user.role_id not in (1, 2):
    #     raise InvalidRequestException("Requesting User not authorized")

    print("In Router: ", update_data.__dict__)
    # print("In Router: ", update_data.block_id, update_data.user_id)

    return BlockService.update_block_admin(
        db=db,
        block_id=update_data.block_id,
        user_id=update_data.admin.user_id,
        # updated_by=1
        updated_by=requesting_user.user_id
    )
