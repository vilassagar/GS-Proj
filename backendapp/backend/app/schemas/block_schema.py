from pydantic import BaseModel
from typing_extensions import List
from typing import Optional
from app.schemas.base import CamelCaseModel



class BlockBaseSchema(CamelCaseModel):
    block_id: int
    block_name: str


class BlockAdminUserSchema(CamelCaseModel):
    user_id: int
    user_name: str


class BlockAdminResponseSchema(BlockBaseSchema):
    admin: Optional[BlockAdminUserSchema]

   


class BlockAdminUpdateRequest(CamelCaseModel):
    block_id: int
    # user_id: int
    admin: BlockAdminUserSchema

    model_config = {"extra": "allow"}


class BlockAdminUpdateResponse(CamelCaseModel):
    success: bool
    message: str
    admin_details: BlockAdminResponseSchema

