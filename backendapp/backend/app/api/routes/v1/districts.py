from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.config import get_db
from app.core.core_exceptions import InvalidRequestException
from app.services.dal.dto.user_dto import UserDTO
from app.services.district_service import DistrictService
from app.schemas.district_schema import (
    DistrictAdminResponseSchema,
    DistrictAdminUpdateResponse,
    DistrictAdminUpdateRequest
)
from app.utils.vx_api_perms_utils import VxAPIPermsUtils, VxAPIPermsEnum
from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/v1/district",
    tags=["districts"],
    responses={404: {"description": "Not Found"}}
)


# VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getdistrictadmins', perm=VxAPIPermsEnum.AUTHENTICATED)
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getdistrictadmins', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getdistrictadmins", response_model=List[DistrictAdminResponseSchema],
            summary="Get district admins",
            description="Returns list of districts with their admins")
async def get_district_admins(db: Session = Depends(get_db),
                              searcTerm=Query(default=None, description="Searching by district name")
                              # As discussed with Avdhoot removing the validation for requesting user
                              # requesting_user: UserDTO = Depends(get_current_user)
                              ):
    # if requesting_user.role_id not in (1,):  # Only super admin
    #     raise InvalidRequestException("Requesting User not authorized")
    return DistrictService.get_district_admins(db, search_term=searcTerm)


# VxAPIPermsUtils.set_perm_post(path=router.prefix + '/updatedistrictadmin', perm=VxAPIPermsEnum.ADMIN_WRITE)
# VxAPIPermsUtils.set_perm_post(path=router.prefix + '/updatedistrictadmin', perm=VxAPIPermsEnum.AUTHENTICATED)
VxAPIPermsUtils.set_perm_post(path=router.prefix + '/updateDistrictAdmin', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.post("/updateDistrictAdmin", response_model=DistrictAdminUpdateResponse,
             summary="Update district admin",
             description="Assign/update district admin for a specific district")
async def update_district_admin(
        # Todo check this
        update_data: DistrictAdminUpdateRequest,
        db: Session = Depends(get_db),
        # As discussed with Avdhoot removing the validation for requesting user
        requesting_user: UserDTO = Depends(get_current_user)
):
    # if requesting_user.role_id not in (1,):  # Only super admin
    #     raise InvalidRequestException("Requesting User not authorized")

    # print("Printing in Update district data: ", update_data.district_id, update_data.user_id, requesting_user)

    return DistrictService.update_district_admin(
        db=db,
        district_id=update_data.district_id,
        user_id=update_data.admin.user_id,
        updated_by=requesting_user.id
        # updated_by=1
    )
