from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from pydantic.utils import to_camel

from app.config import get_db

from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.services.dal.dto.user_hierarchy_dto import DistrictDTO, BlockDTO, GramPanchayatDTO
from app.services.dal.user_hierarchy_dal import GramPanchayatDal, BlockDal, DistrictDal
from app.services.preset_services import PresetService
from app.utils.vx_api_perms_utils import VxAPIPermsUtils
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix="/v1/preset",
    tags=["preset"],
    responses={404: {"description": "Not Found"}}
)

VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getDistricts', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getDistricts"
            # ,response_model=List[DistrictDTO]
            )
async def get_districts(db: Session = Depends(get_db)):
    """Get all active districts"""
    districts = PresetService.get_all_districts(db)

    print("In District router: ", districts)

    return [dist.to_camel() for dist in districts]
    # return [
    #     {'districtId': district.district_id,
    #      'districtName': district.district_name
    #      } for district in districts
    # ]


VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getBlocksByDictrictId', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getBlocksByDictrictId"
            # , response_model=List[BlockDTO]
            )
async def get_blocks_by_district(
        districtId: int = Query(..., alias="districtId"),
        db: Session = Depends(get_db)
):
    """Get blocks by district ID"""
    blocks = PresetService.get_blocks_by_district(db, districtId)
    return [block.to_camel() for block in blocks]


VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getGramPanchayatsByBlockId', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getGramPanchayatsByBlockId"
            # , response_model=List[GramPanchayatDTO]
            )
async def get_gram_panchayats_by_block(
        blockId: int = Query(..., alias="blockId"),
        db: Session = Depends(get_db)
):
    """Get gram panchayats by block ID"""
    gps = PresetService.get_gram_panchayats_by_block(db, blockId)
    return [gp.to_camel() for gp in gps]


VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getDepartments', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getDepartments"
            # , response_model=List[GramPanchayatDTO]
            )
async def get_departments(
        db: Session = Depends(get_db)
):
    """Get gram panchayats by block ID"""
    # gps = PresetService.get_gram_panchayats_by_block(db, blockId)
    # return gps
    # department_dtos = [DepartmentDTO.from_orm(dept) for dept in departments]

    return [dept.to_camel() for dept in PresetService.get_departments(db=db)]


VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getYojanas', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getYojanas"
            # , response_model=List[GramPanchayatDTO]
            )
async def get_yojanas(
        db: Session = Depends(get_db)
):
    return [yoj.to_camel() for yoj in PresetService.get_yojanas(db=db)]
