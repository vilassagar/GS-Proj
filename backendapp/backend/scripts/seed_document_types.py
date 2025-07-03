# scripts/seed_document_types.py
"""
Script to seed document types with field definitions
Run this after your database is set up
"""

import os
import sys
import json
import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL) # type: ignore
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_document_types():
    """Insert document types with field definitions"""
    
    # Document types data
    document_types = [
        # IDENTITY PROOF DOCUMENTS
        {
            'name': 'फोटो',
            'name_english': 'Photo',
            'is_mandatory': True,
            'category': 'identity_proof',
            'field_definitions': {                
            },
            'instructions': 'पासपोर्ट साइज फोटो अपलोड करा. फोटो स्पष्ट आणि अलीकडचा असावा.'
        },
        {
            'name': 'आधार कार्ड',
            'name_english': 'Aadhaar Card',
            'is_mandatory': True,
            'category': 'identity_proof', 
            'field_definitions': {
                'aadhaar_number': {
                    'type': 'text',
                    'label': 'Aadhaar Number',
                    'label_marathi': 'आधार नंबर',
                    'pattern': '^[0-9]{12}$',
                    'placeholder': '1234 5678 9012',
                    'required': True,
                    'validation_message': 'Please enter a valid 12-digit Aadhaar number'
                },
                'name_on_aadhaar': {
                    'type': 'text',
                    'label': 'Name on Aadhaar',
                    'label_marathi': 'आधार कार्डवरील नाव',
                    'required': True
                },
                'date_of_birth': {
                    'type': 'date',
                    'label': 'Date of Birth',
                    'label_marathi': 'जन्म तारीख',
                    'required': True
                },
                # 'address_on_aadhaar': {
                #     'type': 'textarea',
                #     'label': 'Address on Aadhaar',
                #     'label_marathi': 'आधार कार्डवरील पत्ता',
                #     'required': False
                # }
            },
            'instructions': 'आधार कार्डाची स्पष्ट प्रत अपलोड करा. सर्व माहिती वाचता येण्यासारखी असावी.'
        },
        {
            'name': 'पॅन कार्ड',
            'name_english': 'PAN Card', 
            'is_mandatory': True,
            'category': 'identity_proof',
            'field_definitions': {
                'pan_number': {
                    'type': 'text',
                    'label': 'PAN Number',
                    'label_marathi': 'पॅन नंबर',
                    'pattern': '^[A-Z]{5}[0-9]{4}[A-Z]{1}$',
                    'placeholder': 'ABCDE1234F',
                    'required': True,
                    'validation_message': 'Please enter a valid PAN number (e.g., ABCDE1234F)'
                },
                # 'name_on_pan': {
                #     'type': 'text',
                #     'label': 'Name on PAN',
                #     'label_marathi': 'पॅन कार्डवरील नाव',
                #     'required': True
                # },
                # 'father_name': {
                #     'type': 'text',
                #     'label': 'Father\'s Name',
                #     'label_marathi': 'वडिलांचे नाव',
                #     'required': True
                # },
                # 'date_of_birth_pan': {
                #     'type': 'date', 
                #     'label': 'Date of Birth (as per PAN)',
                #     'label_marathi': 'जन्म तारीख (पॅन प्रमाणे)',
                #     'required': True
                # }
            },
            'instructions': 'पॅन कार्डाची स्पष्ट प्रत अपलोड करा. पॅन नंबर स्पष्टपणे दिसत असावा.'
        },
        {
            'name': 'जातीचा दाखला',
            'name_english': 'Caste Certificate',
            'is_mandatory': False,
            'category': 'caste_category',
            'field_definitions': {
                'certificate_number': {
                    'type': 'text',
                    'label': 'Certificate Number',
                    'label_marathi': 'प्रमाणपत्र क्रमांक',
                    'required': True
                },
                'caste_name': {
                    'type': 'text',
                    'label': 'Caste Name',
                    'label_marathi': 'जातीचे नाव',
                    'required': True
                },
                'category': {
                    'type': 'select',
                    'label': 'Category',
                    'label_marathi': 'प्रवर्ग',
                    'options': ['ST', 'SC', 'VJNT', 'NT', 'OBC', 'SBC'],
                    'required': True
                },
                'issued_date': {
                    'type': 'date',
                    'label': 'Issue Date',
                    'label_marathi': 'जारी केल्याची तारीख',
                    'required': True
                },
                'issuing_authority': {
                    'type': 'text',
                    'label': 'Issuing Authority',
                    'label_marathi': 'जारीकर्ता प्राधिकरण',
                    'required': True
                }
            },
            'instructions': 'सक्षम प्राधिकाऱ्याकडून जारी केलेला जातीचा दाखला अपलोड करा.'
        },
        {
            'name': 'दहावी गुणपत्रक',
            'name_english': 'SSC Marklist',
            'is_mandatory': True,
            'category': 'educational',
            'field_definitions': {
                'seat_number': {
                    'type': 'text',
                    'label': 'Seat Number',
                    'label_marathi': 'आसन क्रमांक',
                    'required': True
                },
                'passing_year': {
                    'type': 'number',
                    'label': 'Passing Year',
                    'label_marathi': 'उत्तीर्ण वर्ष',
                    'min': 1980,
                    'max': 2025,
                    'required': True
                },
                'percentage': {
                    'type': 'number',
                    'label': 'Percentage',
                    'label_marathi': 'टक्केवारी',
                    'min': 0,
                    'max': 100,
                    'step': 0.01,
                    'required': True
                },
                'board_name': {
                    'type': 'select',
                    'label': 'Board Name',
                    'label_marathi': 'मंडळाचे नाव',
                    'options': ['Maharashtra State Board', 'CBSE', 'ICSE', 'Other'],
                    'required': True
                }
            },
            'instructions': 'दहावीची मूळ गुणपत्रिका अपलोड करा.'
        },
        {
            'name': 'पगार बॅंक खाते पासबुक',
            'name_english': 'Salary Account Bank Passbook',
            'is_mandatory': False,
            'category': 'professional',
            'field_definitions': {
                'account_number': {
                    'type': 'text',
                    'label': 'Account Number',
                    'label_marathi': 'खाते क्रमांक',
                    'required': True
                },
                'bank_name': {
                    'type': 'text',
                    'label': 'Bank Name',
                    'label_marathi': 'बँकेचे नाव',
                    'required': True
                },
                'branch_name': {
                    'type': 'text',
                    'label': 'Branch Name',
                    'label_marathi': 'शाखेचे नाव',
                    'required': True
                },
                'ifsc_code': {
                    'type': 'text',
                    'label': 'IFSC Code',
                    'label_marathi': 'IFSC कोड',
                    'pattern': '^[A-Z]{4}0[A-Z0-9]{6}$',
                    'required': True
                },
                'account_holder_name': {
                    'type': 'text',
                    'label': 'Account Holder Name',
                    'label_marathi': 'खातेधारकाचे नाव',
                    'required': True
                }
            },
            'instructions': 'पगार खात्याच्या पासबुकचे पहिले पान अपलोड करा.'
        }
    ]
    
    # Insert into database
    session = SessionLocal()
    try:
        for i, doc_type in enumerate(document_types, 1):
            # Check if document type already exists
            existing = session.execute(
                text("SELECT id FROM document_types WHERE name_english = :name_english"), 
                {"name_english": doc_type['name_english']}
            ).first()
            
            if not existing:
                insert_query = text("""
                    INSERT INTO document_types 
                    (name, name_english, is_mandatory, category, field_definitions, instructions, created_at, is_active)
                    VALUES 
                    (:name, :name_english, :is_mandatory, :category, :field_definitions, :instructions, :created_at, :is_active)
                """)
                
                session.execute(insert_query, {
                    'name': doc_type['name'],
                    'name_english': doc_type['name_english'],
                    'is_mandatory': doc_type['is_mandatory'],
                    'category': doc_type['category'],
                    'field_definitions': json.dumps(doc_type['field_definitions']),
                    'instructions': doc_type['instructions'],
                    'created_at': datetime.datetime.utcnow(),
                    'is_active': True
                })
                
                print(f"✅ Inserted: {doc_type['name_english']}")
            else:
                print(f"⚠️  Already exists: {doc_type['name_english']}")
        
        session.commit()
        print(f"\n🎉 Successfully seeded {len(document_types)} document types!")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error seeding document types: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    print("🌱 Seeding document types...")
    seed_document_types()