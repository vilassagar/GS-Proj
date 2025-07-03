"""Revision ID: 3b1c2d4e5f6g
Revises: 2a34e1c5ce77
Create Date: 2025-07-02
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Boolean, DateTime, Float, Text, Date
import datetime

def upgrade():
    # Departments
    departments_table = table('departments',
        column('id', Integer),
        column('name', String),
        column('created_at', DateTime),
        column('updated_at', DateTime),
        column('is_active', Boolean)
    )
    op.bulk_insert(departments_table, [
        {'id': 1, 'name': 'कृषी विभाग', 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
    ])

    # Districts
    districts_table = table('districts',
        column('id', Integer),
        column('name', String),
        column('created_at', DateTime),
        column('updated_at', DateTime),
        column('is_active', Boolean)
    )
    op.bulk_insert(districts_table, [
        {'id': 1, 'name': 'पुणे', 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
    ])

    # Blocks
    blocks_table = table('blocks',
        column('id', Integer),
        column('name', String),
        column('district_id', Integer),
        column('created_at', DateTime),
        column('updated_at', DateTime),
        column('is_active', Boolean)
    )
    op.bulk_insert(blocks_table, [
        {'id': 1, 'name': 'हवेली', 'district_id': 1, 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
    ])

    # Gram Panchayats
    gram_panchayats_table = table('gram_panchayats',
        column('id', Integer),
        column('name', String),
        column('block_id', Integer),
        column('created_at', DateTime),
        column('updated_at', DateTime),
        column('is_active', Boolean)
    )
    op.bulk_insert(gram_panchayats_table, [
        {'id': 1, 'name': 'लोणी काळभोर', 'block_id': 1, 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
    ])

    # Roles
    roles_table = table('roles',
        column('id', Integer),
        column('name', String),
        column('description', String),
        column('created_at', DateTime),
        column('updated_at', DateTime),
        column('is_active', Boolean)
    )
    op.bulk_insert(roles_table, [
        {'id': 1, 'name': 'admin', 'description': 'प्रशासक', 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
    ])

    # Users
    users_table = table('users',
        column('id', Integer),
        column('first_name', String),
        column('last_name', String),
        column('email', String),
        column('mobile_number', String),
        column('role_id', Integer),
        column('designation', sa.Enum),
        column('district_id', Integer),
        column('block_id', Integer),
        column('gram_panchayat_id', Integer),
        column('status', sa.Enum),
        column('created_by', Integer),
        column('updated_by', Integer),
        column('documents_uploaded', Boolean),
        column('created_at', DateTime),
        column('updated_at', DateTime),
        column('is_active', Boolean)
    )
    op.bulk_insert(users_table, [
        {'id': 1, 'first_name': 'राम', 'last_name': 'शिंदे', 'email': 'ram@example.com', 'mobile_number': '9999999999', 'role_id': 1, 'designation': 'GRAM_PANCHAYAT_ADHIKARI', 'district_id': 1, 'block_id': 1, 'gram_panchayat_id': 1, 'status': 'APPROVED', 'created_by': None, 'updated_by': None, 'documents_uploaded': True, 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
    ])

    # Books
    books_table = table('books',
        column('id', Integer),
        column('title', String),
        column('department_id', Integer),
        column('file_path', String),
        column('is_processed', Boolean),
        column('created_by', Integer),
        column('updated_by', Integer),
        column('filename', String),
        column('upload_date', DateTime),
        column('total_pages', Integer),
        column('author', String),
        column('created_at', DateTime),
        column('updated_at', DateTime),
        column('is_active', Boolean)
    )
    op.bulk_insert(books_table, [
        {'id': 1, 'title': 'मराठी पुस्तक', 'department_id': 1, 'file_path': '/files/book1.pdf', 'is_processed': True, 'created_by': 1, 'updated_by': None, 'filename': 'book1.pdf', 'upload_date': datetime.datetime.utcnow(), 'total_pages': 100, 'author': 'साने गुरुजी', 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
    ])

    # Pages
    pages_table = table('pages',
        column('id', Integer),
        column('book_id', Integer),
        column('page_number', Integer),
        column('content', Text),
        column('confidence_score', Float),
        column('word_count', Integer),
        column('character_count', Integer),
        column('language_detected', String),
        column('processing_time', Float)
    )
    op.bulk_insert(pages_table, [
        {'id': 1, 'book_id': 1, 'page_number': 1, 'content': 'ही पहिली पान आहे.', 'confidence_score': 0.99, 'word_count': 5, 'character_count': 18, 'language_detected': 'mar', 'processing_time': 0.5}
    ])

    # Words
    words_table = table('words',
        column('id', Integer),
        column('page_id', Integer),
        column('word', String),
        column('x_position', Integer),
        column('y_position', Integer),
        column('width', Integer),
        column('height', Integer),
        column('confidence', Float),
        column('is_marathi', Boolean),
        column('font_size', Integer)
    )
    op.bulk_insert(words_table, [
        {'id': 1, 'page_id': 1, 'word': 'पहिली', 'x_position': 10, 'y_position': 20, 'width': 30, 'height': 15, 'confidence': 0.98, 'is_marathi': True, 'font_size': 12}
    ])

    # Yojanas
    yojanas_table = table('yojanas',
        column('id', Integer),
        column('name', String),
        column('created_at', DateTime),
        column('updated_at', DateTime),
        column('is_active', Boolean)
    )
    op.bulk_insert(yojanas_table, [
        {'id': 1, 'name': 'शिक्षण योजना', 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
    ])

    # GRs
    grs_table = table('grs',
        column('id', Integer),
        column('gr_number', String),
        column('gr_code', String),
        column('subject', String),
        column('department_id', Integer),
        column('effective_date', Date),
        column('yojana_id', Integer),
        column('file_path', String),
        column('created_by', Integer),
        column('updated_by', Integer),
        column('created_at', DateTime),
        column('updated_at', DateTime),
        column('is_active', Boolean)
    )
    op.bulk_insert(grs_table, [
        {'id': 1, 'gr_number': 'GR001', 'gr_code': 'GR-EDU-01', 'subject': 'शिक्षणासाठी अनुदान', 'department_id': 1, 'effective_date': datetime.date.today(), 'yojana_id': 1, 'file_path': '/files/gr1.pdf', 'created_by': 1, 'updated_by': None, 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
    ])

    # Document Types
    document_types_table = table('document_types',
        column('id', Integer),
        column('name', String),
        column('name_english', String),
        column('is_mandatory', Boolean),
        column('field_definitions', sa.JSON),
        column('category', String),
        column('instructions', Text),
        column('created_by', Integer),
        column('updated_by', Integer),
        column('created_at', DateTime),
        column('updated_at', DateTime),
        column('is_active', Boolean)
    )
    op.bulk_insert(document_types_table, [
        {'id': 1, 'name': 'ओळखपत्र', 'name_english': 'ID Card', 'is_mandatory': True, 'field_definitions': None, 'category': 'IDENTITY', 'instructions': 'ओळखपत्र अपलोड करा', 'created_by': 1, 'updated_by': None, 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
    ])

    # User Documents
    user_documents_table = table('user_documents',
        column('id', Integer),
        column('user_id', Integer),
        column('document_type_id', Integer),
        column('file_path', String),
        column('field_values', sa.JSON),
        column('verification_status', sa.Enum),
        column('admin_comments', Text),
        column('created_by', Integer),
        column('updated_by', Integer),
        column('created_at', DateTime),
        column('updated_at', DateTime),
        column('is_active', Boolean)
    )
    op.bulk_insert(user_documents_table, [
        {'id': 1, 'user_id': 1, 'document_type_id': 1, 'file_path': '/files/id1.pdf', 'field_values': None, 'verification_status': 'APPROVED', 'admin_comments': 'सर्व तपशील बरोबर आहेत', 'created_by': 1, 'updated_by': None, 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
    ])

    # User OTPs
    user_otps_table = table('user_otps',
        column('id', Integer),
        column('user_id', Integer),
        column('otp', String),
        column('expires_at', DateTime),
        column('message_sid', String)
    )
    op.bulk_insert(user_otps_table, [
        {'id': 1, 'user_id': 1, 'otp': '123456', 'expires_at': datetime.datetime.utcnow() + datetime.timedelta(minutes=5), 'message_sid': 'SID123'}
    ])

def downgrade():
    op.execute('DELETE FROM user_otps WHERE id=1')
    op.execute('DELETE FROM user_documents WHERE id=1')
    op.execute('DELETE FROM document_types WHERE id=1')
    op.execute('DELETE FROM grs WHERE id=1')
    op.execute('DELETE FROM yojanas WHERE id=1')
    op.execute('DELETE FROM words WHERE id=1')
    op.execute('DELETE FROM pages WHERE id=1')
    op.execute('DELETE FROM books WHERE id=1')
    op.execute('DELETE FROM users WHERE id=1')
    op.execute('DELETE FROM roles WHERE id=1')
    op.execute('DELETE FROM gram_panchayats WHERE id=1')
    op.execute('DELETE FROM blocks WHERE id=1')
    op.execute('DELETE FROM districts WHERE id=1')
    op.execute('DELETE FROM departments WHERE id=1')
