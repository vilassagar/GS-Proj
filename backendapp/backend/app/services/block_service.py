from sqlalchemy.orm import Session
from typing import List, Optional
from app.services.dal.dto.user_dto import UserDTO
from app.services.dal.role_dal import RoleDal
from app.services.dal.user_dal import UserDal
from app.services.dal.user_hierarchy_dal import DistrictDal, BlockDal
from app.schemas.block_schema import BlockAdminResponseSchema, BlockAdminUpdateResponse, BlockAdminUserSchema
from app.core.core_exceptions import NotFoundException, InvalidRequestException


class BlockService:
    @staticmethod
    def get_block_admins(db: Session, search_term: Optional[str] = None) -> List[BlockAdminResponseSchema]:
        # Get Block Admin role
        block_admin_role = RoleDal.get_role_by_name(db, "blockAdmin")
        if not block_admin_role:
            raise NotFoundException("Block Admin role not configured")

        # Get blocks based on search term
        if search_term:
            blocks = BlockDal.get_blocks_by_search_term(db, search_term)
        else:
            blocks = BlockDal.get_all_active_blocks(db)

        result = []
        for block in blocks:
            # Get admins assigned to this specific block
            admins = UserDal.get_users_by_role_and_block(
                db=db,
                role_id=block_admin_role.id,
                block_id=block.block_id
            )

            result.append(BlockAdminResponseSchema(
                block_id=block.block_id,
                block_name=block.block_name,
                admin=BlockAdminUserSchema(
                    # **admins[0]
                    user_id=admins[0].id,
                    user_name=f"{admins[0].first_name} {admins[0].last_name}"
                ) if admins else None
            ))

        return result

    @staticmethod
    def update_block_admin(db: Session, block_id: int,
                           user_id: int, updated_by: int) -> BlockAdminUpdateResponse:
        # Checking if block exists
        block = BlockDal.get_block_by_id(db, block_id)

        print("In Update block admin service layer")

        if not block:
            raise NotFoundException(f"block with ID {block_id} not found")

        print("Block found")

        # Checking if user exists
        user = UserDal.get_user_by_id(db, user_id)
        if not user or not user.is_active:
            raise NotFoundException(f"Active user with ID {user_id} not found")

        print("User Found")

        # Checking if user belongs to provided block
        # Todo check whether we need below condition
        if user.block_id != block_id:
            raise InvalidRequestException(f"User {user_id} does not belong to {block_id}")

        print("User Found")

        UserDal.update_block_admin_to_gs(db=db, block_id=block_id)

        print("Curr block admin updated GS")

        # Updating the role for user to block admin
        updated_user = UserDal.update_user(
            db=db,
            user_id=user_id,
            update_dict={
                "role_id": 3,
                "block_id": block_id,
                "updated_by": updated_by
            }
        )

        return BlockAdminUpdateResponse(
            success=True,
            message="Block admin updated successfully",
            admin_details=BlockAdminResponseSchema(
                block_id=block.block_id,
                block_name=block.block_name,
                admin=BlockAdminUserSchema(
                    user_id=updated_user.id,
                    user_name=f"{updated_user.first_name} {updated_user.last_name}"
                )
            )
        )

