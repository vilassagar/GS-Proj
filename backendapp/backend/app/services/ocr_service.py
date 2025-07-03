# ocr_service.py
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import re
from typing import List, Dict
import os

class MarathiOCRService:
    def __init__(self):
        # Configure Tesseract for Marathi
        self.tesseract_config = r'--oem 3 --psm 6 -l mar+eng'
        
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict]:
        """Extract text from each page of PDF"""
        pages = convert_from_path(pdf_path, dpi=300)
        extracted_data = []
        
        for page_num, page in enumerate(pages, 1):
            # Preprocess image for better OCR
            page = self.preprocess_image(page)
            
            # Extract text
            text = pytesseract.image_to_string(page, config=self.tesseract_config)
            
            # Extract with bounding boxes for positional search
            boxes = pytesseract.image_to_data(page, config=self.tesseract_config, output_type=pytesseract.Output.DICT)
            
            extracted_data.append({
                'page_number': page_num,
                'text': self.clean_marathi_text(text),
                'boxes': boxes,
                'confidence': self.calculate_confidence(boxes)
            })
            
        return extracted_data
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """Enhance image quality for better OCR"""
        # Convert to grayscale
        image = image.convert('L')
        
        # Increase contrast
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Resize if too small
        width, height = image.size
        if width < 1000:
            scale = 1000 / width
            image = image.resize((int(width * scale), int(height * scale)))
            
        return image
    
    def clean_marathi_text(self, text: str) -> str:
        """Clean and normalize Marathi text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove non-Marathi/English characters (keep Devanagari range)
        text = re.sub(r'[^\u0900-\u097F\u0020-\u007E\s]', '', text)
        
        return text
    
    def calculate_confidence(self, boxes: Dict) -> float:
        """Calculate average confidence score"""
        confidences = [int(conf) for conf in boxes['conf'] if int(conf) > 0]
        return sum(confidences) / len(confidences) if confidences else 0