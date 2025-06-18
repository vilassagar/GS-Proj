from sqlalchemy.orm import Session
from typing_extensions import List

from app.services.dal.department_dal import DepartmentDal
from app.services.dal.dto.department_dto import DepartmentDTO
from app.services.dal.dto.gr_yojana_dto import YojanaDTO
from app.services.dal.gr_dal import YojanaDal
from app.services.dal.user_hierarchy_dal import DistrictDal, BlockDal, GramPanchayatDal
from app.services.dal.dto.user_hierarchy_dto import (
    DistrictDTO, BlockDTO, GramPanchayatDTO
)

class PresetService:
    @staticmethod
    def get_all_districts(db: Session) -> list[DistrictDTO]:
        return DistrictDal.get_all_districts(db)

    @staticmethod
    def get_blocks_by_district(db: Session, district_id: int) -> list[BlockDTO]:
        return BlockDal.get_blocks_by_district(db, district_id)

    @staticmethod
    def get_gram_panchayats_by_block(db: Session, block_id: int) -> list[GramPanchayatDTO]:
        return GramPanchayatDal.get_gp_by_block(db, block_id)

    @staticmethod
    def get_departments(db) -> List[DepartmentDTO]:
        return DepartmentDal.get_departments_list(db=db)

    @staticmethod
    def get_yojanas(db) -> List[YojanaDTO]:
        return YojanaDal.get_all_yojanas(db=db)
