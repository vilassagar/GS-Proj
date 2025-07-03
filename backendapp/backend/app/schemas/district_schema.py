from typing import Optional

from pydantic import BaseModel
from app.schemas.block_schema import BlockAdminUserSchema  # Reuse existing


class DistrictAdminResponseSchema(BaseModel):
    district_id: int
    district_name: str
    admin: Optional[BlockAdminUserSchema]


class DistrictAdminUpdateRequest(BaseModel):
    district_id: int
    # user_id: int
    admin: BlockAdminUserSchema


class DistrictAdminUpdateResponse(BaseModel):
    success: bool
    message: str
    admin_details: Optional[DistrictAdminResponseSchema]
