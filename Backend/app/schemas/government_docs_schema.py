from fastapi_camelcase import CamelModel
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class BookUploadSchema(CamelModel):
    subject: str = Field(..., description="Subject of the GR Upload")
    department_id: int = Field(..., description="Department ID", ge=1)

    # class Config:
    #     # orm_mode = True
    #     min_anystr_length = 1
    #     anystr_strip_whitespace = True


class GRUploadSchema(BookUploadSchema):
    gr_number: str = Field(..., description="GR Number")
    effective_date: date = Field(..., description="Date of the GR Upload")
    gr_code: str = Field(..., description="GR Code")
    yojana_id: int = Field(..., description="Yojana id")
