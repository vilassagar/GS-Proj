# seed_dynamic_documents.py
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.models.documents import DocumentType

def create_dynamic_document_types():
    db = SessionLocal()
    
    # Aadhar Card
    aadhar_fields = {
        "aadhar_number": {
            "type": "TEXT",
            "label": "आधार क्रमांक",
            "label_english": "Aadhar Number",
            "required": True,
            "validation": {"pattern": "^[0-9]{4}-[0-9]{4}-[0-9]{4}$"},
            "placeholder": "1234-5678-9012",
            "help_text": "12 digit Aadhar number with dashes"
        },
        "full_name": {
            "type": "TEXT",
            "label": "पूर्ण नाव",
            "label_english": "Full Name as per Aadhar",
            "required": True,
            "placeholder": "Enter full name",
            "help_text": "Name should match exactly as on Aadhar card"
        },
        "date_of_birth": {
            "type": "DATE",
            "label": "जन्म दिनांक",
            "label_english": "Date of Birth",
            "required": True,
            "help_text": "Date of birth as per Aadhar card"
        }
    }
    
    # Update or create Aadhar card document type
    aadhar_doc = db.query(DocumentType).filter(DocumentType.name == "आधार कार्ड").first()
    if aadhar_doc:
        aadhar_doc.field_definitions = aadhar_fields
        aadhar_doc.category = "IDENTITY"
        aadhar_doc.instructions = "कृपया आधार कार्डची स्पष्ट प्रत अपलोड करा आणि सर्व तपशील भरा"
    
    # PAN Card
    pan_fields = {
        "pan_number": {
            "type": "TEXT",
            "label": "पॅन क्रमांक",
            "label_english": "PAN Number",
            "required": True,
            "validation": {"pattern": "^[A-Z]{5}[0-9]{4}[A-Z]{1}$"},
            "placeholder": "ABCDE1234F",
            "help_text": "10 character PAN number in capital letters"
        },
        "full_name": {
            "type": "TEXT",
            "label": "पूर्ण नाव",
            "label_english": "Full Name as per PAN",
            "required": True,
            "placeholder": "Enter full name",
            "help_text": "Name should match exactly as on PAN card"
        },
        "father_name": {
            "type": "TEXT",
            "label": "वडिलांचे नाव",
            "label_english": "Father's Name",
            "required": True,
            "placeholder": "Enter father's name"
        }
    }
    
    pan_doc = db.query(DocumentType).filter(DocumentType.name == "पॅन कार्ड").first()
    if pan_doc:
        pan_doc.field_definitions = pan_fields
        pan_doc.category = "IDENTITY"
        pan_doc.instructions = "कृपया पॅन कार्डची स्पष्ट प्रत अपलोड करा"
    
    # SSC Certificate
    ssc_cert_fields = {
        "student_name": {
            "type": "TEXT",
            "label": "विद्यार्थ्याचे नाव",
            "label_english": "Student Name",
            "required": True,
            "placeholder": "Enter student name"
        },
        "passing_year": {
            "type": "YEAR",
            "label": "उत्तीर्ण वर्ष",
            "label_english": "Passing Year",
            "required": True,
            "validation": {"min": 1990, "max": 2030}
        },
        "board_name": {
            "type": "SELECT",
            "label": "बोर्ड",
            "label_english": "Board",
            "required": True,
            "options": [
                "Maharashtra State Board",
                "CBSE",
                "ICSE",
                "Other State Board"
            ]
        },
        "school_name": {
            "type": "TEXT",
            "label": "शाळेचे नाव",
            "label_english": "School Name",
            "required": True,
            "placeholder": "Enter school name"
        },
        "seat_number": {
            "type": "TEXT",
            "label": "आसन क्रमांक",
            "label_english": "Seat Number",
            "required": True,
            "placeholder": "Enter seat number"
        }
    }
    
    ssc_cert_doc = db.query(DocumentType).filter(DocumentType.name == "दहावी प्रमाणपत्र").first()
    if ssc_cert_doc:
        ssc_cert_doc.field_definitions = ssc_cert_fields
        ssc_cert_doc.category = "EDUCATION"
        ssc_cert_doc.instructions = "कृपया दहावीचे मूळ प्रमाणपत्र अपलोड करा"
    
    # SSC Marksheet
    ssc_marks_fields = {
        "student_name": {
            "type": "TEXT",
            "label": "विद्यार्थ्याचे नाव",
            "label_english": "Student Name",
            "required": True
        },
        "passing_year": {
            "type": "YEAR",
            "label": "उत्तीर्ण वर्ष",
            "label_english": "Passing Year",
            "required": True,
            "validation": {"min": 1990, "max": 2030}
        },
        "total_marks": {
            "type": "NUMBER",
            "label": "एकूण गुण",
            "label_english": "Total Marks",
            "required": True,
            "validation": {"min": 0, "max": 1000}
        },
        "obtained_marks": {
            "type": "NUMBER",
            "label": "मिळालेले गुण",
            "label_english": "Obtained Marks",
            "required": True,
            "validation": {"min": 0, "max": 1000}
        },
        "percentage": {
            "type": "PERCENTAGE",
            "label": "टक्केवारी",
            "label_english": "Percentage",
            "required": True,
            "validation": {"min": 0, "max": 100}
        },
        "grade": {
            "type": "SELECT",
            "label": "श्रेणी",
            "label_english": "Grade",
            "required": False,
            "options": ["A+", "A", "B+", "B", "C+", "C", "D", "First Class", "Second Class", "Pass Class"]
        }
    }
    
    ssc_marks_doc = db.query(DocumentType).filter(DocumentType.name == "दहावी गुणपत्रक").first()
    if ssc_marks_doc:
        ssc_marks_doc.field_definitions = ssc_marks_fields
        ssc_marks_doc.category = "EDUCATION"
        ssc_marks_doc.instructions = "कृपया दहावीचे मूळ गुणपत्रक अपलोड करा"
    
    # Graduate Degree Certificate
    degree_cert_fields = {
        "student_name": {
            "type": "TEXT",
            "label": "विद्यार्थ्याचे नाव",
            "label_english": "Student Name",
            "required": True
        },
        "degree_name": {
            "type": "TEXT",
            "label": "पदवीचे नाव",
            "label_english": "Degree Name",
            "required": True,
            "placeholder": "B.A., B.Com, B.Sc, etc."
        },
        "specialization": {
            "type": "TEXT",
            "label": "विशेषीकरण",
            "label_english": "Specialization/Subject",
            "required": False,
            "placeholder": "Economics, Physics, etc."
        },
        "university_name": {
            "type": "TEXT",
            "label": "विद्यापीठाचे नाव",
            "label_english": "University Name",
            "required": True,
            "placeholder": "Enter university name"
        },
        "college_name": {
            "type": "TEXT",
            "label": "महाविद्यालयाचे नाव",
            "label_english": "College Name",
            "required": True,
            "placeholder": "Enter college name"
        },
        "passing_year": {
            "type": "YEAR",
            "label": "उत्तीर्ण वर्ष",
            "label_english": "Passing Year",
            "required": True,
            "validation": {"min": 1990, "max": 2030}
        },
        "class_grade": {
            "type": "SELECT",
            "label": "वर्ग/श्रेणी",
            "label_english": "Class/Grade",
            "required": False,
            "options": ["First Class with Distinction", "First Class", "Second Class", "Third Class", "Pass"]
        }
    }
    
    degree_cert_doc = db.query(DocumentType).filter(DocumentType.name == "पदवी प्रमाणपत्र").first()
    if degree_cert_doc:
        degree_cert_doc.field_definitions = degree_cert_fields
        degree_cert_doc.category = "EDUCATION"
        degree_cert_doc.instructions = "कृपया पदवीचे मूळ प्रमाणपत्र अपलोड करा"
    
    # Selection Order (Appointment Order)
    selection_order_fields = {
        "employee_name": {
            "type": "TEXT",
            "label": "कर्मचार्‍याचे नाव",
            "label_english": "Employee Name",
            "required": True
        },
        "post_name": {
            "type": "TEXT",
            "label": "पदाचे नाव",
            "label_english": "Post Name",
            "required": True,
            "placeholder": "ग्रामसेवक, सहायक ग्रामसेवक"
        },
        "appointment_date": {
            "type": "DATE",
            "label": "नेमणूक दिनांक",
            "label_english": "Appointment Date",
            "required": True
        },
        "order_number": {
            "type": "TEXT",
            "label": "आदेश क्रमांक",
            "label_english": "Order Number",
            "required": True,
            "placeholder": "Enter order number"
        },
        "order_date": {
            "type": "DATE",
            "label": "आदेश दिनांक",
            "label_english": "Order Date",
            "required": True
        },
        "issuing_authority": {
            "type": "TEXT",
            "label": "जारीकर्ता प्राधिकरण",
            "label_english": "Issuing Authority",
            "required": True,
            "placeholder": "CEO Zilla Panchayat, etc."
        },
        "district": {
            "type": "TEXT",
            "label": "जिल्हा",
            "label_english": "District",
            "required": True
        },
        "block_panchayat": {
            "type": "TEXT",
            "label": "पंचायत समिती",
            "label_english": "Block/Panchayat Samiti",
            "required": True
        }
    }
    
    selection_order_doc = db.query(DocumentType).filter(DocumentType.name == "नेमणुक आदेश").first()
    if selection_order_doc:
        selection_order_doc.field_definitions = selection_order_fields
        selection_order_doc.category = "SERVICE"
        selection_order_doc.instructions = "कृपया नेमणुकीचा मूळ आदेश अपलोड करा"
    
    # Bank Passbook
    bank_passbook_fields = {
        "account_holder_name": {
            "type": "TEXT",
            "label": "खातेधारकाचे नाव",
            "label_english": "Account Holder Name",
            "required": True
        },
        "account_number": {
            "type": "TEXT",
            "label": "खाते क्रमांक",
            "label_english": "Account Number",
            "required": True,
            "placeholder": "Enter bank account number"
        },
        "bank_name": {
            "type": "TEXT",
            "label": "बँकेचे नाव",
            "label_english": "Bank Name",
            "required": True,
            "placeholder": "State Bank of India, etc."
        },
        "branch_name": {
            "type": "TEXT",
            "label": "शाखेचे नाव",
            "label_english": "Branch Name",
            "required": True,
            "placeholder": "Enter branch name"
        },
        "ifsc_code": {
            "type": "TEXT",
            "label": "IFSC कोड",
            "label_english": "IFSC Code",
            "required": True,
            "validation": {"pattern": "^[A-Z]{4}0[A-Z0-9]{6}$"},
            "placeholder": "SBIN0001234"
        },
        "account_type": {
            "type": "SELECT",
            "label": "खाते प्रकार",
            "label_english": "Account Type",
            "required": True,
            "options": ["Savings", "Current", "Salary"]
        }
    }
    
    bank_passbook_doc = db.query(DocumentType).filter(DocumentType.name == "पगार बँक खाते पासबुक").first()
    if bank_passbook_doc:
        bank_passbook_doc.field_definitions = bank_passbook_fields
        bank_passbook_doc.category = "FINANCIAL"
        bank_passbook_doc.instructions = "कृपया बँक पासबुकचे पहिले पान अपलोड करा"
    
    # Caste Certificate
    caste_cert_fields = {
        "applicant_name": {
            "type": "TEXT",
            "label": "अर्जदाराचे नाव",
            "label_english": "Applicant Name",
            "required": True
        },
        "caste": {
            "type": "TEXT",
            "label": "जात",
            "label_english": "Caste",
            "required": True,
            "placeholder": "Enter caste name"
        },
        "category": {
            "type": "SELECT",
            "label": "वर्ग",
            "label_english": "Category",
            "required": True,
            "options": ["SC", "ST", "OBC", "VJNT", "SBC", "Other"]
        },
        "father_name": {
            "type": "TEXT",
            "label": "वडिलांचे नाव",
            "label_english": "Father's Name",
            "required": True
        },
        "certificate_number": {
            "type": "TEXT",
            "label": "प्रमाणपत्र क्रमांक",
            "label_english": "Certificate Number",
            "required": True,
            "placeholder": "Enter certificate number"
        },
        "issue_date": {
            "type": "DATE",
            "label": "जारी दिनांक",
            "label_english": "Issue Date",
            "required": True
        },
        "issuing_authority": {
            "type": "TEXT",
            "label": "जारीकर्ता प्राधिकरण",
            "label_english": "Issuing Authority",
            "required": True,
            "placeholder": "Tehsildar, SDO, etc."
        },
        "validity": {
            "type": "SELECT",
            "label": "वैधता",
            "label_english": "Validity",
            "required": False,
            "options": ["Permanent", "3 Years", "5 Years", "10 Years"]
        }
    }
    
    caste_cert_doc = db.query(DocumentType).filter(DocumentType.name == "जातीचा दाखला").first()
    if caste_cert_doc:
        caste_cert_doc.field_definitions = caste_cert_fields
        caste_cert_doc.category = "CASTE"
        caste_cert_doc.instructions = "कृपया जातीच्या दाखल्याची मूळ प्रत अपलोड करा"
    
    db.commit()
    db.close()
    print("✅ Dynamic document types created successfully!")

if __name__ == "__main__":
    create_dynamic_document_types()