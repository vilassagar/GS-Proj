# app/schemas/document_schema.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class DocumentCategory(str, Enum):
    """Document categories for organizing different types of documents"""
    IDENTITY_PROOF = "identity_proof"
    EDUCATIONAL = "educational"
    ADDRESS_PROOF = "address_proof"
    PROFESSIONAL = "professional"
    CASTE_CATEGORY = "caste_category"
    INCOME_PROOF = "income_proof"
    MEDICAL = "medical"
    OTHER = "other"

class DocumentType(BaseModel):
    """Document type model with category support"""
    id: int
    name: str
    name_english: str
    category: DocumentCategory
    is_mandatory: bool = False
    instructions: Optional[str] = None
    max_file_size_mb: int = 5
    allowed_formats: List[str] = ["pdf", "jpg", "jpeg", "png", "doc", "docx"]
    
    class Config:
        from_attributes = True

class DocumentCategoryResponse(BaseModel):
    """Response model for document categories with their types"""
    category: DocumentCategory
    category_name: str
    category_name_english: str
    description: Optional[str] = None
    document_types: List[DocumentType] = []
    
    class Config:
        from_attributes = True

# Document type definitions by category
DOCUMENT_CATEGORIES_CONFIG = {
    DocumentCategory.IDENTITY_PROOF: {
        "name": "पहचान प्रमाण",
        "name_english": "Identity Proof",
        "description": "Documents to verify your identity",
        "types": [
            {
                "name": "आधार कार्ड",
                "name_english": "Aadhaar Card",
                "is_mandatory": True,
                "instructions": "Clear photo of both front and back side"
            },
            {
                "name": "पैन कार्ड",
                "name_english": "PAN Card",
                "is_mandatory": True,
                "instructions": "Clear photo of PAN card"
            },
            {
                "name": "पासपोर्ट",
                "name_english": "Passport",
                "is_mandatory": False,
                "instructions": "First page with photo and personal details"
            },
            {
                "name": "मतदाता पहचान पत्र",
                "name_english": "Voter ID",
                "is_mandatory": False,
                "instructions": "Clear photo of both sides"
            },
            {
                "name": "ड्राइविंग लाइसेंस",
                "name_english": "Driving License",
                "is_mandatory": False,
                "instructions": "Clear photo of both sides"
            }
        ]
    },
    DocumentCategory.EDUCATIONAL: {
        "name": "शैक्षणिक प्रमाण पत्र",
        "name_english": "Educational Certificates",
        "description": "Academic qualifications and certificates",
        "types": [
            {
                "name": "10वीं की मार्कशीट",
                "name_english": "10th Marksheet",
                "is_mandatory": True,
                "instructions": "Original marksheet or certified copy"
            },
            {
                "name": "12वीं की मार्कशीट",
                "name_english": "12th Marksheet",
                "is_mandatory": True,
                "instructions": "Original marksheet or certified copy"
            },
            {
                "name": "स्नातक की डिग्री",
                "name_english": "Graduation Degree",
                "is_mandatory": False,
                "instructions": "Degree certificate and final year marksheet"
            },
            {
                "name": "स्नातकोत्तर की डिग्री",
                "name_english": "Post Graduation Degree",
                "is_mandatory": False,
                "instructions": "Degree certificate and final year marksheet"
            },
            {
                "name": "डिप्लोमा सर्टिफिकेट",
                "name_english": "Diploma Certificate",
                "is_mandatory": False,
                "instructions": "Original diploma certificate"
            },
            {
                "name": "तकनीकी योग्यता प्रमाण पत्र",
                "name_english": "Technical Qualification Certificate",
                "is_mandatory": False,
                "instructions": "Relevant technical certifications"
            }
        ]
    },
    DocumentCategory.ADDRESS_PROOF: {
        "name": "पता प्रमाण",
        "name_english": "Address Proof",
        "description": "Documents to verify your current address",
        "types": [
            {
                "name": "राशन कार्ड",
                "name_english": "Ration Card",
                "is_mandatory": False,
                "instructions": "Clear photo showing name and address"
            },
            {
                "name": "बिजली बिल",
                "name_english": "Electricity Bill",
                "is_mandatory": False,
                "instructions": "Latest bill not older than 3 months"
            },
            {
                "name": "पानी का बिल",
                "name_english": "Water Bill",
                "is_mandatory": False,
                "instructions": "Latest bill not older than 3 months"
            },
            {
                "name": "बैंक स्टेटमेंट",
                "name_english": "Bank Statement",
                "is_mandatory": False,
                "instructions": "Latest statement not older than 3 months"
            },
            {
                "name": "टेलीफोन बिल",
                "name_english": "Telephone Bill",
                "is_mandatory": False,
                "instructions": "Latest bill not older than 3 months"
            },
            {
                "name": "निवास प्रमाण पत्र",
                "name_english": "Residence Certificate",
                "is_mandatory": False,
                "instructions": "Government issued residence certificate"
            }
        ]
    },
    DocumentCategory.PROFESSIONAL: {
        "name": "व्यावसायिक दस्तावेज",
        "name_english": "Professional Documents",
        "description": "Employment and work experience related documents",
        "types": [
            {
                "name": "नियुक्ति पत्र",
                "name_english": "Appointment Letter",
                "is_mandatory": False,
                "instructions": "Current job appointment letter"
            },
            {
                "name": "अनुभव प्रमाण पत्र",
                "name_english": "Experience Certificate",
                "is_mandatory": False,
                "instructions": "Previous employment experience certificates"
            },
            {
                "name": "वेतन प्रमाण पत्र",
                "name_english": "Salary Certificate",
                "is_mandatory": False,
                "instructions": "Latest salary certificate from employer"
            },
            {
                "name": "सेवा प्रमाण पत्र",
                "name_english": "Service Certificate",
                "is_mandatory": False,
                "instructions": "Government service certificate if applicable"
            }
        ]
    },
    DocumentCategory.CASTE_CATEGORY: {
        "name": "जाति/श्रेणी प्रमाण पत्र",
        "name_english": "Caste/Category Certificates",
        "description": "Caste, category and reservation related documents",
        "types": [
            {
                "name": "जाति प्रमाण पत्र",
                "name_english": "Caste Certificate",
                "is_mandatory": False,
                "instructions": "Valid caste certificate from competent authority"
            },
            {
                "name": "ईडब्ल्यूएस प्रमाण पत्र",
                "name_english": "EWS Certificate",
                "is_mandatory": False,
                "instructions": "Economically Weaker Section certificate"
            },
            {
                "name": "ओबीसी प्रमाण पत्र",
                "name_english": "OBC Certificate",
                "is_mandatory": False,
                "instructions": "Other Backward Class certificate"
            },
            {
                "name": "एससी/एसटी प्रमाण पत्र",
                "name_english": "SC/ST Certificate",
                "is_mandatory": False,
                "instructions": "Scheduled Caste/Scheduled Tribe certificate"
            }
        ]
    },
    DocumentCategory.INCOME_PROOF: {
        "name": "आय प्रमाण",
        "name_english": "Income Proof",
        "description": "Documents to verify income and financial status",
        "types": [
            {
                "name": "वेतन पर्ची",
                "name_english": "Salary Slip",
                "is_mandatory": False,
                "instructions": "Latest 3 months salary slips"
            },
            {
                "name": "आय प्रमाण पत्र",
                "name_english": "Income Certificate",
                "is_mandatory": False,
                "instructions": "Government issued income certificate"
            },
            {
                "name": "आयकर रिटर्न",
                "name_english": "Income Tax Return",
                "is_mandatory": False,
                "instructions": "Latest ITR acknowledgment"
            },
            {
                "name": "बैंक स्टेटमेंट (आय सत्यापन)",
                "name_english": "Bank Statement (Income Verification)",
                "is_mandatory": False,
                "instructions": "6 months bank statement for income verification"
            }
        ]
    },
    DocumentCategory.MEDICAL: {
        "name": "चिकित्सा दस्तावेज",
        "name_english": "Medical Documents",
        "description": "Health and medical related certificates",
        "types": [
            {
                "name": "चिकित्सा प्रमाण पत्र",
                "name_english": "Medical Certificate",
                "is_mandatory": False,
                "instructions": "Medical fitness certificate from registered doctor"
            },
            {
                "name": "विकलांगता प्रमाण पत्र",
                "name_english": "Disability Certificate",
                "is_mandatory": False,
                "instructions": "Disability certificate from competent medical authority"
            }
        ]
    },
    DocumentCategory.OTHER: {
        "name": "अन्य दस्तावेज",
        "name_english": "Other Documents",
        "description": "Miscellaneous documents",
        "types": [
            {
                "name": "चरित्र प्रमाण पत्र",
                "name_english": "Character Certificate",
                "is_mandatory": False,
                "instructions": "Character certificate from competent authority"
            },
            {
                "name": "शपथ पत्र",
                "name_english": "Affidavit",
                "is_mandatory": False,
                "instructions": "Relevant affidavit on stamp paper"
            }
        ]
    }
}