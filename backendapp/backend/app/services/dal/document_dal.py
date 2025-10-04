# app/services/dal/document_dal.py - Updated for your SQLAlchemy models
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models.documents import DocumentType, UserDocument
from app.models.enums.approval_status import ApprovalStatus
from app.services.dal.dto.document_dto import DocumentTypeDTO, UserDocumentDTO
from sqlalchemy.orm import Session

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
    @staticmethod
    def get_all_document_types(db: Session) -> List:
        """FIXED: Get all active document types with proper error handling"""
        print("🔍 DocumentTypeDal: Fetching all document types...")
        
        try:
            from app.models.documents import DocumentType
            
            # Query with explicit filtering and ordering
            doc_types = db.query(DocumentType).filter(
                DocumentType.is_active == True
            ).order_by(DocumentType.id).all()
            
            print(f"📊 Raw query returned {len(doc_types)} document types")
            
            # Convert to DTOs
            from app.services.dal.dto.document_dto import DocumentTypeDTO
            dtos = []
            
            for i, dt in enumerate(doc_types):
                try:
                    dto = DocumentTypeDTO.to_dto(dt)
                    dtos.append(dto)
                    
                    # Debug first few
                    if i < 3:
                        print(f"📄 Document {i+1}: {dt.name_english}")
                        print(f"   Category: '{dt.category}'")
                        print(f"   Is Mandatory: {dt.is_mandatory}")
                        print(f"   Field Definitions: {bool(dt.field_definitions)}")
                        
                except Exception as dto_error:
                    print(f"⚠️  Error converting document type {dt.id} to DTO: {dto_error}")
                    continue
            
            print(f"✅ Successfully converted {len(dtos)} documents to DTOs")
            return dtos
            
        except Exception as e:
            print(f"❌ Error in DocumentTypeDal.get_all_document_types: {e}")
            import traceback
            traceback.print_exc()
            return []

    
    @staticmethod
    def get_document_types_by_category(db: Session, category: str) -> List[DocumentTypeDTO]:
        """Get document types filtered by category"""
        doc_types = db.query(DocumentType).filter(
            DocumentType.is_active == True,
            DocumentType.category.ilike(f'%{category}%')  # Case-insensitive search
        ).all()
        
        return [DocumentTypeDTO.to_dto(dt) for dt in doc_types]

class DocumentTypeDalAdditionalMethods:
    """Additional methods to add to DocumentTypeDal"""
    
    @staticmethod
    def update_document_type(
        db: Session, 
        document_type_id: int, 
        update_data: Dict[str, Any]
    ) -> Optional[DocumentType]:
        """Update a document type with new data"""
        
        doc_type = db.query(DocumentType).filter(
            DocumentType.id == document_type_id,
            DocumentType.is_active == True
        ).first()
        
        if not doc_type:
            return None
        
        # Update fields
        for key, value in update_data.items():
            if hasattr(doc_type, key):
                setattr(doc_type, key, value)
        
        db.commit()
        db.refresh(doc_type)
        return doc_type
    
    @staticmethod
    def get_document_type_with_usage_stats(
        db: Session, 
        document_type_id: int
    ) -> Optional[Dict[str, Any]]:
        """Get document type with usage statistics"""
        
        doc_type = db.query(DocumentType).filter(
            DocumentType.id == document_type_id,
            DocumentType.is_active == True
        ).first()
        
        if not doc_type:
            return None
        
        # Get usage statistics
        total_uploads = db.query(UserDocument).filter(
            UserDocument.document_type_id == document_type_id,
            UserDocument.is_active == True
        ).count()
        
        approved_uploads = db.query(UserDocument).filter(
            UserDocument.document_type_id == document_type_id,
            UserDocument.is_active == True,
            UserDocument.verification_status == ApprovalStatus.APPROVED
        ).count()
        
        pending_uploads = db.query(UserDocument).filter(
            UserDocument.document_type_id == document_type_id,
            UserDocument.is_active == True,
            UserDocument.verification_status == ApprovalStatus.PENDING
        ).count()
        
        rejected_uploads = db.query(UserDocument).filter(
            UserDocument.document_type_id == document_type_id,
            UserDocument.is_active == True,
            UserDocument.verification_status == ApprovalStatus.REJECTED
        ).count()
        
        return {
            "documentType": doc_type,
            "usageStats": {
                "totalUploads": total_uploads,
                "approvedUploads": approved_uploads,
                "pendingUploads": pending_uploads,
                "rejectedUploads": rejected_uploads,
                "approvalRate": (approved_uploads / total_uploads * 100) if total_uploads > 0 else 0
            }
        }


