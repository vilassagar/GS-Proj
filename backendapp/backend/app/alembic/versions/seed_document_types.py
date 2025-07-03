# app/alembic/versions/seed_document_types.py
"""Add comprehensive document types with field definitions

Revision ID: seed_document_types
Revises: existing_migration_id
Create Date: 2025-07-03

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Boolean, DateTime, JSON, Text
import datetime
import json

def upgrade():
    # Create document_types table reference
    document_types_table = table('document_types',
        column('id', Integer),
        column('name', String),
        column('name_english', String),
        column('is_mandatory', Boolean),
        column('field_definitions', JSON),
        column('category', String),
        column('instructions', Text),
        column('created_by', Integer),
        column('updated_by', Integer),
        column('created_at', DateTime),
        column('updated_at', DateTime),
        column('is_active', Boolean)
    )

    # Document types data with field definitions
    document_types_data = [
        # IDENTITY PROOF DOCUMENTS
        {
            'id': 1,
            'name': 'फोटो',
            'name_english': 'Photo',
            'is_mandatory': True,
            'category': 'identity_proof',
            'field_definitions': json.dumps({
                'photo_type': {
                    'type': 'select',
                    'label': 'Photo Type',
                    'label_marathi': 'फोटो प्रकार',
                    'options': ['Passport Size', 'Official'],
                    'required': True
                },
                'background_color': {
                    'type': 'select',
                    'label': 'Background Color',
                    'label_marathi': 'पार्श्वभूमी रंग',
                    'options': ['White', 'Blue', 'Red'],
                    'required': False
                }
            }),
            'instructions': 'पासपोर्ट साइज फोटो अपलोड करा. फोटो स्पष्ट आणि अलीकडचा असावा.',
            'created_by': None,
            'updated_by': None,
            'created_at': datetime.datetime.utcnow(),
            'updated_at': None,
            'is_active': True
        },
        {
            'id': 2,
            'name': 'आधार कार्ड',
            'name_english': 'Aadhaar Card',
            'is_mandatory': True,
            'category': 'identity_proof',
            'field_definitions': json.dumps({
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
                'address_on_aadhaar': {
                    'type': 'textarea',
                    'label': 'Address on Aadhaar',
                    'label_marathi': 'आधार कार्डवरील पत्ता',
                    'required': False
                }
            }),
            'instructions': 'आधार कार्डाची स्पष्ट प्रत अपलोड करा. सर्व माहिती वाचता येण्यासारखी असावी.',
            'created_by': None,
            'updated_by': None,
            'created_at': datetime.datetime.utcnow(),
            'updated_at': None,
            'is_active': True
        },
        {
            'id': 3,
            'name': 'पॅन कार्ड',
            'name_english': 'PAN Card',
            'is_mandatory': True,
            'category': 'identity_proof',
            'field_definitions': json.dumps({
                'pan_number': {
                    'type': 'text',
                    'label': 'PAN Number',
                    'label_marathi': 'पॅन नंबर',
                    'pattern': '^[A-Z]{5}[0-9]{4}[A-Z]{1}$',
                    'placeholder': 'ABCDE1234F',
                    'required': True,
                    'validation_message': 'Please enter a valid PAN number (e.g., ABCDE1234F)'
                },
                'name_on_pan': {
                    'type': 'text',
                    'label': 'Name on PAN',
                    'label_marathi': 'पॅन कार्डवरील नाव',
                    'required': True
                },
                'father_name': {
                    'type': 'text',
                    'label': 'Father\'s Name',
                    'label_marathi': 'वडिलांचे नाव',
                    'required': True
                },
                'date_of_birth_pan': {
                    'type': 'date',
                    'label': 'Date of Birth (as per PAN)',
                    'label_marathi': 'जन्म तारीख (पॅन प्रमाणे)',
                    'required': True
                }
            }),
            'instructions': 'पॅन कार्डाची स्पष्ट प्रत अपलोड करा. पॅन नंबर स्पष्टपणे दिसत असावा.',
            'created_by': None,
            'updated_by': None,
            'created_at': datetime.datetime.utcnow(),
            'updated_at': None,
            'is_active': True
        },
        {
            'id': 4,
            'name': 'रेशनकार्ड प्रत',
            'name_english': 'Ration Card Copy',
            'is_mandatory': False,
            'category': 'address_proof',
            'field_definitions': json.dumps({
                'ration_card_number': {
                    'type': 'text',
                    'label': 'Ration Card Number',
                    'label_marathi': 'रेशन कार्ड नंबर',
                    'required': True
                },
                'card_type': {
                    'type': 'select',
                    'label': 'Card Type',
                    'label_marathi': 'कार्ड प्रकार',
                    'options': ['APL', 'BPL', 'Antyodaya'],
                    'required': True
                },
                'head_of_family': {
                    'type': 'text',
                    'label': 'Head of Family',
                    'label_marathi': 'कुटुंब प्रमुख',
                    'required': True
                }
            }),
            'instructions': 'रेशन कार्डाची संपूर्ण प्रत अपलोड करा.',
            'created_by': None,
            'updated_by': None,
            'created_at': datetime.datetime.utcnow(),
            'updated_at': None,
            'is_active': True
        },
        {
            'id': 5,
            'name': 'जन्मदाखला',
            'name_english': 'Birth Certificate',
            'is_mandatory': True,
            'category': 'identity_proof',
            'field_definitions': json.dumps({
                'certificate_number': {
                    'type': 'text',
                    'label': 'Certificate Number',
                    'label_marathi': 'प्रमाणपत्र क्रमांक',
                    'required': True
                },
                'registration_number': {
                    'type': 'text',
                    'label': 'Registration Number',
                    'label_marathi': 'नोंदणी क्रमांक',
                    'required': True
                },
                'place_of_birth': {
                    'type': 'text',
                    'label': 'Place of Birth',
                    'label_marathi': 'जन्मस्थान',
                    'required': True
                },
                'date_of_birth_cert': {
                    'type': 'date',
                    'label': 'Date of Birth',
                    'label_marathi': 'जन्म तारीख',
                    'required': True
                }
            }),
            'instructions': 'अधिकृत जन्म दाखला अपलोड करा.',
            'created_by': None,
            'updated_by': None,
            'created_at': datetime.datetime.utcnow(),
            'updated_at': None,
            'is_active': True
        },
        {
            'id': 6,
            'name': 'जातीचा दाखला',
            'name_english': 'Caste Certificate',
            'is_mandatory': False,
            'category': 'caste_category',
            'field_definitions': json.dumps({
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
            }),
            'instructions': 'सक्षम प्राधिकाऱ्याकडून जारी केलेला जातीचा दाखला अपलोड करा.',
            'created_by': None,
            'updated_by': None,
            'created_at': datetime.datetime.utcnow(),
            'updated_at': None,
            'is_active': True
        },

        # EDUCATIONAL DOCUMENTS
        {
            'id': 9,
            'name': 'दहावी गुणपत्रक',
            'name_english': 'SSC Marklist',
            'is_mandatory': True,
            'category': 'educational',
            'field_definitions': json.dumps({
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
                    'max': new Date().getFullYear(),
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
            }),
            'instructions': 'दहावीची मूळ गुणपत्रिका अपलोड करा.',
            'created_by': None,
            'updated_by': None,
            'created_at': datetime.datetime.utcnow(),
            'updated_at': None,
            'is_active': True
        },
        {
            'id': 10,
            'name': 'दहावी प्रमाणपत्र',
            'name_english': 'SSC Certificate',
            'is_mandatory': True,
            'category': 'educational',
            'field_definitions': json.dumps({
                'certificate_number': {
                    'type': 'text',
                    'label': 'Certificate Number',
                    'label_marathi': 'प्रमाणपत्र क्रमांक',
                    'required': True
                },
                'name_on_certificate': {
                    'type': 'text',
                    'label': 'Name on Certificate',
                    'label_marathi': 'प्रमाणपत्रावरील नाव',
                    'required': True
                },
                'school_name': {
                    'type': 'text',
                    'label': 'School Name',
                    'label_marathi': 'शाळेचे नाव',
                    'required': True
                }
            }),
            'instructions': 'दहावीचे मूळ प्रमाणपत्र अपलोड करा.',
            'created_by': None,
            'updated_by': None,
            'created_at': datetime.datetime.utcnow(),
            'updated_at': None,
            'is_active': True
        },

        # PROFESSIONAL DOCUMENTS
        {
            'id': 25,
            'name': 'पगार बॅंक खाते पासबुक',
            'name_english': 'Salary Account Bank Passbook',
            'is_mandatory': False,
            'category': 'professional',
            'field_definitions': json.dumps({
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
            }),
            'instructions': 'पगार खात्याच्या पासबुकचे पहिले पान अपलोड करा.',
            'created_by': None,
            'updated_by': None,
            'created_at': datetime.datetime.utcnow(),
            'updated_at': None,
            'is_active': True
        },
        {
            'id': 38,
            'name': 'सेवापुस्तक प्रत',
            'name_english': 'Service Book Copy',
            'is_mandatory': False,
            'category': 'professional',
            'field_definitions': json.dumps({
                'employee_id': {
                    'type': 'text',
                    'label': 'Employee ID',
                    'label_marathi': 'कर्मचारी क्रमांक',
                    'required': True
                },
                'designation': {
                    'type': 'text',
                    'label': 'Designation',
                    'label_marathi': 'पदनाम',
                    'required': True
                },
                'office_name': {
                    'type': 'text',
                    'label': 'Office Name',
                    'label_marathi': 'कार्यालयाचे नाव',
                    'required': True
                },
                'date_of_joining': {
                    'type': 'date',
                    'label': 'Date of Joining',
                    'label_marathi': 'नियुक्तीची तारीख',
                    'required': True
                }
            }),
            'instructions': 'सेवापुस्तकाच्या संबंधित पानांची प्रत अपलोड करा.',
            'created_by': None,
            'updated_by': None,
            'created_at': datetime.datetime.utcnow(),
            'updated_at': None,
            'is_active': True
        },

        # INCOME PROOF
        {
            'id': 42,
            'name': 'दिव्यांग प्रमाणपत्र',
            'name_english': 'Handicapped Certificate',
            'is_mandatory': False,
            'category': 'medical',
            'field_definitions': json.dumps({
                'certificate_number': {
                    'type': 'text',
                    'label': 'Certificate Number',
                    'label_marathi': 'प्रमाणपत्र क्रमांक',
                    'required': True
                },
                'disability_type': {
                    'type': 'select',
                    'label': 'Type of Disability',
                    'label_marathi': 'अपंगत्वाचा प्रकार',
                    'options': ['Physical', 'Visual', 'Hearing', 'Mental', 'Multiple'],
                    'required': True
                },
                'disability_percentage': {
                    'type': 'number',
                    'label': 'Disability Percentage',
                    'label_marathi': 'अपंगत्वाची टक्केवारी',
                    'min': 1,
                    'max': 100,
                    'required': True
                },
                'issued_date': {
                    'type': 'date',
                    'label': 'Issue Date',
                    'label_marathi': 'जारी केल्याची तारीख',
                    'required': True
                },
                'valid_until': {
                    'type': 'date',
                    'label': 'Valid Until',
                    'label_marathi': 'वैधता',
                    'required': False
                }
            }),
            'instructions': 'सक्षम वैद्यकीय प्राधिकाऱ्याकडून जारी केलेले दिव्यांग प्रमाणपत्र अपलोड करा.',
            'created_by': None,
            'updated_by': None,
            'created_at': datetime.datetime.utcnow(),
            'updated_at': None,
            'is_active': True
        }
    ]

    # Insert document types
    for doc_data in document_types_data:
        op.bulk_insert(document_types_table, [doc_data])

def downgrade():
    # Delete the inserted document types
    op.execute('DELETE FROM document_types WHERE id IN (1,2,3,4,5,6,9,10,25,38,42)')