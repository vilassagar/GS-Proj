from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import get_db
from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.services.document_service import DocumentTypeService
from app.utils.vx_api_perms_utils import VxAPIPermsUtils

router = APIRouter(
    prefix="/v1/upload",
    tags=["gramsevak"],
    responses={404: {"description": "Not Found"}}
)


VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getdocumenttype', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getdocumenttype",
            # response_model=List[GramsevakListItem]
            )
async def get_all_document_types(db: Session = Depends(get_db)):
    return DocumentTypeService.get_all_document_types(db=db)