class UserDocumentDalAdditionalMethods:
    """Additional methods to add to UserDocumentDal"""
    
    @staticmethod
    def get_user_document_by_id(
        db: Session, 
        user_id: int, 
        document_id: int
    ) -> Optional[UserDocument]:
        """Get a specific user document by ID, ensuring user ownership"""
        
        user_doc = db.query(UserDocument).filter(
            UserDocument.id == document_id,
            UserDocument.user_id == user_id,
            UserDocument.is_active == True
        ).first()
        
        return user_doc

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
    
    @staticmethod
    def update_user_document(
        db: Session, 
        document_id: int, 
        update_data: Dict[str, Any]
    ) -> Optional[UserDocument]:
        """Update a user document with new data"""
        from datetime import datetime
        
        user_doc = db.query(UserDocument).filter(
            UserDocument.id == document_id,
            UserDocument.is_active == True
        ).first()
        
        if not user_doc:
            return None
        
        # Update fields
        for key, value in update_data.items():
            if hasattr(user_doc, key):
                setattr(user_doc, key, value)
        
        # Set updated timestamp
        user_doc.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(user_doc)
        return user_doc    

# @staticmethod
# def update_user_document(
#     db: Session, 
#     document_id: int, 
#     update_data: Dict[str, Any]
# ) -> Optional[UserDocument]:
#     """Update a user document with new data"""
    
#     user_doc = db.query(UserDocument).filter(
#         UserDocument.id == document_id,
#         UserDocument.is_active == True
#     ).first()
    
#     if not user_doc:
#         return None
    
#     # Update fields
#     for key, value in update_data.items():
#         if hasattr(user_doc, key):
#             setattr(user_doc, key, value)
    
#     # Set updated timestamp
#     from datetime import datetime
#     user_doc.updated_at = datetime.utcnow()
    
#     db.commit()
#     db.refresh(user_doc)
#     return user_doc
    
#     @staticmethod
#     def get_user_documents_with_field_completion(
#         db: Session, 
#         user_id: int
#     ) -> List[Dict[str, Any]]:
#         """Get user documents with field completion analysis"""
        
#         # Get user documents with joined document types
#         docs = db.query(UserDocument).join(
#             DocumentType, UserDocument.document_type_id == DocumentType.id
#         ).filter(
#             UserDocument.user_id == user_id,
#             UserDocument.is_active == True,
#             DocumentType.is_active == True
#         ).all()
        
#         result = []
#         for doc in docs:
#             # Get field definitions from document type
#             field_definitions = getattr(doc.document_type, 'field_definitions', {}) or {}
#             field_values = getattr(doc, 'field_values', {}) or {}
            
#             # Calculate field completion
#             field_completion = UserDocumentDalAdditionalMethods._calculate_field_completion(
#                 field_values, field_definitions
#             )
            
#             result.append({
#                 "document": doc,
#                 "fieldCompletion": field_completion,
#                 "fieldDefinitions": field_definitions,
#                 "fieldValues": field_values
#             })
        
#         return result
    
#     @staticmethod
#     def get_documents_by_verification_status(
#         db: Session, 
#         user_id: int = None, 
#         verification_status: str = None
#     ) -> List[UserDocument]:
#         """Get documents filtered by verification status"""
        
