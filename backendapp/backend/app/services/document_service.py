from typing import List, Dict, Union, Optional, Any
from sqlalchemy.orm import Session
from app.services.dal.document_dal import DocumentTypeDal

class DocumentTypeService:
    @staticmethod
    def get_all_document_types(db: Session) -> List[Dict[str, Union[int, bool, str]]]:
        """Legacy method - kept for backward compatibility"""
        dts = DocumentTypeDal.get_all_document_types(db=db)

        return [
            {
                "documentTypeId": dt.id,
                "documentTypeName": dt.name,
                "mandatory": dt.is_mandatory,  # Fixed typo: was "mendatory"
            } for dt in dts
        ]
    
    @staticmethod
    def get_all_document_types_enhanced(
        db: Session, 
        category: Optional[str] = None,
        is_mandatory: Optional[bool] = None,
        include_field_definitions: bool = True
    ) -> Dict[str, Any]:
        """
        Enhanced method that returns comprehensive document type information
        """
        print(f"🔍 Getting document types - category: {category}, mandatory: {is_mandatory}")
        
        # Get all document types from DAL
        all_doc_types = DocumentTypeDal.get_all_document_types(db=db)
        print(f"📊 Found {len(all_doc_types)} total document types")
        
        # Apply filters
        filtered_doc_types = all_doc_types
        
        if category:
            filtered_doc_types = [
                dt for dt in filtered_doc_types 
                if getattr(dt, 'category', '').lower() == category.lower()
            ]
            print(f"📊 After category filter ({category}): {len(filtered_doc_types)} documents")
        
        if is_mandatory is not None:
            filtered_doc_types = [
                dt for dt in filtered_doc_types 
                if getattr(dt, 'is_mandatory', False) == is_mandatory
            ]
            print(f"📊 After mandatory filter ({is_mandatory}): {len(filtered_doc_types)} documents")
        
        # Build comprehensive response
        document_types = []
        category_stats = {}
        
        for dt in filtered_doc_types:
            # Get all attributes safely
            doc_id = getattr(dt, 'id', 0)
            name = getattr(dt, 'name', '')
            name_english = getattr(dt, 'name_english', '')
            is_mandatory_val = getattr(dt, 'is_mandatory', False)
            category_val = getattr(dt, 'category', 'other')
            instructions = getattr(dt, 'instructions', 'Please upload this document')
            
            # Handle field_definitions (could be JSON string or dict)
            field_definitions = getattr(dt, 'field_definitions', None)
            if isinstance(field_definitions, str):
                try:
                    import json
                    field_definitions = json.loads(field_definitions)
                except (json.JSONDecodeError, TypeError):
                    field_definitions = {}
            elif field_definitions is None:
                field_definitions = {}
            
            # Build document type object
            doc_type_obj = {
                "documentTypeId": doc_id,
                "documentTypeName": name,
                "documentTypeNameEnglish": name_english,
                "category": category_val,
                "categoryMarathi": _get_category_marathi_name(category_val),
                "isMandatory": is_mandatory_val,
                "instructions": instructions,
                "maxFileSizeMb": 5,  # Default file size limit
                "allowedFormats": ["pdf", "jpg", "jpeg", "png", "doc", "docx"],
                "isActive": getattr(dt, 'is_active', True),
                "createdAt": getattr(dt, 'created_at').isoformat() if hasattr(dt, 'created_at') and dt.created_at else None
            }
            
            # Include field definitions if requested
            if include_field_definitions:
                doc_type_obj["fieldDefinitions"] = field_definitions
                doc_type_obj["hasFieldDefinitions"] = bool(field_definitions)
                doc_type_obj["fieldCount"] = len(field_definitions) if field_definitions else 0
            
            document_types.append(doc_type_obj)
            
            # Update category statistics
            if category_val not in category_stats:
                category_stats[category_val] = {
                    "categoryName": category_val,
                    "categoryMarathi": _get_category_marathi_name(category_val),
                    "totalDocuments": 0,
                    "mandatoryDocuments": 0,
                    "optionalDocuments": 0
                }
            
            category_stats[category_val]["totalDocuments"] += 1
            if is_mandatory_val:
                category_stats[category_val]["mandatoryDocuments"] += 1
            else:
                category_stats[category_val]["optionalDocuments"] += 1
        
        # Build final response
        response = {
            "success": True,
            "totalDocumentTypes": len(document_types),
            "filteredCount": len(document_types),
            "totalAvailable": len(all_doc_types),
            "filters": {
                "category": category,
                "isMandatory": is_mandatory,
                "includeFieldDefinitions": include_field_definitions
            },
            "documentTypes": document_types,
            "categoryStats": list(category_stats.values()),
            "availableCategories": list(set(getattr(dt, 'category', 'other') for dt in all_doc_types)),
            "lastUpdated": "2025-01-20T10:00:00Z"  # You can make this dynamic
        }
        
        print(f"✅ Returning {len(document_types)} document types")
        return response

def _get_category_marathi_name(category: str) -> str:
    """Get Marathi name for category"""
    category_mapping = {
        "identity_proof": "ओळख पुरावा",
        "address_proof": "पत्ता पुरावा",
        "educational": "शैक्षणिक",
        "caste_category": "जात प्रमाण",
        "professional": "व्यावसायिक", 
        "income_proof": "उत्पन्न पुरावा",
        "medical": "वैद्यकीय",
        "other": "इतर"
    }
    return category_mapping.get(category.lower(), category)
