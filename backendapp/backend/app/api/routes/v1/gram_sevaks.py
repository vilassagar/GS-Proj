from typing import Optional
import re

from fastapi import APIRouter, Depends, Query, status, Request
from sqlalchemy.orm import Session

from app.config import get_db
from app.core.core_exceptions import InvalidRequestException
from app.dependencies.auth import get_current_user
from app.models.enums.approval_status import ApprovalStatusRequest
from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.schemas.gramsevak_schema import (
    ChangeStatusRequest
)
from app.services.dal.dto.user_dto import UserDTO
from app.services.gramsevak_service import GramsevakService
from app.utils.vx_api_perms_utils import VxAPIPermsUtils

router = APIRouter(
    prefix="/v1/gramsevak",
    tags=["gramsevak"],
    responses={404: {"description": "Not Found"}}
)


VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getGramsevakList', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getGramsevakList",
            # response_model=List[GramsevakListItem]
            )
async def get_gramsevak_list(
        searchTerm: Optional[str] = Query(default=None, description="Searching by district name"),
        status: Optional[ApprovalStatusRequest] = Query(default=ApprovalStatusRequest.ALL),
        db: Session = Depends(get_db)
):
    print("In Router")
    return GramsevakService.get_gramsevak_list(db, search_term=searchTerm, status_filter=status)
    # return [gs.to_camel() for gs in GramsevakService.get_gramsevak_list(db, search_term=searchTerm, status_filter=status)]


VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getGramsevakById', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getGramsevakById")
# response_model=GramsevakDetailResponse)
async def get_gramsevak_by_id(
        id: int = Query(..., alias="id"),
        db: Session = Depends(get_db)
):
    print("In Router for gs")
    return GramsevakService.get_gramsevak_details(db, gramsevak_id=id)


VxAPIPermsUtils.set_perm_patch(path=router.prefix + '/changeStatus', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.patch("/changeStatus")
async def change_gramsevak_status(
        request: ChangeStatusRequest,
        db: Session = Depends(get_db)
):
    print("Hitting The router:")

    return GramsevakService.update_gramsevak_status(
        db,
        gramsevak_id=request.gramsevak_id,
        new_status=request.status
    )


VxAPIPermsUtils.set_perm_post(path=router.prefix + "/docUpload", perm=VxAPIPermsEnum.AUTHENTICATED)
@router.post("/docUpload", status_code=status.HTTP_201_CREATED)
async def upload_gramsevak_documents(
    request: Request,
    requesting_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload multiple documents where document_id is the key and file is the value.
    """
    form_data = await request.form()
    form_items = list(form_data.items())

    # Debug: print out the form items
    for key, value in form_items:
        print(f"Key: {key}, Value Type: {type(value)}")

    document_map = dict()
    metadata_map = dict()
    
    for key, value in form_items:
        # Check if this is a file upload (pure numeric key)
        if key.isdigit():
            doc_id = int(key)
            document_map[doc_id] = value
        # Check if this is metadata (format: "docId_fieldName")
        elif '_' in key:
            parts = key.split('_', 1)  # Split only on first underscore
            if parts[0].isdigit():
                doc_id = int(parts[0])
                field_name = parts[1]
                
                if doc_id not in metadata_map:
                    metadata_map[doc_id] = {}
                
                metadata_map[doc_id][field_name] = value
        else:
            # Skip invalid keys or log them
            print(f"Skipping invalid key: {key}")
            continue

    if not document_map:
        raise InvalidRequestException("No valid document data received.")

    # Pass both document files and their metadata to the service
    await GramsevakService.upload_gs_docs(
        db=db,
        gramsevak_id=requesting_user.user_id,
        documents=document_map,
        metadata=metadata_map  # Add this parameter
    )

    return {"message": "Documents uploaded successfully"}