#         query = db.query(UserDocument).join(
#             DocumentType, UserDocument.document_type_id == DocumentType.id
#         ).filter(
#             UserDocument.is_active == True,
#             DocumentType.is_active == True
#         )
        
#         if user_id:
#             query = query.filter(UserDocument.user_id == user_id)
        
#         if verification_status:
#             query = query.filter(UserDocument.verification_status == verification_status)
        
#         return query.all()
    
#     @staticmethod
#     def get_user_documents_summary(db: Session, user_id: int) -> Dict[str, Any]:
#         """Get summary statistics for user documents"""
        
#         # Get all user documents
#         all_docs = db.query(UserDocument).filter(
#             UserDocument.user_id == user_id,
#             UserDocument.is_active == True
#         ).all()
        
#         # Count by status
#         total_docs = len(all_docs)
#         approved_docs = len([doc for doc in all_docs if doc.verification_status == ApprovalStatus.APPROVED])
#         pending_docs = len([doc for doc in all_docs if doc.verification_status == ApprovalStatus.PENDING])
#         rejected_docs = len([doc for doc in all_docs if doc.verification_status == ApprovalStatus.REJECTED])
        
#         # Get mandatory vs optional counts
#         mandatory_docs = db.query(UserDocument).join(
#             DocumentType, UserDocument.document_type_id == DocumentType.id
#         ).filter(
#             UserDocument.user_id == user_id,
#             UserDocument.is_active == True,
#             DocumentType.is_mandatory == True
#         ).all()
        
#         optional_docs = db.query(UserDocument).join(
#             DocumentType, UserDocument.document_type_id == DocumentType.id
#         ).filter(
#             UserDocument.user_id == user_id,
#             UserDocument.is_active == True,
#             DocumentType.is_mandatory == False
#         ).all()
        
#         return {
#             "totalDocuments": total_docs,
#             "approvedDocuments": approved_docs,
#             "pendingDocuments": pending_docs,
#             "rejectedDocuments": rejected_docs,
#             "mandatoryDocuments": len(mandatory_docs),
#             "optionalDocuments": len(optional_docs),
#             "approvalRate": (approved_docs / total_docs * 100) if total_docs > 0 else 0,
#             "lastUploadDate": max([doc.created_at for doc in all_docs]) if all_docs else None
#         }
    
#     @staticmethod
#     def soft_delete_user_document(db: Session, document_id: int, user_id: int) -> bool:
#         """Soft delete a user document"""
        
#         user_doc = db.query(UserDocument).filter(
#             UserDocument.id == document_id,
#             UserDocument.user_id == user_id,
#             UserDocument.is_active == True
#         ).first()
        
#         if not user_doc:
#             return False
        
#         user_doc.is_active = False
#         user_doc.updated_at = datetime.utcnow()
        
#         db.commit()
#         return True
    
#     @staticmethod
#     def get_documents_requiring_field_updates(db: Session, user_id: int = None) -> List[Dict[str, Any]]:
#         """Get documents that have field definitions but missing or incomplete field values"""
        
#         query = db.query(UserDocument).join(
#             DocumentType, UserDocument.document_type_id == DocumentType.id
#         ).filter(
#             UserDocument.is_active == True,
#             DocumentType.is_active == True,
#             DocumentType.field_definitions.isnot(None)
#         )
        
#         if user_id:
#             query = query.filter(UserDocument.user_id == user_id)
        
#         docs = query.all()
        
#         result = []
#         for doc in docs:
#             field_definitions = getattr(doc.document_type, 'field_definitions', {}) or {}
#             field_values = getattr(doc, 'field_values', {}) or {}
            
#             # Check if field update is needed
#             field_completion = UserDocumentDalAdditionalMethods._calculate_field_completion(
#                 field_values, field_definitions
#             )
            
#             if not field_completion['isComplete']:
#                 result.append({
#                     "document": doc,
#                     "fieldCompletion": field_completion,
#                     "missingRequiredFields": field_completion['missingRequiredFields']
#                 })
        
