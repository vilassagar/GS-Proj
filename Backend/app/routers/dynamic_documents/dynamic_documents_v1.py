import json
from typing import Optional, List
from fastapi import APIRouter, Depends, UploadFile, File, Form, status, HTTPException
from sqlalchemy.orm import Session

from app.config import get_db
from app.dependencies.auth import get_current_user
from app.services.dal.dto.user_dto import UserDTO
from app.services.dynamic_document_service import DynamicDocumentService
from app.schemas.dynamic_document_schema import (
    DocumentUploadSchema, 
    DocumentVerificationSchema,
    DocumentTypeResponseSchema,
    UserDocumentResponseSchema
)
from app.utils.vx_api_perms_utils import VxAPIPermsUtils, VxAPIPermsEnum

router = APIRouter(
    prefix="/v1/documents",
    tags=["dynamic_documents"],
    responses={404: {"description": "Not Found"}}
)

# Get all document types with their field definitions
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/types', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/types", response_model=List[DocumentTypeResponseSchema])
async def get_document_types_with_fields(
    category: Optional[str] = None,
    is_mandatory: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all document types with their dynamic field definitions"""
    return DynamicDocumentService.get_document_types_with_fields(
        db, category=category, is_mandatory=is_mandatory
    )

# Get specific document type with field definitions
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/types/{document_type_id}', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/types/{document_type_id}")
async def get_document_type_fields(
    document_type_id: int,
    db: Session = Depends(get_db)
):
    """Get specific document type with its field definitions"""
    return DynamicDocumentService.get_document_type_fields(db, document_type_id)

# Upload document with dynamic fields
VxAPIPermsUtils.set_perm_post(path=router.prefix + '/upload', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document_with_fields(
    document_data: str = Form(..., description="JSON string with document_type_id and field_values"),
    file: UploadFile = File(...),
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload document with dynamic field values
    
    document_data should be JSON string like:
    {
        "document_type_id": 1,
        "field_values": {
            "aadhar_number": "1234-5678-9012",
            "full_name": "John Doe"
        }
    }
    """
    try:
        # Parse JSON data
        data_dict = json.loads(document_data)
        document_schema = DocumentUploadSchema(**data_dict)
        
        return await DynamicDocumentService.upload_document_with_fields(
            db=db,
            user_id=current_user.user_id,
            document_data=document_schema,
            file=file
        )
        
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON in document_data"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# Get user's uploaded documents
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/my-documents', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/my-documents", response_model=List[UserDocumentResponseSchema])
async def get_my_documents(
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's uploaded documents with field values"""
    return DynamicDocumentService.get_user_documents_with_fields(db, current_user.user_id)

# Admin: Verify document
VxAPIPermsUtils.set_perm_post(path=router.prefix + '/verify', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.post("/verify")
async def verify_document(
    verification_data: DocumentVerificationSchema,
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin endpoint to verify/reject documents"""
    # Check if user has admin permissions
    if current_user.role_id not in [1, 2, 3]:  # Super admin, district admin, block admin
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    return DynamicDocumentService.verify_document(
        db=db,
        verification_data=verification_data,
        admin_user_id=current_user.user_id
    )

# Get user documents by user ID (Admin only)
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/user/{user_id}', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.get("/user/{user_id}", response_model=List[UserDocumentResponseSchema])
async def get_user_documents_by_id(
    user_id: int,
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Admin endpoint to get any user's documents"""
    # Check if user has admin permissions
    if current_user.role_id not in [1, 2, 3]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    return DynamicDocumentService.get_user_documents_with_fields(db, user_id)