from datetime import datetime
from typing import Optional
from app.models import Department  # Ensure to import the Department model
from app.services.dal.dto.to_camel import ToCamel


class DepartmentDTO(ToCamel):
    def __init__(
        self,
        id: int,
        name: str,
        # created_by: Optional[int],
        # updated_by: Optional[int],
        created_at: datetime,
        updated_at: Optional[datetime],
        is_active: bool
    ):
        self.department_id = id
        self.department_name = name
        self.id = id
        self.name = name
        # self.created_by = created_by
        # self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active

    @staticmethod
    def to_dto(department: Department) -> "DepartmentDTO":
        return DepartmentDTO(
            id=department.id,
            name=department.name,
            # created_by=department.created_by,
            # updated_by=department.updated_by,
            created_at=department.created_at,
            updated_at=department.updated_at,
            is_active=department.is_active
        )
