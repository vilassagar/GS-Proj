from datetime import datetime
from typing import Optional
from app.models.documents import DocumentType, UserDocument
from app.services.dal.dto.to_camel import ToCamel


class DocumentTypeDTO(ToCamel):
    def __init__(
            self,
            id: int,
            name: str,
            is_mandatory: bool,
            created_by: Optional[int],
            updated_by: Optional[int],
            created_at: datetime,
            updated_at: Optional[datetime],
            is_active: bool
    ):
        self.id = id
        self.name = name
        self.is_mandatory = is_mandatory
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active

    @staticmethod
    def to_dto(doc_type: DocumentType) -> "DocumentTypeDTO":
        return DocumentTypeDTO(
            id=doc_type.id,
            name=doc_type.name,
            is_mandatory=doc_type.is_mandatory,
            created_by=doc_type.created_by,
            updated_by=doc_type.updated_by,
            created_at=doc_type.created_at,
            updated_at=doc_type.updated_at,
            is_active=doc_type.is_active
        )


class UserDocumentDTO(ToCamel):
    def __init__(
            self,
            id: int,
            document_type: str,
            user_id: int,
            document_type_id: int,
            file_path: str,
            verification_status: str,
            created_by: Optional[int],
            updated_by: Optional[int],
            created_at: datetime,
            updated_at: Optional[datetime],
            is_active: bool
    ):
        self.id = id
        self.user_id = user_id
        self.document_type_id = document_type_id
        self.document_type = document_type
        self.file_path = file_path
        self.verification_status = verification_status
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active

    @staticmethod
    def to_dto(user_doc: UserDocument) -> "UserDocumentDTO":
        return UserDocumentDTO(
            id=user_doc.id,
            document_type=user_doc.document_type.name,
            user_id=user_doc.user_id,
            document_type_id=user_doc.document_type_id,
            file_path=user_doc.file_path,
            verification_status=user_doc.verification_status,
            created_by=user_doc.created_by,
            updated_by=user_doc.updated_by,
            created_at=user_doc.created_at,
            updated_at=user_doc.updated_at,
            is_active=user_doc.is_active
        )
