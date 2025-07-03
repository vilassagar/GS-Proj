from sqlalchemy.orm import Session
from typing_extensions import List

from app.models import Department, Yojana
from app.services.dal.dto.department_dto import DepartmentDTO
from app.services.dal.dto.gr_yojana_dto import YojanaDTO


class DepartmentDal:

    @staticmethod
    def get_yojana_list(db: Session) -> List[DepartmentDTO]:
        query = db.query(Yojana).filter(Yojana.is_active)

        return [YojanaDTO.to_dto(yojana) for yojana in query.all()]

    @staticmethod
    def get_department_by_id(db: Session, department_id: int):
        dept = db.query(Department).filter(Department.is_active, Department.id == department_id).first()

        return DepartmentDTO.to_dto(dept)
