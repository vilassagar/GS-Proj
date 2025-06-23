#!/usr/bin/env python3
"""
Seed data script for GramSevak application
Run this after database migration to populate initial data
"""

import sys
import os
from datetime import datetime

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.config import SessionLocal, engine
from app.models.roles import Role
from app.models.users import User
from app.models.users_hierarchy import District, Block, GramPanchayat
from app.models.department import Department
from app.models.gr_yojana import Yojana
from app.models.documents import DocumentType
from app.models.enums.user_designation import UserDesignation
from app.models.enums.approval_status import ApprovalStatus


def create_seed_data():
    """Create initial seed data for the application"""
    db: Session = SessionLocal()
    
    try:
        print("🌱 Starting seed data creation...")
        
        # 1. Create Roles
        print("📝 Creating roles...")
        roles_data = [
            {"id": 1, "name": "superAdmin", "description": "Super Administrator with full access"},
            {"id": 2, "name": "districtAdmin", "description": "District Administrator"},
            {"id": 3, "name": "blockAdmin", "description": "Block Administrator"},
            {"id": 4, "name": "gramSevak", "description": "Gram Sevak/Village Worker"},
        ]
        
        for role_data in roles_data:
            existing_role = db.query(Role).filter(Role.name == role_data["name"]).first()
            if not existing_role:
                role = Role(**role_data)
                db.add(role)
                print(f"  ✅ Created role: {role_data['name']}")
            else:
                print(f"  ⏭️  Role already exists: {role_data['name']}")
        
        # 2. Create Departments
        print("🏢 Creating departments...")
        departments_data = [
            {"name": "ग्रामीण विकास विभाग"},  # Rural Development Department
            {"name": "महिला आणि बाल विकास"},   # Women and Child Development
            {"name": "शिक्षण विभाग"},          # Education Department
            {"name": "आरोग्य विभाग"},          # Health Department
            {"name": "कृषी विभाग"},            # Agriculture Department
        ]
        
        for dept_data in departments_data:
            existing_dept = db.query(Department).filter(Department.name == dept_data["name"]).first()
            if not existing_dept:
                department = Department(**dept_data)
                db.add(department)
                print(f"  ✅ Created department: {dept_data['name']}")
            else:
                print(f"  ⏭️  Department already exists: {dept_data['name']}")
        
        # 3. Create Yojanas (Schemes)
        print("📋 Creating yojanas...")
        yojanas_data = [
            {"name": "महात्मा गांधी राष्ट्रीय ग्रामीण रोजगार हमी योजना"},  # MGNREGA
            {"name": "प्रधानमंत्री आवास योजना"},                        # PM Housing Scheme
            {"name": "स्वच्छ भारत मिशन"},                              # Clean India Mission
            {"name": "डिजिटल इंडिया योजना"},                           # Digital India
            {"name": "आयुष्मान भारत योजना"},                          # Ayushman Bharat
        ]
        
        for yojana_data in yojanas_data:
            existing_yojana = db.query(Yojana).filter(Yojana.name == yojana_data["name"]).first()
            if not existing_yojana:
                yojana = Yojana(**yojana_data)
                db.add(yojana)
                print(f"  ✅ Created yojana: {yojana_data['name']}")
            else:
                print(f"  ⏭️  Yojana already exists: {yojana_data['name']}")
        
        # 4. Create Document Types - Complete List with English Names
        print("📄 Creating document types...")
        document_types_data = [
            # Basic mandatory documents
            {"name": "फोटो", "name_english": "Photo", "is_mandatory": True},
            {"name": "आधार कार्ड", "name_english": "Adhar Card", "is_mandatory": True},
            {"name": "पॅन कार्ड", "name_english": "Pan Card", "is_mandatory": True},
            {"name": "रेशनकार्ड प्रत", "name_english": "Ration Card Copy", "is_mandatory": False},
            {"name": "जन्मदाखला", "name_english": "Birth Certificate", "is_mandatory": True},
            
            # Caste related documents
            {"name": "जातीचा दाखला", "name_english": "Caste Certificate", "is_mandatory": False},
            {"name": "जात पडताळणी प्रमाणपत्र", "name_english": "Cast Validation Certificate", "is_mandatory": False},
            
            # Travel document
            {"name": "पासपोर्ट", "name_english": "Passport", "is_mandatory": False},
            
            # Education documents - SSC
            {"name": "दहावी गुणपत्रक", "name_english": "SSC Marklist", "is_mandatory": True},
            {"name": "दहावी प्रमाणपत्र", "name_english": "SSC Certificate", "is_mandatory": True},
            
            # Education documents - HSC
            {"name": "बारावी गुणपत्रक", "name_english": "HSC Marklist", "is_mandatory": False},
            {"name": "बारावी प्रमाणपत्र", "name_english": "HSC Certificate", "is_mandatory": False},
            {"name": "शाळा सोडल्याचा दाखला/TC", "name_english": "Leaving Certificate/Transcript Certificate", "is_mandatory": False},
            
            # Diploma
            {"name": "पदविका गुणपत्रक", "name_english": "Diploma Marklist", "is_mandatory": False},
            {"name": "पदविका प्रमाणपत्र", "name_english": "Diploma Certificate", "is_mandatory": False},
            
            # Degree
            {"name": "पदवी गुणपत्रक", "name_english": "Degree Marklist", "is_mandatory": False},
            {"name": "पदवी प्रमाणपत्र", "name_english": "Degree Certificate", "is_mandatory": False},
            
            # Post Graduate
            {"name": "पदव्युत्तर गुणपत्रक", "name_english": "Post Graduate Marklist", "is_mandatory": False},
            {"name": "पदव्युत्तर प्रमाणपत्र", "name_english": "Post Graduate Certificate", "is_mandatory": False},
            
            # PhD
            {"name": "डॉक्टरेट गुणपत्रक", "name_english": "PhD Marklist", "is_mandatory": False},
            {"name": "डॉक्टरेट प्रमाणपत्र", "name_english": "PhD Certificate", "is_mandatory": False},
            
            # Computer Certificate
            {"name": "MS-CIT", "name_english": "MS-CIT Certificate", "is_mandatory": False},
            
            # Appointment related documents
            {"name": "नेमणुक परीक्षा हॉल तिकीट", "name_english": "Hall Ticket of Exam", "is_mandatory": False},
            {"name": "नेमणुक आदेश", "name_english": "Selection Order", "is_mandatory": True},
            {"name": "हजर अर्ज", "name_english": "Application of Presence", "is_mandatory": False},
            {"name": "पगार बँक खाते पासबुक", "name_english": "Salary Account Bank Passbook", "is_mandatory": True},
            {"name": "ओळखपत्र", "name_english": "Identity Card", "is_mandatory": True},
            
            # Service related orders
            {"name": "कायम केलेचा आदेश", "name_english": "Permenent Order", "is_mandatory": False},
            {"name": "सेवा परीक्षा उत्तीर्ण आदेश", "name_english": "Service Exam Passed Order", "is_mandatory": False},
            {"name": "स्थायित्व लाभाचा आदेश", "name_english": "Confirmation Order", "is_mandatory": False},
            
            # Assured Career Progression Scheme orders
            {"name": "12 वर्षे - सेवांतर्गत आश्वासित प्रगती योजना आदेश", "name_english": "12 Yrs-Sevantargat Ashwashit Pragati Yojana Benefit Order", "is_mandatory": False},
            {"name": "24 वर्षे - सेवांतर्गत आश्वासित प्रगती योजना आदेश", "name_english": "24 Yrs-Sevantargat Ashwashit Pragati Yojana Benefit Order", "is_mandatory": False},
            {"name": "10 वर्षे - सुधारित सेवांतर्गत आश्वासित प्रगती योजना आदेश", "name_english": "10 Yrs-Sudharit Sevantargat Ashwashit Pragati Yojana Benefit Order", "is_mandatory": False},
            {"name": "20 वर्षे - सुधारित सेवांतर्गत आश्वासित प्रगती योजना आदेश", "name_english": "20 Yrs-Sudharit Sevantargat Ashwashit Pragati Yojana Benefit Order", "is_mandatory": False},
            {"name": "30 वर्षे - सुधारित सेवांतर्गत आश्वासित प्रगती योजना आदेश", "name_english": "30 Yrs-Sudharit Sevantargat Ashwashit Pragati Yojana Benefit Order", "is_mandatory": False},
            
            # Award and increment orders
            {"name": "उत्कृष्ट/अतिउत्कृष्ट वेतनवाढ आदेश", "name_english": "Utkrushth/AtiUtkrushth Increment Order", "is_mandatory": False},
            {"name": "आदर्श ग्रामसेवक पुरस्कार प्राप्त आदेश", "name_english": "Adarsh Gramsevak Puraskar Order", "is_mandatory": False},
            {"name": "आदर्श वेतनवाढ आदेश", "name_english": "Adarsh Gramsevak Puraskar Increment Order", "is_mandatory": False},
            
            # Other service documents
            {"name": "सेवापुस्तक प्रत", "name_english": "Service book copy", "is_mandatory": False},
            {"name": "पदोन्नती आदेश", "name_english": "Promotion Order", "is_mandatory": False},
            {"name": "जिल्हा बदली असलेस आदेश (नाहरकत दाखला)", "name_english": "District Transfer Order (NOC)", "is_mandatory": False},
            
            # Special certificates
            {"name": "दिव्यांग प्रमाणपत्र", "name_english": "Handicapped Certificate", "is_mandatory": False},
            {"name": "मान्यता प्रमाणपत्र - कागदपत्र युनियन वेबसाईटवर टाकणेसाठी", "name_english": "Consent Certificate for Document on Union Domain", "is_mandatory": False},
        ]
        
        for doc_data in document_types_data:
            existing_doc = db.query(DocumentType).filter(DocumentType.name == doc_data["name"]).first()
            if not existing_doc:
                document_type = DocumentType(**doc_data)
                db.add(document_type)
                print(f"  ✅ Created document type: {doc_data['name']}")
            else:
                print(f"  ⏭️  Document type already exists: {doc_data['name']}")
        
        # 5. Create Districts
        print("🏘️  Creating districts...")
        districts_data = [
            {"name": "पुणे"},      # Pune
            {"name": "मुंबई"},     # Mumbai
            {"name": "नागपूर"},    # Nagpur
            {"name": "कोल्हापूर"}, # Kolhapur
            {"name": "औरंगाबाद"}, # Aurangabad
        ]
        
        district_objects = {}
        for district_data in districts_data:
            existing_district = db.query(District).filter(District.name == district_data["name"]).first()
            if not existing_district:
                district = District(**district_data)
                db.add(district)
                db.flush()  # To get the ID
                district_objects[district_data["name"]] = district
                print(f"  ✅ Created district: {district_data['name']}")
            else:
                district_objects[district_data["name"]] = existing_district
                print(f"  ⏭️  District already exists: {district_data['name']}")
        
        # 6. Create Blocks
        print("🏗️  Creating blocks...")
        blocks_data = [
            {"name": "पुणे शहर", "district_name": "पुणे"},
            {"name": "हवेली", "district_name": "पुणे"},
            {"name": "मुळशी", "district_name": "पुणे"},
            {"name": "बोरीवली", "district_name": "मुंबई"},
            {"name": "अंधेरी", "district_name": "मुंबई"},
        ]
        
        block_objects = {}
        for block_data in blocks_data:
            district = district_objects.get(block_data["district_name"])
            if district:
                existing_block = db.query(Block).filter(
                    Block.name == block_data["name"],
                    Block.district_id == district.id
                ).first()
                if not existing_block:
                    block = Block(
                        name=block_data["name"],
                        district_id=district.id
                    )
                    db.add(block)
                    db.flush()
                    block_objects[f"{block_data['district_name']}-{block_data['name']}"] = block
                    print(f"  ✅ Created block: {block_data['name']} in {block_data['district_name']}")
                else:
                    block_objects[f"{block_data['district_name']}-{block_data['name']}"] = existing_block
                    print(f"  ⏭️  Block already exists: {block_data['name']}")
        
        # 7. Create Gram Panchayats
        print("🏛️  Creating gram panchayats...")
        gp_data = [
            {"name": "कर्वे नगर", "block_key": "पुणे-पुणे शहर"},
            {"name": "शिवाजी नगर", "block_key": "पुणे-पुणे शहर"},
            {"name": "हवेली गाव", "block_key": "पुणे-हवेली"},
            {"name": "मुळशी गाव", "block_key": "पुणे-मुळशी"},
        ]
        
        gp_objects = {}
        for gp_data_item in gp_data:
            block = block_objects.get(gp_data_item["block_key"])
            if block:
                existing_gp = db.query(GramPanchayat).filter(
                    GramPanchayat.name == gp_data_item["name"],
                    GramPanchayat.block_id == block.id
                ).first()
                if not existing_gp:
                    gp = GramPanchayat(
                        name=gp_data_item["name"],
                        block_id=block.id
                    )
                    db.add(gp)
                    db.flush()
                    gp_objects[gp_data_item["name"]] = gp
                    print(f"  ✅ Created gram panchayat: {gp_data_item['name']}")
                else:
                    gp_objects[gp_data_item["name"]] = existing_gp
                    print(f"  ⏭️  Gram panchayat already exists: {gp_data_item['name']}")
        
        # 8. Create Default Super Admin User
        print("👤 Creating default users...")
        pune_district = district_objects.get("पुणे")
        pune_city_block = block_objects.get("पुणे-पुणे शहर")
        karve_nagar_gp = gp_objects.get("कर्वे नगर")
        
        if pune_district and pune_city_block and karve_nagar_gp:
            existing_admin = db.query(User).filter(User.email == "admin@gramseva.gov.in").first()
            if not existing_admin:
                admin_user = User(
                    first_name="सुपर",
                    last_name="अॅडमिन",
                    email="admin@gramseva.gov.in",
                    mobile_number="+919999999999",
                    whatsapp_number="+919999999999",
                    role_id=1,  # superAdmin
                    designation=UserDesignation.VISTAR_ADHIKARI,
                    district_id=pune_district.id,
                    block_id=pune_city_block.id,
                    gram_panchayat_id=karve_nagar_gp.id,
                    status=ApprovalStatus.APPROVED,
                    documents_uploaded=True,
                )
                db.add(admin_user)
                print(f"  ✅ Created super admin user: admin@gramseva.gov.in")
            else:
                print(f"  ⏭️  Super admin already exists")
        
        # Commit all changes
        db.commit()
        print("✨ Seed data creation completed successfully!")
        
        # Print summary
        print("\n📊 Summary:")
        print(f"  Roles: {db.query(Role).count()}")
        print(f"  Departments: {db.query(Department).count()}")
        print(f"  Yojanas: {db.query(Yojana).count()}")
        print(f"  Document Types: {db.query(DocumentType).count()}")
        print(f"  Districts: {db.query(District).count()}")
        print(f"  Blocks: {db.query(Block).count()}")
        print(f"  Gram Panchayats: {db.query(GramPanchayat).count()}")
        print(f"  Users: {db.query(User).count()}")
        
    except Exception as e:
        print(f"❌ Error creating seed data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_seed_data()