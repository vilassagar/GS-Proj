from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
from sqlalchemy.orm import Session
from typing import Optional, List
import os
import shutil
import uuid
from datetime import datetime

from app.config import get_db
from app.services.ocr_service import MarathiOCRService
from app.services.search_service import SearchService
from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.services.document_service import DocumentTypeService
from app.utils.vx_api_perms_utils import VxAPIPermsUtils

router = APIRouter(
    prefix="/v1/upload",
    tags=["upload"],
    responses={404: {"description": "Not Found"}}
)

ocr_service = MarathiOCRService()

VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getdocumenttype', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getdocumenttype")
async def get_all_document_types(db: Session = Depends(get_db)):
    return DocumentTypeService.get_all_document_types(db=db)

# ✅ FIX 1: Add missing permission for upload endpoint
VxAPIPermsUtils.set_perm_post(path=router.prefix + '/upload-book/', perm=VxAPIPermsEnum.AUTHENTICATED)
@router.post("/upload-book/")
async def upload_book(
    file: UploadFile = File(...),
    title: str = Form(...),
    author: str = Form(...),
    department_id: Optional[int] = Form(None),  # ✅ FIX 2: Add optional department
    db: Session = Depends(get_db)
):
    """Upload and process PDF book"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # ✅ FIX 3: Create unique filename to avoid conflicts
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{timestamp}_{uuid.uuid4().hex[:8]}_{file.filename}"
    file_path = f"uploads/{unique_filename}"
    
    os.makedirs("uploads", exist_ok=True)
    
    # ✅ FIX 4: Add file saving error handling
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    try:
        # Extract text using OCR
        extracted_data = ocr_service.extract_text_from_pdf(file_path)
        
        # Save to database
        from app.models.books import Book, Page, Word
        
        # ✅ FIX 5: Add missing file_path parameter (THIS WAS THE MAIN ISSUE!)
        book = Book(
            title=title,
            author=author,
            filename=file.filename,  # Original filename
            file_path=file_path,     # ✅ CRITICAL FIX: Add this line!
            department_id=department_id,  # ✅ FIX 6: Add department if provided
            is_processed=True,       # ✅ FIX 7: Set processing status
            total_pages=len(extracted_data)
        )
        db.add(book)
        db.commit()
        db.refresh(book)
        
        # ✅ FIX 8: Add counters for better feedback
        pages_created = 0
        words_created = 0
        
        # Save pages and words
        for page_data in extracted_data:
            # ✅ FIX 9: Add more page fields for better functionality
            page = Page(
                book_id=book.id,
                page_number=page_data['page_number'],
                content=page_data['text'],
                confidence_score=page_data.get('confidence', 0.0),
                word_count=len([w for w in page_data['text'].split() if w.strip()]),
                character_count=len(page_data['text']),
                language_detected='mar' if any('\u0900' <= c <= '\u097F' for c in page_data['text']) else 'eng'
            )
            db.add(page)
            db.commit()
            db.refresh(page)
            pages_created += 1
            
            # ✅ FIX 10: Add error handling for word processing
            boxes = page_data.get('boxes', {})
            if boxes and 'text' in boxes:
                for i, word in enumerate(boxes['text']):
                    try:
                        if (word.strip() and 
                            i < len(boxes.get('conf', [])) and 
                            int(boxes['conf'][i]) > 30):
                            
                            word_obj = Word(
                                page_id=page.id,
                                word=word,
                                x_position=boxes['left'][i] if i < len(boxes.get('left', [])) else None,
                                y_position=boxes['top'][i] if i < len(boxes.get('top', [])) else None,
                                width=boxes['width'][i] if i < len(boxes.get('width', [])) else None,
                                height=boxes['height'][i] if i < len(boxes.get('height', [])) else None,
                                confidence=float(boxes['conf'][i]),
                                is_marathi=any('\u0900' <= c <= '\u097F' for c in word)
                            )
                            db.add(word_obj)
                            words_created += 1
                    except (IndexError, ValueError, TypeError) as word_error:
                        # Skip problematic words but continue processing
                        continue
                
                # Commit words for this page
                db.commit()
        
        # ✅ FIX 11: Return more detailed success response
        return {
            "message": "Book uploaded and processed successfully",
            "book_id": book.id,
            "original_filename": file.filename,
            "stored_filename": unique_filename,
            "pages_processed": pages_created,
            "words_extracted": words_created,
            "total_pages": len(extracted_data)
        }
    
    except Exception as e:
        # ✅ FIX 12: Clean up uploaded file on error
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Don't fail if cleanup fails
        
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

# ✅ FIX 13: Add permissions for search endpoints
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/search/exact', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/search/exact")
async def exact_search(
    query: str,
    book_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Exact text search"""
    search_service = SearchService(db)
    results = search_service.exact_search(query, book_id)
    return {"results": results, "count": len(results)}

