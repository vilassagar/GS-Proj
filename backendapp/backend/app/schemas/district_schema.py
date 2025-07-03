from typing import Optional
from app.schemas.base import CamelCaseModel
from app.schemas.block_schema import BlockAdminUserSchema  # Reuse existing

class DistrictAdminResponseSchema(CamelCaseModel):
    district_id: int
    district_name: str
    admin: Optional[BlockAdminUserSchema]


class DistrictAdminUpdateRequest(CamelCaseModel):
    district_id: int
    # user_id: int
    admin: BlockAdminUserSchema


class DistrictAdminUpdateResponse(CamelCaseModel):
    success: bool
    message: str
    admin_details: Optional[DistrictAdminResponseSchema]
