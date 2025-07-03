import os
import datetime
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:#Mystack9393#@localhost:5432/Gs_devDB")

engine = create_engine(DATABASE_URL)
metadata = MetaData()
Session = sessionmaker(bind=engine)
session = Session()

# Departments
departments = Table('departments', metadata, autoload_with=engine)
session.execute(departments.insert(), [
    {'id': 1, 'name': 'कृषी विभाग', 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
])

# Districts
districts = Table('districts', metadata, autoload_with=engine)
session.execute(districts.insert(), [
    {'id': 1, 'name': 'पुणे', 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
])

# Blocks
blocks = Table('blocks', metadata, autoload_with=engine)
session.execute(blocks.insert(), [
    {'id': 1, 'name': 'हवेली', 'district_id': 1, 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
])

# Gram Panchayats
gram_panchayats = Table('gram_panchayats', metadata, autoload_with=engine)
session.execute(gram_panchayats.insert(), [
    {'id': 1, 'name': 'लोणी काळभोर', 'block_id': 1, 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
])

# # Roles
# roles = Table('roles', metadata, autoload_with=engine)
# session.execute(roles.insert(), [
#     {'id': 1, 'name': 'admin', 'description': 'प्रशासक', 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
# ])

# Users
users = Table('users', metadata, autoload_with=engine)
session.execute(users.insert(), [
    {'id': 1, 'first_name': 'राम', 'last_name': 'शिंदे', 'email': 'ram@example.com', 'mobile_number': '9999999999', 'role_id': 1, 'designation': 'GRAM_PANCHAYAT_ADHIKARI', 'district_id': 1, 'block_id': 1, 'gram_panchayat_id': 1, 'status': 'APPROVED', 'created_by': None, 'updated_by': None, 'documents_uploaded': True, 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
])

# Books
books = Table('books', metadata, autoload_with=engine)
session.execute(books.insert(), [
    {'id': 1, 'title': 'मराठी पुस्तक', 'department_id': 1, 'file_path': '/files/book1.pdf', 'is_processed': True, 'created_by': 1, 'updated_by': None, 'filename': 'book1.pdf', 'upload_date': datetime.datetime.utcnow(), 'total_pages': 100, 'author': 'साने गुरुजी', 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
])

# Pages
pages = Table('pages', metadata, autoload_with=engine)
session.execute(pages.insert(), [
    {'id': 1, 'book_id': 1, 'page_number': 1, 'content': 'ही पहिली पान आहे.', 'confidence_score': 0.99, 'word_count': 5, 'character_count': 18, 'language_detected': 'mar', 'processing_time': 0.5}
])

# Words
words = Table('words', metadata, autoload_with=engine)
session.execute(words.insert(), [
    {'id': 1, 'page_id': 1, 'word': 'पहिली', 'x_position': 10, 'y_position': 20, 'width': 30, 'height': 15, 'confidence': 0.98, 'is_marathi': True, 'font_size': 12}
])

# Yojanas
yojanas = Table('yojanas', metadata, autoload_with=engine)
session.execute(yojanas.insert(), [
    {'id': 1, 'name': 'शिक्षण योजना', 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
])

# GRs
grs = Table('grs', metadata, autoload_with=engine)
session.execute(grs.insert(), [
    {'id': 1, 'gr_number': 'GR001', 'gr_code': 'GR-EDU-01', 'subject': 'शिक्षणासाठी अनुदान', 'department_id': 1, 'effective_date': datetime.date.today(), 'yojana_id': 1, 'file_path': '/files/gr1.pdf', 'created_by': 1, 'updated_by': None, 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
])

# Document Types
document_types = Table('document_types', metadata, autoload_with=engine)
session.execute(document_types.insert(), [
    {'id': 1, 'name': 'ओळखपत्र', 'name_english': 'ID Card', 'is_mandatory': True, 'field_definitions': None, 'category': 'IDENTITY', 'instructions': 'ओळखपत्र अपलोड करा', 'created_by': 1, 'updated_by': None, 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
])

# User Documents
user_documents = Table('user_documents', metadata, autoload_with=engine)
session.execute(user_documents.insert(), [
    {'id': 1, 'user_id': 1, 'document_type_id': 1, 'file_path': '/files/id1.pdf', 'field_values': None, 'verification_status': 'APPROVED', 'admin_comments': 'सर्व तपशील बरोबर आहेत', 'created_by': 1, 'updated_by': None, 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
])

# User OTPs
user_otps = Table('user_otps', metadata, autoload_with=engine)
session.execute(user_otps.insert(), [
    {'id': 1, 'user_id': 1, 'otp': '123456', 'expires_at': datetime.datetime.utcnow() + datetime.timedelta(minutes=5), 'message_sid': 'SID123'}
])

session.commit()
session.close()
print("Seed data inserted successfully.")
