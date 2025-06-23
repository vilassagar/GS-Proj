from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models.documents import DocumentType, UserDocument
from app.services.dal.dto.dynamic_document_dto import DocumentTypeWithFieldsDTO, UserDocumentWithFieldsDTO

class DynamicDocumentDal:
    
    @staticmethod
    def get_document_type_with_fields(db: Session, doc_type_id: int) -> Optional[DocumentTypeWithFieldsDTO]:
        doc_type = db.query(DocumentType).filter(
            DocumentType.id == doc_type_id,
            DocumentType.is_active == True
        ).first()
        
        return DocumentTypeWithFieldsDTO.to_dto(doc_type) if doc_type else None
    
    @staticmethod
    def get_all_document_types_with_fields(
        db: Session, 
        category: Optional[str] = None,
        is_mandatory: Optional[bool] = None
    ) -> List[DocumentTypeWithFieldsDTO]:
        query = db.query(DocumentType).filter(DocumentType.is_active == True)
        
        if category:
            query = query.filter(DocumentType.category == category)
        if is_mandatory is not None:
            query = query.filter(DocumentType.is_mandatory == is_mandatory)
            
        doc_types = query.all()
        return [DocumentTypeWithFieldsDTO.to_dto(dt) for dt in doc_types]
    
    @staticmethod
    def create_user_document_with_fields(
        db: Session,
        user_id: int,
        document_type_id: int,
        file_path: str,
        field_values: Dict[str, Any]
    ) -> UserDocument:
        # Delete existing document of same type for this user
        existing_doc = db.query(UserDocument).filter_by(
            user_id=user_id, 
            document_type_id=document_type_id
        ).first()
        
        if existing_doc:
            db.delete(existing_doc)
            db.flush()
        
        # Create new document
        new_doc = UserDocument(
            user_id=user_id,
            document_type_id=document_type_id,
            file_path=file_path,
            field_values=field_values,
            created_by=user_id,
            updated_by=user_id
        )
        
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)
        return new_doc
    
    @staticmethod
    def get_user_documents_with_fields(db: Session, user_id: int) -> List[UserDocumentWithFieldsDTO]:
        user_docs = db.query(UserDocument).filter(
            UserDocument.user_id == user_id,
            UserDocument.is_active == True
        ).all()
        
        return [UserDocumentWithFieldsDTO.to_dto(doc) for doc in user_docs]
    
    @staticmethod
    def update_document_verification(
        db: Session,
        document_id: int,
        verification_status: str,
        admin_comments: Optional[str],
        admin_user_id: int
    ) -> Optional[UserDocument]:
        doc = db.query(UserDocument).filter(
            UserDocument.id == document_id,
            UserDocument.is_active == True
        ).first()
        
        if not doc:
            return None
            
        doc.verification_status = verification_status
        doc.admin_comments = admin_comments
        doc.updated_by = admin_user_id
        
        db.commit()
        db.refresh(doc)
        return doc