from datetime import datetime
from typing import Optional, Dict, Any, List
from app.models.documents import DocumentType, UserDocument
from app.services.dal.dto.to_camel import ToCamel

class DocumentFieldDefinition(ToCamel):
    def __init__(
        self,
        field_name: str,
        field_type: str,
        label: str,
        label_english: str,
        is_required: bool = False,
        validation_rules: Optional[Dict[str, Any]] = None,
        options: Optional[List[str]] = None,
        placeholder: Optional[str] = None,
        help_text: Optional[str] = None
    ):
        self.field_name = field_name
        self.field_type = field_type
        self.label = label
        self.label_english = label_english
        self.is_required = is_required
        self.validation_rules = validation_rules or {}
        self.options = options or []
        self.placeholder = placeholder
        self.help_text = help_text

class DocumentTypeWithFieldsDTO(ToCamel):
    def __init__(
        self,
        id: int,
        name: str,
        name_english: Optional[str],
        is_mandatory: bool,
        category: Optional[str],
        instructions: Optional[str],
        field_definitions: List[DocumentFieldDefinition],
        created_at: datetime,
        updated_at: Optional[datetime],
        is_active: bool
    ):
        self.document_type_id = id
        self.document_type_name = name
        self.document_type_name_english = name_english
        self.is_mandatory = is_mandatory
        self.category = category
        self.instructions = instructions
        self.field_definitions = field_definitions
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active

    @staticmethod
    def to_dto(doc_type: DocumentType) -> "DocumentTypeWithFieldsDTO":
        field_definitions = []
        if doc_type.field_definitions:
            for field_name, field_config in doc_type.field_definitions.items():
                field_definitions.append(DocumentFieldDefinition(
                    field_name=field_name,
                    field_type=field_config.get('type', 'TEXT'),
                    label=field_config.get('label', field_name),
                    label_english=field_config.get('label_english', field_name),
                    is_required=field_config.get('required', False),
                    validation_rules=field_config.get('validation', {}),
                    options=field_config.get('options', []),
                    placeholder=field_config.get('placeholder'),
                    help_text=field_config.get('help_text')
                ))
        
        return DocumentTypeWithFieldsDTO(
            id=doc_type.id,
            name=doc_type.name,
            name_english=doc_type.name_english,
            is_mandatory=doc_type.is_mandatory,
            category=doc_type.category,
            instructions=doc_type.instructions,
            field_definitions=field_definitions,
            created_at=doc_type.created_at,
            updated_at=doc_type.updated_at,
            is_active=doc_type.is_active
        )

class UserDocumentWithFieldsDTO(ToCamel):
    def __init__(
        self,
        id: int,
        document_type: DocumentTypeWithFieldsDTO,
        file_path: str,
        field_values: Dict[str, Any],
        verification_status: str,
        admin_comments: Optional[str],
        created_at: datetime,
        updated_at: Optional[datetime]
    ):
        self.user_document_id = id
        self.document_type = document_type
        self.file_path = file_path
        self.field_values = field_values
        self.verification_status = verification_status
        self.admin_comments = admin_comments
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def to_dto(user_doc: UserDocument) -> "UserDocumentWithFieldsDTO":
        return UserDocumentWithFieldsDTO(
            id=user_doc.id,
            document_type=DocumentTypeWithFieldsDTO.to_dto(user_doc.document_type),
            file_path=user_doc.file_path,
            field_values=user_doc.field_values or {},
            verification_status=user_doc.verification_status.value,
            admin_comments=user_doc.admin_comments,
            created_at=user_doc.created_at,
            updated_at=user_doc.updated_at
        )