from datetime import date, datetime
from typing import Optional
from app.models.gr_yojana import Yojana, GR
from app.services.dal.dto.to_camel import ToCamel


class YojanaDTO(ToCamel):
    def __init__(
        self,
        id: int,
        name: str,
        # created_by: Optional[int],
        # updated_by: Optional[int],
        # yojana_name: str,
        created_at: datetime,
        updated_at: Optional[datetime],
        is_active: bool
    ):
        self.yojana_id = id
        self.yojana_name = name
        # self.id = id
        # self.name = name
        # self.created_by = created_by
        # self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active

    @staticmethod
    def to_dto(yojana: Yojana) -> "YojanaDTO":
        return YojanaDTO(
            id=yojana.id,
            name=yojana.name,
            # created_by=yojana.created_by,
            # updated_by=yojana.updated_by,
            created_at=yojana.created_at,
            updated_at=yojana.updated_at,
            is_active=yojana.is_active
        )


class GRDTO(ToCamel):
    def __init__(
        self,
        id: int,
        gr_number: str,
        gr_code: Optional[str],
        subject: str,
        department_name: str,
        effective_date: date,
        yojana_id: int,
        file_path: str,
        created_by: Optional[int],
        updated_by: Optional[int],
        created_at: datetime,
        updated_at: Optional[datetime],
        is_active: bool
    ):
        self.id = id
        self.gr_number = gr_number
        self.gr_code = gr_code
        self.subject = subject
        self.department_name = department_name
        self.effective_date = effective_date
        self.yojana_id = yojana_id
        # self.yojana_name = yojana_name
        self.file_path = file_path
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active

    @staticmethod
    def to_dto(gr: GR) -> "GRDTO":
        return GRDTO(
            id=gr.id,
            gr_number=gr.gr_number,
            gr_code=gr.gr_code,
            subject=gr.subject,
            department_name=gr.department,
            effective_date=gr.effective_date,
            yojana_id=gr.yojana_id,
            # yojana_name=gr.yojana.name,
            file_path=gr.file_path,
            created_by=gr.created_by,
            updated_by=gr.updated_by,
            created_at=gr.created_at,
            updated_at=gr.updated_at,
            is_active=gr.is_active
        )