VxAPIPermsUtils.set_perm_get(path=router.prefix + '/search/fuzzy', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/search/fuzzy")
async def fuzzy_search(
    query: str,
    book_id: Optional[int] = None,
    threshold: float = 0.7,
    db: Session = Depends(get_db)
):
    """Fuzzy/approximate search"""
    search_service = SearchService(db)
    results = search_service.fuzzy_search(query, book_id, threshold)
    return {"results": results, "count": len(results)}

VxAPIPermsUtils.set_perm_get(path=router.prefix + '/search/phrase', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/search/phrase")
async def phrase_search(
    phrase: str,
    book_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Phrase search"""
    search_service = SearchService(db)
    results = search_service.phrase_search(phrase, book_id)
    return {"results": results, "count": len(results)}

VxAPIPermsUtils.set_perm_get(path=router.prefix + '/search/positional', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/search/positional")
async def positional_search(
    query: str,
    book_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Positional search"""
    search_service = SearchService(db)
    results = search_service.positional_search(query, book_id)
    return {"results": results, "count": len(results)}

VxAPIPermsUtils.set_perm_get(path=router.prefix + '/search/semantic', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/search/semantic")
async def semantic_search(
    query: str,
    book_id: Optional[int] = None,
    top_k: int = 10,
    db: Session = Depends(get_db)
):
    """Semantic search"""
    search_service = SearchService(db)
    results = search_service.semantic_search(query, book_id, top_k)
    return {"results": results, "count": len(results)}

VxAPIPermsUtils.set_perm_get(path=router.prefix + '/books', perm=VxAPIPermsEnum.PUBLIC)
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
            "upload_date": book.upload_date,
            "is_processed": book.is_processed,
            "filename": book.filename,
            "department_id": book.department_id
        }
        for book in books
    ]

# ✅ FIX 14: Add helpful endpoints
VxAPIPermsUtils.set_perm_get(path=router.prefix + '/ocr-status', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/ocr-status")
async def check_ocr_status():
    """Check if OCR service is available"""
    return {
        "tesseract_available": ocr_service.tesseract_available if hasattr(ocr_service, 'tesseract_available') else True,
        "supported_languages": ["English", "Marathi"],
        "upload_formats": ["PDF"]
    }

VxAPIPermsUtils.set_perm_get(path=router.prefix + '/book/{book_id}/details', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/book/{book_id}/details")
async def get_book_details(book_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific book"""
    from app.models.books import Book, Page
    
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    pages = db.query(Page).filter(Page.book_id == book_id).all()
    
    return {
        "book": {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "filename": book.filename,
            "total_pages": book.total_pages,
            "is_processed": book.is_processed,
            "upload_date": book.upload_date
        },
        "pages": [
            {
                "page_number": page.page_number,
                "word_count": page.word_count,
                "character_count": page.character_count,
                "language_detected": page.language_detected,
                "confidence_score": page.confidence_score
            }
            for page in pages
        ]
    }