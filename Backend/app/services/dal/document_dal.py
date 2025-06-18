from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.documents import DocumentType, UserDocument
from app.models.enums.approval_status import ApprovalStatus
from app.services.dal.dto.document_dto import DocumentTypeDTO, UserDocumentDTO


class DocumentTypeDal:
    @staticmethod
    def create_document_type(db: Session, name: str, is_mandatory: bool, created_by: int) -> DocumentType:
        new_doc_type = DocumentType(
            name=name,
            is_mandatory=is_mandatory,
            created_by=created_by
        )
        db.add(new_doc_type)
        db.commit()
        db.refresh(new_doc_type)
        return new_doc_type

    @staticmethod
    def get_document_type_by_id(db: Session, doc_type_id: int) -> Optional[DocumentTypeDTO]:
        doc_type = db.query(DocumentType).filter(DocumentType.id == doc_type_id, DocumentType.is_active).first()
        return DocumentTypeDTO.to_dto(doc_type) if doc_type else None

    @staticmethod
    def get_all_document_types(db: Session) -> List[DocumentTypeDTO]:
        doc_types = db.query(DocumentType).filter(DocumentType.is_active).all()
        return [DocumentTypeDTO.to_dto(dt) for dt in doc_types]


class UserDocumentDal:
    @staticmethod
    def create_user_document(db: Session, user_id: int, document_type_id: int, file_path: str):

        existing_doc = db.query(UserDocument).filter_by(user_id=user_id, document_type_id=document_type_id).first()

        # If an existing document is found, delete it
        if existing_doc:
            db.delete(existing_doc)
            db.commit()  # Commit deletion before inserting new document

        new_doc = UserDocument(
            user_id=user_id,
            document_type_id=document_type_id,
            file_path=file_path,
            verification_status=ApprovalStatus.PENDING,
            created_by=user_id,
            updated_by=user_id
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)

        return new_doc

    @staticmethod
    def get_user_documents(db: Session, user_id: int) -> List[UserDocumentDTO]:
        docs = db.query(UserDocument).filter(UserDocument.user_id == user_id, UserDocument.is_active).all()
        return [UserDocumentDTO.to_dto(doc) for doc in docs]

    @staticmethod
    def update_verification_status(db: Session, doc_id: int, status: str, updated_by: int) -> Optional[UserDocumentDTO]:
        doc = db.query(UserDocument).filter(UserDocument.id == doc_id, UserDocument.is_active).first()
        if not doc:
            return None

        doc.verification_status = status
        doc.updated_by = updated_by
        db.commit()
        db.refresh(doc)
        return UserDocumentDTO.to_dto(doc)