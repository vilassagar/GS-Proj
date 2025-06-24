# search_service.py
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
import re
from app.models.books import Book, Page, Word  # ✅ Fixed import

class SearchService:
    def __init__(self, db: Session):
        self.db = db
        self.semantic_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    
    def _extract_context_lines(self, content: str, query: str, min_lines: int = 3) -> Dict:
        """Extract context lines around the match"""
        lines = content.split('\n')
        matched_lines = []
        
        for i, line in enumerate(lines):
            if query.lower() in line.lower():
                # Get context around the match
                start_idx = max(0, i - min_lines//2)
                end_idx = min(len(lines), i + min_lines//2 + 1)
                
                # Ensure we have at least min_lines
                if end_idx - start_idx < min_lines:
                    if start_idx == 0:
                        end_idx = min(len(lines), start_idx + min_lines)
                    else:
                        start_idx = max(0, end_idx - min_lines)
                
                context_lines = lines[start_idx:end_idx]
                matched_lines.append({
                    'line_number': i + 1,
                    'matched_line': line,
                    'context': '\n'.join(context_lines),
                    'context_start': start_idx + 1,
                    'context_end': end_idx
                })
        
        return matched_lines
    
    def exact_search(self, query: str, book_id: Optional[int] = None, limit: int = 50) -> List[Dict]:
        """1. Enhanced exact text search with context"""
        query_filter = self.db.query(Page).filter(Page.content.contains(query))
        
        if book_id:
            query_filter = query_filter.filter(Page.book_id == book_id)
        
        # Join with Book to get book details
        query_filter = query_filter.join(Book).limit(limit)
        results = query_filter.all()
        
        enhanced_results = []
        books_found = {}  # Track books and their matches
        
        for result in results:
            book_key = f"{result.book.id}-{result.book.title}"
            if book_key not in books_found:
                books_found[book_key] = {
                    'book_id': result.book.id,
                    'book_title': result.book.title,
                    'book_author': result.book.author,
                    'total_pages': result.book.total_pages,
                    'matches': []
                }
            
            # Extract context lines
            context_matches = self._extract_context_lines(result.content, query)
            
            for match in context_matches:
                books_found[book_key]['matches'].append({
                    'page_number': result.page_number,
                    'line_number': match['line_number'],
                    'matched_line': match['matched_line'],
                    'context': match['context'],
                    'context_range': f"Lines {match['context_start']}-{match['context_end']}",
                    'confidence_score': result.confidence_score,
                    'match_type': 'exact'
                })
        
        # Convert to list format with book grouping
        for book_data in books_found.values():
            enhanced_results.append(book_data)
        
        return enhanced_results
    
    def fuzzy_search(self, query: str, book_id: Optional[int] = None, threshold: float = 0.7, limit: int = 50) -> List[Dict]:
        """2. Enhanced fuzzy/approximate search with context"""
        from difflib import SequenceMatcher
        
        query_filter = self.db.query(Page).join(Book)
        if book_id:
            query_filter = query_filter.filter(Page.book_id == book_id)
            
        all_pages = query_filter.limit(limit * 2).all()  # Get more pages for fuzzy matching
        books_found = {}
        
        for page in all_pages:
            lines = page.content.split('\n')
            book_key = f"{page.book.id}-{page.book.title}"
            
            if book_key not in books_found:
                books_found[book_key] = {
                    'book_id': page.book.id,
                    'book_title': page.book.title,
                    'book_author': page.book.author,
                    'total_pages': page.book.total_pages,
                    'matches': []
                }
            
            for line_idx, line in enumerate(lines):
                words = line.split()
                for word in words:
                    similarity = SequenceMatcher(None, query.lower(), word.lower()).ratio()
                    if similarity >= threshold:
                        # Get context around this line
                        start_idx = max(0, line_idx - 1)
                        end_idx = min(len(lines), line_idx + 3)  # At least 3 lines
                        context_lines = lines[start_idx:end_idx]
                        
                        books_found[book_key]['matches'].append({
                            'page_number': page.page_number,
                            'line_number': line_idx + 1,
                            'matched_line': line,
                            'matched_word': word,
                            'similarity': similarity,
                            'context': '\n'.join(context_lines),
                            'context_range': f"Lines {start_idx + 1}-{end_idx}",
                            'confidence_score': page.confidence_score,
                            'match_type': 'fuzzy'
                        })
                        break  # One match per line is enough
        
        # Sort by similarity and limit results
        enhanced_results = []
        for book_data in books_found.values():
            # Sort matches by similarity
            book_data['matches'].sort(key=lambda x: x['similarity'], reverse=True)
            # Limit matches per book
            book_data['matches'] = book_data['matches'][:10]
            enhanced_results.append(book_data)
        
        return enhanced_results
    
    def phrase_search(self, phrase: str, book_id: Optional[int] = None, limit: int = 50) -> List[Dict]:
        """3. Enhanced phrase search with context"""
        query_filter = self.db.query(Page).join(Book).filter(Page.content.ilike(f'%{phrase}%'))
        
        if book_id:
            query_filter = query_filter.filter(Page.book_id == book_id)
            
        results = query_filter.limit(limit).all()
        books_found = {}
        
        for result in results:
            book_key = f"{result.book.id}-{result.book.title}"
            if book_key not in books_found:
                books_found[book_key] = {
                    'book_id': result.book.id,
                    'book_title': result.book.title,
                    'book_author': result.book.author,
                    'total_pages': result.book.total_pages,
                    'matches': []
                }
            
            # Find all occurrences of the phrase in the page
            lines = result.content.split('\n')
            for line_idx, line in enumerate(lines):
                if phrase.lower() in line.lower():
                    # Get extended context (at least 3 lines)
                    start_idx = max(0, line_idx - 1)
                    end_idx = min(len(lines), line_idx + 3)
                    context_lines = lines[start_idx:end_idx]
                    
                    # Highlight the phrase in the matched line
                    highlighted_line = line.replace(phrase, f"**{phrase}**")
                    
                    books_found[book_key]['matches'].append({
                        'page_number': result.page_number,
                        'line_number': line_idx + 1,
                        'matched_line': highlighted_line,
                        'phrase': phrase,
                        'context': '\n'.join(context_lines),
                        'context_range': f"Lines {start_idx + 1}-{end_idx}",
                        'confidence_score': result.confidence_score,
                        'match_type': 'phrase'
                    })
        
        enhanced_results = []
        for book_data in books_found.values():
            enhanced_results.append(book_data)
        
        return enhanced_results
    
    def positional_search(self, query: str, book_id: Optional[int] = None, limit: int = 50) -> List[Dict]:
        """4. Enhanced positional search with context"""
        words_query = self.db.query(Word).filter(Word.word.ilike(f'%{query}%')).join(Page).join(Book)
        
        if book_id:
            words_query = words_query.filter(Page.book_id == book_id)
            
        word_results = words_query.limit(limit).all()
        books_found = {}
        
        for word in word_results:
            book_key = f"{word.page.book.id}-{word.page.book.title}"
            if book_key not in books_found:
                books_found[book_key] = {
                    'book_id': word.page.book.id,
                    'book_title': word.page.book.title,
                    'book_author': word.page.book.author,
                    'total_pages': word.page.book.total_pages,
                    'matches': []
                }
            
            # Get surrounding context from the page
            page_lines = word.page.content.split('\n')
            word_line = None
            line_idx = 0
            
            # Find which line contains this word
            for i, line in enumerate(page_lines):
                if word.word in line:
                    word_line = line
                    line_idx = i
                    break
            
            if word_line:
                # Get context around the word
                start_idx = max(0, line_idx - 1)
                end_idx = min(len(page_lines), line_idx + 3)
                context_lines = page_lines[start_idx:end_idx]
                
                books_found[book_key]['matches'].append({
                    'page_number': word.page.page_number,
                    'line_number': line_idx + 1,
                    'matched_word': word.word,
                    'matched_line': word_line,
                    'position': {'x': word.x_position, 'y': word.y_position},
                    'dimensions': {'width': word.width, 'height': word.height},
                    'confidence': word.confidence,
                    'context': '\n'.join(context_lines),
                    'context_range': f"Lines {start_idx + 1}-{end_idx}",
                    'match_type': 'positional'
                })
        
        enhanced_results = []
        for book_data in books_found.values():
            # Sort by confidence
            book_data['matches'].sort(key=lambda x: x['confidence'], reverse=True)
            enhanced_results.append(book_data)
        
        return enhanced_results
    
    def semantic_search(self, query: str, book_id: Optional[int] = None, top_k: int = 20, min_similarity: float = 0.3) -> List[Dict]:
        """5. Enhanced semantic search with context"""
        query_filter = self.db.query(Page).join(Book)
        if book_id:
            query_filter = query_filter.filter(Page.book_id == book_id)
            
        all_pages = query_filter.all()
        
        if not all_pages:
            return []
        
        # Split pages into chunks for better semantic matching
        page_chunks = []
        page_metadata = []
        
        for page in all_pages:
            lines = page.content.split('\n')
            # Create overlapping chunks of 3-5 lines
            for i in range(0, len(lines), 3):
                chunk_lines = lines[i:i+5]  # 5 lines per chunk with overlap
                if len(chunk_lines) >= 2:  # Minimum 2 lines
                    chunk_text = '\n'.join(chunk_lines)
                    page_chunks.append(chunk_text)
                    page_metadata.append({
                        'page': page,
                        'chunk_start_line': i + 1,
                        'chunk_end_line': min(i + 5, len(lines)),
                        'chunk_lines': chunk_lines
                    })
        
        if not page_chunks:
            return []
        
        # Get embeddings
        query_embedding = self.semantic_model.encode([query])
        chunk_embeddings = self.semantic_model.encode(page_chunks)
        
        # Calculate similarities
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity(query_embedding, chunk_embeddings)[0]
        
        # Get top results
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        books_found = {}
        for idx in top_indices:
            similarity_score = similarities[idx]
            if similarity_score > min_similarity:
                metadata = page_metadata[idx]
                page = metadata['page']
                
                book_key = f"{page.book.id}-{page.book.title}"
                if book_key not in books_found:
                    books_found[book_key] = {
                        'book_id': page.book.id,
                        'book_title': page.book.title,
                        'book_author': page.book.author,
                        'total_pages': page.book.total_pages,
                        'matches': []
                    }
                
                # Get extended context around the semantic match
                all_lines = page.content.split('\n')
                start_idx = max(0, metadata['chunk_start_line'] - 2)
                end_idx = min(len(all_lines), metadata['chunk_end_line'] + 2)
                extended_context = all_lines[start_idx:end_idx]
                
                books_found[book_key]['matches'].append({
                    'page_number': page.page_number,
                    'matched_chunk': page_chunks[idx],
                    'context': '\n'.join(extended_context),
                    'context_range': f"Lines {start_idx + 1}-{end_idx}",
                    'similarity_score': float(similarity_score),
                    'chunk_range': f"Lines {metadata['chunk_start_line']}-{metadata['chunk_end_line']}",
                    'confidence_score': page.confidence_score,
                    'match_type': 'semantic'
                })
        
        enhanced_results = []
        for book_data in books_found.values():
            # Sort by similarity score
            book_data['matches'].sort(key=lambda x: x['similarity_score'], reverse=True)
            # Limit matches per book to avoid overwhelming results
            book_data['matches'] = book_data['matches'][:5]
            enhanced_results.append(book_data)
        
        # Sort books by highest similarity score
        enhanced_results.sort(key=lambda x: max(m['similarity_score'] for m in x['matches']), reverse=True)
        
        return enhanced_results