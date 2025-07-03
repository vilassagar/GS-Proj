# app/schemas/gramsevak_schema.py
from typing import List

from fastapi import UploadFile
from pydantic import BaseModel

from app.models.enums.approval_status import ApprovalStatus


class GramsevakListItem(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    block: str
    service_id: str
    district: str
    is_approved: bool



class DesignationSchema(BaseModel):
    designation_id: int
    designation_name: str


class DistrictSchema(BaseModel):
    district_id: int
    district_name: str


class BlockSchema(BaseModel):
    block_id: int
    block_name: str


class GramPanchayatSchema(BaseModel):
    gram_panchayat_id: int
    gram_panchayat_name: str


class DocumentSchema(BaseModel):
    document_type: str
    document_name: str
    document_path: str


class GramsevakDetailResponse(BaseModel):
    first_name: str
    last_name: str
    designation: DesignationSchema
    district: DistrictSchema
    block: BlockSchema
    gram_panchayat: GramPanchayatSchema
    mobile_number: str
    whatsapp_number: str
    email: str
    documents: List[DocumentSchema]


class ChangeStatusRequest(BaseModel):
    gramsevak_id: int
    status: ApprovalStatus

class DocumentUploadRequest(BaseModel):
    documentTypeId: int
    document: UploadFile
    # document: File
