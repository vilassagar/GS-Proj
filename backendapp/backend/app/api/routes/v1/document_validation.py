# app/api/routes/v1/document_validation.py
"""
Example API endpoint showing how to use document types with field validation
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import json
import re
from datetime import datetime

from app.config import get_db
from app.dependencies.auth import get_current_user
from app.services.dal.dto.user_dto import UserDTO
from app.services.dal.document_dal import DocumentTypeDal, UserDocumentDal
from app.utils.vx_api_perms_utils import VxAPIPermsUtils, VxAPIPermsEnum

router = APIRouter(
    prefix="/v1/documents",
    tags=["document_validation"],
    responses={404: {"description": "Not Found"}}
)

class DocumentValidator:
    """Validates document field values based on field definitions"""
    
    @staticmethod
    def validate_field(field_name: str, field_value: Any, field_definition: Dict) -> Dict[str, Any]:
        """Validate a single field value"""
        errors = []
        field_type = field_definition.get('type', 'text')
        is_required = field_definition.get('required', False)
        
        # Check if required field is empty
        if is_required and (field_value is None or field_value == ''):
            errors.append(f"{field_definition.get('label', field_name)} is required")
            return {'valid': False, 'errors': errors}
        
        # Skip validation if field is empty and not required
        if field_value is None or field_value == '':
            return {'valid': True, 'errors': []}
        
        # Type-specific validation
        if field_type == 'text':
            # Pattern validation
            pattern = field_definition.get('pattern')
            if pattern and not re.match(pattern, str(field_value)):
                validation_msg = field_definition.get('validation_message', 
                    f"{field_definition.get('label', field_name)} format is invalid")
                errors.append(validation_msg)
        
        elif field_type == 'number':
            try:
                num_value = float(field_value)
                min_val = field_definition.get('min')
                max_val = field_definition.get('max')
                
                if min_val is not None and num_value < min_val:
                    errors.append(f"{field_definition.get('label', field_name)} must be at least {min_val}")
                if max_val is not None and num_value > max_val:
                    errors.append(f"{field_definition.get('label', field_name)} must be at most {max_val}")
            except (ValueError, TypeError):
                errors.append(f"{field_definition.get('label', field_name)} must be a valid number")
        
        elif field_type == 'date':
            try:
                # Try to parse the date
                if isinstance(field_value, str):
                    datetime.strptime(field_value, '%Y-%m-%d')
            except ValueError:
                errors.append(f"{field_definition.get('label', field_name)} must be a valid date (YYYY-MM-DD)")
        
        elif field_type == 'select':
            options = field_definition.get('options', [])
            if options and field_value not in options:
                errors.append(f"{field_definition.get('label', field_name)} must be one of: {', '.join(options)}")
        
        return {'valid': len(errors) == 0, 'errors': errors}
    
    @staticmethod
    def validate_document_fields(document_type_id: int, field_values: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """Validate all field values for a document type"""
        
        # Get document type with field definitions
        doc_type = DocumentTypeDal.get_document_type_by_id(db, document_type_id)
        if not doc_type:
            return {'valid': False, 'errors': ['Document type not found']}
        
        field_definitions = doc_type.field_definitions or {}
        all_errors = []
        field_results = {}
        
        # Validate each field
        for field_name, field_definition in field_definitions.items():
            field_value = field_values.get(field_name)
            result = DocumentValidator.validate_field(field_name, field_value, field_definition)
            field_results[field_name] = result
            
            if not result['valid']:
                all_errors.extend(result['errors'])
        
        # Check for extra fields (not defined in field_definitions)
        extra_fields = set(field_values.keys()) - set(field_definitions.keys())
        if extra_fields:
            all_errors.append(f"Unknown fields: {', '.join(extra_fields)}")
        
        return {
            'valid': len(all_errors) == 0,
            'errors': all_errors,
            'field_results': field_results,
            'document_type': {
                'id': doc_type.id,
                'name': doc_type.name,
                'name_english': doc_type.name_english,
                'category': doc_type.category
            }
        }

# Get document types with field definitions
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/types', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/types")
async def get_document_types_with_fields(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get document types with their field definitions"""
    
    doc_types = DocumentTypeDal.get_all_document_types(db)
    
    # Filter by category if provided
    if category:
        doc_types = [dt for dt in doc_types if getattr(dt, 'category', '') == category]
    
    result = []
    for dt in doc_types:
        result.append({
            'documentTypeId': dt.id,
            'name': dt.name,
            'nameEnglish': dt.name_english,
            'category': dt.category,
            'isMandatory': dt.is_mandatory,
            'instructions': dt.instructions,
            'fieldDefinitions': dt.field_definitions or {},
            'exampleValues': DocumentValidator._get_example_values(dt.field_definitions or {})
        })
    
    return {
        'documentTypes': result,
        'totalCount': len(result)
    }

