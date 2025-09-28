from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
import os
import shutil

from app.config import get_db
from app.services.ocr_service import MarathiOCRService
from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.services.document_service import DocumentTypeService
from app.utils.vx_api_perms_utils import VxAPIPermsUtils

router = APIRouter(
    prefix="/v1/upload",
    tags=["upload"],
    responses={404: {"description": "Not Found"}}
)

ocr_service = MarathiOCRService()

# FIXED: Enhanced getdocumenttype endpoint
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getdocumenttype', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getdocumenttype")
async def get_all_document_types(
    category: Optional[str] = Query(None, description="Filter by category (identity_proof, educational, etc.)"),
    is_mandatory: Optional[bool] = Query(None, description="Filter by mandatory status"),
    include_field_definitions: bool = Query(True, description="Include field definitions in response"),
    db: Session = Depends(get_db)
):
    """
    Get all document types with comprehensive information
    
    Query Parameters:
    - category: Filter by document category
    - is_mandatory: Filter by mandatory status (true/false)
    - include_field_definitions: Include field definitions (default: true)
    """
    try:
        return DocumentTypeService.get_all_document_types_enhanced(
            db=db,
            category=category,
            is_mandatory=is_mandatory,
            include_field_definitions=include_field_definitions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving document types: {str(e)}")

# Keep existing endpoints...
@router.post("/upload-book/")
async def upload_book(
    file: UploadFile = File(...),
    title: str = Form(...),
    author: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload and process PDF book"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Save uploaded file
    file_path = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Extract text using OCR
        extracted_data = ocr_service.extract_text_from_pdf(file_path)
        
        # Save to database
        from app.models.books import Book, Page, Word
        
        book = Book(
            title=title,
            author=author,
            filename=file.filename,
            total_pages=len(extracted_data)
        )
        db.add(book)
        db.commit()
        db.refresh(book)
        
        # Save pages and words
        for page_data in extracted_data:
            page = Page(
                book_id=book.id,
                page_number=page_data['page_number'],
                content=page_data['text'],
                confidence_score=page_data['confidence']
            )
            db.add(page)
            db.commit()
            db.refresh(page)
            
            # Save word positions
            boxes = page_data['boxes']
            for i, word in enumerate(boxes['text']):
                if word.strip() and int(boxes['conf'][i]) > 30:
                    word_obj = Word(
                        page_id=page.id,
                        word=word,
                        x_position=boxes['left'][i],
                        y_position=boxes['top'][i],
                        width=boxes['width'][i],
                        height=boxes['height'][i],
                        confidence=float(boxes['conf'][i])
                    )
                    db.add(word_obj)
            
            db.commit()
        
        return {"message": "Book uploaded and processed successfully", "book_id": book.id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@router.get("/books")
async def get_books(db: Session = Depends(get_db)):
    """Get all books"""
    from app.models.books import Book
    books = db.query(Book).all()
    return [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "total_pages": book.total_pages,
            "upload_date": book.upload_date
        }
        for book in books
    ]
