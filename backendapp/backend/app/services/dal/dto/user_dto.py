from datetime import datetime
from typing import Optional

from app.models.users import User
from app.services.dal.dto.roles_dto import RoleDTO
from app.services.dal.dto.to_camel import ToCamel
from app.services.dal.dto.user_hierarchy_dto import DistrictDTO, BlockDTO, GramPanchayatDTO


class UserDTO(ToCamel):
    def __init__(
            self,
            id: int,
            first_name: str,
            last_name: str,
            email: str,
            mobile_number: str,
            whatsapp_number: str,
            role_id: int,
            designation: str,
            district_id: Optional[int],
            block_id: Optional[int],
            gram_panchayat_id: Optional[int],
            status: str,
            created_at: Optional[datetime],
            updated_at: Optional[datetime],
            created_by: int,
            updated_by: int,
            is_active: bool,
            documents_uploaded: bool
    ):
        # User data
        self.id = id
        self.user_id = id
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = first_name + " " + last_name
        self.email = email
        self.mobile_number = mobile_number
        self.whatsapp_number = whatsapp_number
        self.role_id = role_id
        self.designation = designation
        self.district_id = district_id
        self.block_id = block_id
        self.gram_panchayat_id = gram_panchayat_id
        self.status = status

        # TimestampMixin cols
        self.created_at = created_at
        self.updated_at = updated_at
        self.created_by = created_by
        self.updated_by = updated_by
        self.is_active = is_active
        self.documents_uploaded = documents_uploaded

    @staticmethod
    def to_dto(user: User) -> "UserDTO":
        return UserDTO(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            mobile_number=user.mobile_number,
            whatsapp_number=user.whatsapp_number,
            role_id=user.role_id,
            designation=user.designation,
            district_id=user.district_id,
            block_id=user.block_id,
            gram_panchayat_id=user.gram_panchayat_id,
            status=user.status,
            created_at=user.created_at,
            updated_at=user.updated_at,
            created_by=user.created_by,
            updated_by=user.updated_by,
            is_active=user.is_active,
            documents_uploaded=user.documents_uploaded
        )


class UserWithDetailsDTO(UserDTO):
    def __init__(
            self,
            id: int,
            first_name: str,
            last_name: str,
            email: str,
            mobile_number: str,
            whatsapp_number: str,
            role_id: int,
            role: Optional[RoleDTO],
            designation: str,
            district_id: Optional[int],
            district: Optional[DistrictDTO],
            block_id: Optional[int],
            block: Optional[BlockDTO],
            gram_panchayat_id: Optional[int],
            gram_panchayat: Optional[GramPanchayatDTO],
            status: str,
            created_at: Optional[datetime],
            updated_at: Optional[datetime],
            created_by: int,
            updated_by: int,
            is_active: bool,
            documents_uploaded: bool
    ):
        super().__init__(
            id=id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile_number=mobile_number,
            whatsapp_number=whatsapp_number,
            role_id=role_id,
            designation=designation,
            district_id=district_id,
            block_id=block_id,
            gram_panchayat_id=gram_panchayat_id,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            updated_by=updated_by,
            is_active=is_active,
            documents_uploaded=documents_uploaded
        )

        # Additional fields specific to UserWithDetailsDTO
        self.role = role
        self.district = district
        self.block = block
        self.gram_panchayat = gram_panchayat

    @staticmethod
    def to_detailed_dto(user: User) -> "UserWithDetailsDTO":
        return UserWithDetailsDTO(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            mobile_number=user.mobile_number,
            whatsapp_number=user.whatsapp_number,
            role_id=user.role_id,
            role=RoleDTO.to_dto(user.role),
            designation=user.designation,
            district_id=user.district_id,
            district=DistrictDTO.to_dto(user.district),
            block_id=user.block_id,
            block=BlockDTO.to_dto(user.block),
            gram_panchayat_id=user.gram_panchayat_id,
            gram_panchayat=GramPanchayatDTO.to_dto(user.gram_panchayat),
            status=user.status,
            created_at=user.created_at,
            updated_at=user.updated_at,
            created_by=user.created_by,
            updated_by=user.updated_by,
            is_active=user.is_active,
            documents_uploaded=user.documents_uploaded
        )
