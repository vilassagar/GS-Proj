import json

from fastapi import APIRouter, Depends, UploadFile, File, status, Form
from sqlalchemy.orm import Session

from app.config import get_db
from app.schemas.government_docs_schema import BookUploadSchema, GRUploadSchema
from app.services.government_docs_service import GovernmentDocsService
from app.utils.vx_api_perms_utils import VxAPIPermsUtils, VxAPIPermsEnum

router = APIRouter(
    prefix="/v1",
    tags=["government_docs"],
    # responses={404: {"description": "Not Found"}}
)


VxAPIPermsUtils.set_perm_post(path=router.prefix + '/uploadGovernmentDoc/book', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.post("/uploadGovernmentDoc/book", status_code=status.HTTP_201_CREATED)
async def upload_book(
        # book_data: BookUploadSchema,
        book_data: str = Form(...),
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):

    book_data = json.loads(book_data)
    print("book_data: ", book_data)
    book_data = BookUploadSchema(**book_data)

    return await GovernmentDocsService.upload_book(
            db=db,
            book_data=book_data,
            file=file
        )


VxAPIPermsUtils.set_perm_post(path=router.prefix + '/uploadGovernmentDoc/gr', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.post("/uploadGovernmentDoc/gr", status_code=status.HTTP_201_CREATED)
async def upload_gr(
        gr_data: str = Form(...),
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    gr_data = json.loads(gr_data)
    print("gr_data: ", gr_data)
    gr_data = GRUploadSchema(**gr_data)

    return await GovernmentDocsService.upload_gr(
            db=db,
            gr_data=gr_data,
            file=file
        )


VxAPIPermsUtils.set_perm_get(path=router.prefix + '/GovernmentDoc/getDocs', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/GovernmentDoc/getDocs", status_code=status.HTTP_201_CREATED)
async def upload_gr(
        db: Session = Depends(get_db)
):
    return await GovernmentDocsService.get_docs(
            db=db
        )
