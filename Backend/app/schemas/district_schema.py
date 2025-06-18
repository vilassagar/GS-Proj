from typing import Optional

from pydantic import BaseModel
from app.schemas.block_schema import BlockAdminUserSchema  # Reuse existing
from app.schemas.base import CamelModel


class DistrictAdminResponseSchema(CamelModel):
    district_id: int
    district_name: str
    admin: Optional[BlockAdminUserSchema]


class DistrictAdminUpdateRequest(CamelModel):
    district_id: int
    # user_id: int
    admin: BlockAdminUserSchema


class DistrictAdminUpdateResponse(CamelModel):
    success: bool
    message: str
    admin_details: Optional[DistrictAdminResponseSchema]