#         return result
    
#     # Helper methods
    
#     @staticmethod
#     def _calculate_field_completion(field_values: Dict[str, Any], field_definitions: Dict[str, Any]) -> Dict[str, Any]:
#         """Calculate field completion status"""
        
#         if not field_definitions:
#             return {
#                 "totalFields": 0,
#                 "completedFields": 0,
#                 "requiredFields": 0,
#                 "completedRequiredFields": 0,
#                 "isComplete": True,
#                 "completionPercentage": 100,
#                 "missingRequiredFields": []
#             }
        
#         total_fields = len(field_definitions)
#         required_fields = [name for name, config in field_definitions.items() if config.get('required', False)]
        
#         completed_fields = 0
#         completed_required_fields = 0
#         missing_required_fields = []
        
#         for field_name, field_config in field_definitions.items():
#             field_value = field_values.get(field_name)
#             has_value = field_value is not None and field_value != ''
            
#             if has_value:
#                 completed_fields += 1
            
#             is_required = field_config.get('required', False)
#             if is_required:
#                 if has_value:
#                     completed_required_fields += 1
#                 else:
#                     missing_required_fields.append({
#                         "fieldName": field_name,
#                         "label": field_config.get('label', field_name),
#                         "type": field_config.get('type', 'text'),
#                         "required": True
#                     })
        
#         is_complete = len(missing_required_fields) == 0
#         completion_percentage = (completed_fields / total_fields * 100) if total_fields > 0 else 100
        
#         return {
#             "totalFields": total_fields,
#             "completedFields": completed_fields,
#             "requiredFields": len(required_fields),
#             "completedRequiredFields": completed_required_fields,
#             "isComplete": is_complete,
#             "completionPercentage": round(completion_percentage, 2),
#             "missingRequiredFields": missing_required_fields
#         }

# class UserDocumentDal:
#     """Updated UserDocumentDal to properly handle document type information"""
    
#     @staticmethod
#     def create_user_document(db: Session, user_id: int, document_type_id: int, file_path: str):
#         # Check for existing document and replace if found
#         existing_doc = db.query(UserDocument).filter_by(
#             user_id=user_id, 
#             document_type_id=document_type_id
#         ).first()

#         if existing_doc:
#             db.delete(existing_doc)
#             db.commit()

#         new_doc = UserDocument(
#             user_id=user_id,
#             document_type_id=document_type_id,
#             file_path=file_path,
#             verification_status=ApprovalStatus.PENDING,
#             created_by=user_id,
#             updated_by=user_id
#         )
#         db.add(new_doc)
#         db.commit()
#         db.refresh(new_doc)

#         return new_doc

#     @staticmethod
#     def get_user_documents(db: Session, user_id: int) -> List[UserDocumentDTO]:
#         """Get user documents with document type information joined"""
#         print(f"🔍 Fetching documents for user {user_id}...")
        
#         # Use join to get document type information
#         docs = db.query(UserDocument).join(
#             DocumentType, UserDocument.document_type_id == DocumentType.id
#         ).filter(
#             UserDocument.user_id == user_id,
#             UserDocument.is_active == True,
#             DocumentType.is_active == True
#         ).all()
        
#         print(f"📊 Found {len(docs)} documents for user {user_id}")
        
#         return [UserDocumentDTO.to_dto(doc) for doc in docs]

#     @staticmethod
#     def update_verification_status(db: Session, doc_id: int, status: str, updated_by: int) -> Optional[UserDocumentDTO]:
#         doc = db.query(UserDocument).filter(
#             UserDocument.id == doc_id, 
#             UserDocument.is_active == True
#         ).first()
        
#         if not doc:
#             return None

#         doc.verification_status = status
#         doc.updated_by = updated_by
#         db.commit()
#         db.refresh(doc)
#         return UserDocumentDTO.to_dto(doc)