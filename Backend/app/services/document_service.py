# from typing import List, Dict

# from sqlalchemy.orm import Session
# from typing_extensions import List

# from app.services.dal.department_dal import DepartmentDal
# from app.services.dal.document_dal import DocumentTypeDal
# from app.services.dal.dto.department_dto import DepartmentDTO
# from app.services.dal.user_hierarchy_dal import DistrictDal, BlockDal, GramPanchayatDal
# from app.services.dal.dto.user_hierarchy_dto import (
#     DistrictDTO, BlockDTO, GramPanchayatDTO
# )

# class DocumentTypeService:
#     @staticmethod
#     def get_all_document_types(db: Session) -> list[dict[str, int | bool | str]]:
#         dts = DocumentTypeDal.get_all_document_types(db=db)

#         return [
#                 {
#                     "documentTypeId": dt.id,
#                     "documentTypeName": dt.name,
#                     "mendatory": dt.is_mandatory,
#                 } for dt in dts
#             ]

from typing import List, Dict, Union

from sqlalchemy.orm import Session

from app.services.dal.department_dal import DepartmentDal
from app.services.dal.document_dal import DocumentTypeDal
from app.services.dal.dto.department_dto import DepartmentDTO
from app.services.dal.user_hierarchy_dal import DistrictDal, BlockDal, GramPanchayatDal
from app.services.dal.dto.user_hierarchy_dto import (
    DistrictDTO, BlockDTO, GramPanchayatDTO
)

class DocumentTypeService:
    @staticmethod
    def get_all_document_types(db: Session) -> List[Dict[str, Union[int, bool, str]]]:
        dts = DocumentTypeDal.get_all_document_types(db=db)

        return [
                {
                    "documentTypeId": dt.id,
                    "documentTypeName": dt.name,
                    "mendatory": dt.is_mandatory,
                } for dt in dts
            ]
