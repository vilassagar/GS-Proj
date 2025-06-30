# app/services/dal/document_dal.py - Updated for your SQLAlchemy models
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.documents import DocumentType, UserDocument
from app.models.enums.approval_status import ApprovalStatus
from app.services.dal.dto.document_dto import DocumentTypeDTO, UserDocumentDTO

class DocumentTypeDal:
    """Updated DocumentTypeDal to properly handle category and instructions"""
    
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
        """Get document type by ID with proper category and instructions"""
        doc_type = db.query(DocumentType).filter(
            DocumentType.id == doc_type_id, 
            DocumentType.is_active == True
        ).first()
        
        if doc_type:
            print(f"🔍 Found document type {doc_type_id}: {doc_type.name_english}")
            print(f"   Category: '{doc_type.category}'")
            print(f"   Instructions: '{doc_type.instructions}'")
        
        return DocumentTypeDTO.to_dto(doc_type) if doc_type else None

    @staticmethod
    def get_all_document_types(db: Session) -> List[DocumentTypeDTO]:
        """Get all active document types with proper category and instructions"""
        print("🔍 Fetching all document types from database...")
        
        doc_types = db.query(DocumentType).filter(
            DocumentType.is_active == True
        ).order_by(DocumentType.id).all()
        
        print(f"📊 Found {len(doc_types)} document types in database")
        
        # Convert to DTOs and debug first few
        dtos = []
        for i, dt in enumerate(doc_types):
            dto = DocumentTypeDTO.to_dto(dt)
            dtos.append(dto)
            
            # Debug first 3 documents
            if i < 3:
                print(f"📄 Document {i+1}: {dt.name_english}")
                print(f"   Category in DB: '{dt.category}' -> DTO: '{dto.category}'")
                print(f"   Instructions in DB: '{dt.instructions}' -> DTO: '{dto.instructions}'")
                print(f"   Is Mandatory: {dt.is_mandatory} -> DTO: {dto.is_mandatory}")
                print(f"   field_definitions: {dt.field_definitions} -> DTO: {dto.field_definitions}")
        
        return dtos
    
    @staticmethod
    def get_document_types_by_category(db: Session, category: str) -> List[DocumentTypeDTO]:
        """Get document types filtered by category"""
        doc_types = db.query(DocumentType).filter(
            DocumentType.is_active == True,
            DocumentType.category.ilike(f'%{category}%')  # Case-insensitive search
        ).all()
        
        return [DocumentTypeDTO.to_dto(dt) for dt in doc_types]

class UserDocumentDal:
    """Updated UserDocumentDal to properly handle document type information"""
    
    @staticmethod
    def create_user_document(db: Session, user_id: int, document_type_id: int, file_path: str):
        # Check for existing document and replace if found
        existing_doc = db.query(UserDocument).filter_by(
            user_id=user_id, 
            document_type_id=document_type_id
        ).first()

        if existing_doc:
            db.delete(existing_doc)
            db.commit()

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
        """Get user documents with document type information joined"""
        print(f"🔍 Fetching documents for user {user_id}...")
        
        # Use join to get document type information
        docs = db.query(UserDocument).join(
            DocumentType, UserDocument.document_type_id == DocumentType.id
        ).filter(
            UserDocument.user_id == user_id,
            UserDocument.is_active == True,
            DocumentType.is_active == True
        ).all()
        
        print(f"📊 Found {len(docs)} documents for user {user_id}")
        
        return [UserDocumentDTO.to_dto(doc) for doc in docs]

    @staticmethod
    def update_verification_status(db: Session, doc_id: int, status: str, updated_by: int) -> Optional[UserDocumentDTO]:
        doc = db.query(UserDocument).filter(
            UserDocument.id == doc_id, 
            UserDocument.is_active == True
        ).first()
        
        if not doc:
            return None

        doc.verification_status = status
        doc.updated_by = updated_by
        db.commit()
        db.refresh(doc)
        return UserDocumentDTO.to_dto(doc)