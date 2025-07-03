from datetime import datetime
from typing import Optional
from app.models.roles import Role
from app.services.dal.dto.to_camel import ToCamel


class RoleDTO(ToCamel):
    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str],
        created_at: datetime,
        updated_at: Optional[datetime],
        is_active: bool
    ):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active

    @staticmethod
    def to_dto(role: Role) -> "RoleDTO":
        return RoleDTO(
            id=role.id,
            name=role.name,
            description=role.description,
            created_at=role.created_at,
            updated_at=role.updated_at,
            is_active=role.is_active,
        )
