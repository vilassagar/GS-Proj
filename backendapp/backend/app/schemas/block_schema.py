from pydantic import BaseModel
from typing_extensions import List
from typing import Optional




class BlockBaseSchema(BaseModel):
    block_id: int
    block_name: str


class BlockAdminUserSchema(BaseModel):
    user_id: int
    user_name: str


class BlockAdminResponseSchema(BlockBaseSchema):
    admin: Optional[BlockAdminUserSchema]

   


class BlockAdminUpdateRequest(BaseModel):
    block_id: int
    # user_id: int
    admin: BlockAdminUserSchema

    model_config = {"extra": "allow"}


class BlockAdminUpdateResponse(BaseModel):
    success: bool
    message: str
    admin_details: BlockAdminResponseSchema

