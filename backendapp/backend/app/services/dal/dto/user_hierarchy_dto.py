from datetime import datetime
from typing import Optional
from app.models.users_hierarchy import District, Block, GramPanchayat
from app.services.dal.dto.to_camel import ToCamel


class DistrictDTO(ToCamel):
    def __init__(
            self,
            id: int,
            name: str,
            created_at: datetime,
            updated_at: Optional[datetime],
            is_active: bool,
            # created_by: Optional[int],
            # updated_by: Optional[int]
    ):
        self.district_id = id
        self.district_name = name
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
        # self.created_by = created_by
        # self.updated_by = updated_by

    @staticmethod
    def to_dto(district: District) -> "DistrictDTO":
        return DistrictDTO(
            id=district.id,
            name=district.name,
            created_at=district.created_at,
            updated_at=district.updated_at,
            is_active=district.is_active,
            # created_by=district.created_by,
            # updated_by=district.updated_by
        )


class BlockDTO(ToCamel):
    def __init__(
            self,
            id: int,
            name: str,
            district_id: int,
            created_at: datetime,
            updated_at: Optional[datetime],
            is_active: bool,
            # created_by: Optional[int],
            # updated_by: Optional[int]
    ):
        self.block_id = id
        self.block_name = name
        self.district_id = district_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
        # self.created_by = created_by
        # self.updated_by = updated_by

    @staticmethod
    def to_dto(block: Block) -> "BlockDTO":
        return BlockDTO(
            id=block.id,
            name=block.name,
            district_id=block.district_id,
            created_at=block.created_at,
            updated_at=block.updated_at,
            is_active=block.is_active,
            # created_by=block.created_by,
            # updated_by=block.updated_by
        )


class GramPanchayatDTO(ToCamel):
    def __init__(
            self,
            id: int,
            name: str,
            block_id: int,
            created_at: datetime,
            updated_at: Optional[datetime],
            is_active: bool,
            # created_by: Optional[int],
            # updated_by: Optional[int]
    ):
        self.gram_panchayat_id = id
        self.gram_panchayat_name = name
        self.block_id = block_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
        # self.created_by = created_by
        # self.updated_by = updated_by

    @staticmethod
    def to_dto(gp: GramPanchayat) -> "GramPanchayatDTO":
        return GramPanchayatDTO(
            id=gp.id,
            name=gp.name,
            block_id=gp.block_id,
            created_at=gp.created_at,
            updated_at=gp.updated_at,
            is_active=gp.is_active,
            # created_by=gp.created_by,
            # updated_by=gp.updated_by
        )
