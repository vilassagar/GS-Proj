from sqlalchemy.orm import Session
from typing import List, Optional
from app.services.dal.dto.user_dto import UserDTO
from app.services.dal.role_dal import RoleDal
from app.services.dal.user_dal import UserDal
from app.services.dal.user_hierarchy_dal import DistrictDal
from app.schemas.district_schema import (
    DistrictAdminResponseSchema,
    DistrictAdminUpdateResponse
)
from app.schemas.block_schema import BlockAdminUserSchema  # <-- Add this import
from app.core.core_exceptions import NotFoundException, InvalidRequestException


class DistrictService:
    @staticmethod
    def get_district_admins(db: Session, search_term: Optional[str] = None) -> List[DistrictAdminResponseSchema]:
        '''
            Getting districts admins by search term for district name
        '''

        district_admin_role = RoleDal.get_role_by_name(db, "districtAdmin")
        if not district_admin_role:
            raise NotFoundException("District Admin role not configured")

        if search_term:
            districts = [district for district in DistrictDal.get_all_districts(db) if
                         search_term.lower() in district.district_name.lower()]
        else:
            districts = DistrictDal.get_all_districts(db)
        result = []

        for district in districts:
            admins = UserDal.get_users_by_role_and_district(
                db,
                role_id=district_admin_role.id,
                district_id=district.district_id
            )

            print(admins)

            result.append(DistrictAdminResponseSchema(
                district_id=district.district_id,
                district_name=district.district_name,
                admin=(
                    None if not admins else
                        BlockAdminUserSchema(  # <-- Fix: use the correct schema class
                            user_id=admins[0].id,
                            user_name=f"{admins[0].first_name} {admins[0].last_name}"
                        )
                )
            ))

        return result

    @staticmethod
    def update_district_admin(db: Session, district_id: int,
                              user_id: int, updated_by: int) -> DistrictAdminUpdateResponse:

        # Checking if requested district is available
        district = DistrictDal.get_district_by_id(db, district_id)
        if not district:
            raise NotFoundException(f"District {district_id} not found")

        # Checking if requested user is available
        user = UserDal.get_user_by_id(db, user_id)
        if not user or not user.is_active:
            raise NotFoundException(f"Active user {user_id} not found")

        if not user.district_id == district_id:
            raise InvalidRequestException(f"User {user_id} does not belong to the district {district_id}")

        # if not UserDal.is_user_in_role(db, user_id, "District_Admin"):
        #     raise InvalidRequestException("User must have District Admin role")

        UserDal.update_district_admin_to_gs(db=db, district_id=district_id)

        updated_user = UserDal.update_user(
            db=db,
            user_id=user_id,
            update_dict={
                "role_id": 2,
                "updated_by": updated_by
            }
        )

        return DistrictAdminUpdateResponse(
            success=True,
            message="District admin updated successfully",
            admin_details=DistrictAdminResponseSchema(
                district_id=district.district_id,
                district_name=district.district_name,
                admin=BlockAdminUserSchema(  # <-- Fix: use the correct schema class
                    user_id=updated_user.id,
                    user_name=f"{updated_user.first_name} {updated_user.last_name}"
                )
            )
        )