# Validate document fields before upload
VxAPIPermsUtils.set_perm_post(path=router.prefix + '/validate-fields', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.post("/validate-fields")
async def validate_document_fields(
    document_type_id: int = Form(...),
    field_values: str = Form(...),  # JSON string of field values
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Validate document field values before upload"""
    
    try:
        # Parse field values JSON
        parsed_field_values = json.loads(field_values)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON format for field_values"
        )
    
    # Validate the fields
    validation_result = DocumentValidator.validate_document_fields(
        document_type_id, parsed_field_values, db
    )
    
    return {
        'userId': current_user.user_id,
        'documentTypeId': document_type_id,
        'validation': validation_result,
        'canProceedWithUpload': validation_result['valid']
    }

# Upload document with field validation
VxAPIPermsUtils.set_perm_post(path=router.prefix + '/upload-with-validation', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.post("/upload-with-validation")
async def upload_document_with_validation(
    document_type_id: int = Form(...),
    field_values: str = Form(...),  # JSON string of field values
    file: UploadFile = File(...),
    current_user: UserDTO = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload document with field validation"""
    
    try:
        # Parse field values JSON
        parsed_field_values = json.loads(field_values)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON format for field_values"
        )
    
    # Validate the fields first
    validation_result = DocumentValidator.validate_document_fields(
        document_type_id, parsed_field_values, db
    )
    
    if not validation_result['valid']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'message': 'Field validation failed',
                'errors': validation_result['errors'],
                'fieldResults': validation_result['field_results']
            }
        )
    
    # Validate file type
    allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx']
    file_extension = file.filename.split('.')[-1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload PDF, JPG, PNG, DOC, or DOCX files only."
        )
    
    # Save file (implement your file saving logic here)
    file_path = f"user_docs/user_{current_user.user_id}/doc_type_{document_type_id}/{file.filename}"
    
    # Create document record with validated field values
    try:
        user_doc = UserDocumentDal.create_user_document(
            db=db,
            user_id=current_user.user_id,
            document_type_id=document_type_id,
            file_path=file_path
        )
        
        # Update the document with field values
        # (You would implement update logic in UserDocumentDal)
        
        return {
            'message': 'Document uploaded successfully with validated field data',
            'documentId': user_doc.id,
            'documentType': validation_result['document_type'],
            'fieldValues': parsed_field_values,
            'filePath': file_path,
            'validation': validation_result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save document: {str(e)}"
        )

# Get example field values for a document type
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/types/{document_type_id}/examples', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/types/{document_type_id}/examples")
async def get_document_field_examples(
    document_type_id: int,
    db: Session = Depends(get_db)
):
    """Get example field values for a document type"""
    
    doc_type = DocumentTypeDal.get_document_type_by_id(db, document_type_id)
    if not doc_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document type not found"
        )
    
    field_definitions = doc_type.field_definitions or {}
    examples = DocumentValidator._get_example_values(field_definitions)
    
    return {
        'documentTypeId': document_type_id,
        'documentTypeName': doc_type.name_english,
        'fieldDefinitions': field_definitions,
        'exampleValues': examples,
        'instructions': doc_type.instructions
    }

# Helper method for DocumentValidator
def _get_example_values(field_definitions: Dict) -> Dict[str, Any]:
    """Generate example values for field definitions"""
    examples = {}
    
    for field_name, field_def in field_definitions.items():
        field_type = field_def.get('type', 'text')
        
        if field_type == 'text':
            placeholder = field_def.get('placeholder', '')
            if 'aadhaar' in field_name.lower():
                examples[field_name] = '1234 5678 9012'
            elif 'pan' in field_name.lower():
                examples[field_name] = 'ABCDE1234F'
            elif 'phone' in field_name.lower() or 'mobile' in field_name.lower():
                examples[field_name] = '+91 9876543210'
            elif placeholder:
                examples[field_name] = placeholder
            else:
                examples[field_name] = f'Example {field_def.get("label", field_name)}'
        
        elif field_type == 'number':
            min_val = field_def.get('min', 0)
            max_val = field_def.get('max', 100)
            examples[field_name] = min_val + (max_val - min_val) / 2
        
        elif field_type == 'date':
            examples[field_name] = '1990-01-01'
        
        elif field_type == 'select':
            options = field_def.get('options', [])
            examples[field_name] = options[0] if options else ''
        
        elif field_type == 'textarea':
            examples[field_name] = f'Example {field_def.get("label", field_name)} text...'
    
    return examples

# Add the helper method to DocumentValidator class
#DocumentValidator._get_example_values = staticmethod(_get_example_values)