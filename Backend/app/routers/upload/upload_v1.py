from fastapi import FastAPI,APIRouter, Depends, File, UploadFile, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base
from ocr_service import MarathiOCRService
from search_service import SearchService
import shutil
import os
from typing import Optional, List
from sqlalchemy.orm import Session

from app.config import get_db
from app.models.enums.vx_api_perms_enum import VxAPIPermsEnum
from app.services.document_service import DocumentTypeService
from app.utils.vx_api_perms_utils import VxAPIPermsUtils

router = APIRouter(
    prefix="/v1/upload",
    tags=["gramsevak"],
    responses={404: {"description": "Not Found"}}
)

ocr_service = MarathiOCRService()

VxAPIPermsUtils.set_perm_get(path=router.prefix + '/getdocumenttype', perm=VxAPIPermsEnum.PUBLIC)
@router.get("/getdocumenttype",
            # response_model=List[GramsevakListItem]
            )
async def get_all_document_types(db: Session = Depends(get_db)):
    return DocumentTypeService.get_all_document_types(db=db)

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
        from models import Book, Page, Word
        
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

@router.get("/books")
async def get_books(db: Session = Depends(get_db)):
    """Get all books"""
    from models import Book
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