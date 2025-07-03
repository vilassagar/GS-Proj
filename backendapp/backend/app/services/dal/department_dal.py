from sqlalchemy.orm import Session
from typing_extensions import List

from app.models import Department
from app.services.dal.dto.department_dto import DepartmentDTO


class DepartmentDal:

    @staticmethod
    def get_departments_list(db: Session) -> List[DepartmentDTO]:
        query = db.query(Department).filter(Department.is_active)

        return [DepartmentDTO.to_dto(dept) for dept in query.all()]

    @staticmethod
    def get_department_by_id(db: Session, department_id: int):
        dept = db.query(Department).filter(Department.is_active, Department.id == department_id).first()

        return DepartmentDTO.to_dto(dept)
