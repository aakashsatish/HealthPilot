import os
import tempfile
from typing import List, Dict, Optional
from paddleocr import PaddleOCR
from pdf2image import convert_from_path
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        """Initialize PaddleOCR with English language"""
        try:
            self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
            logger.info("PaddleOCR initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize PaddleOCR: {e}")
            raise
    
    def extract_text_from_image(self, image_path: str) -> Dict:
        """Extract text from an image file"""
        try:
            result = self.ocr.ocr(image_path, cls=True)
            
            # Extract text from OCR result
            extracted_text = []
            confidence_scores = []
            
            for line in result:
                for word_info in line:
                    text = word_info[1][0]  # The text
                    confidence = word_info[1][1]  # Confidence score
                    extracted_text.append(text)
                    confidence_scores.append(confidence)
            
            return {
                "text": " ".join(extracted_text),
                "lines": extracted_text,
                "confidence_scores": confidence_scores,
                "average_confidence": sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"OCR failed for {image_path}: {e}")
            return {
                "text": "",
                "lines": [],
                "confidence_scores": [],
                "average_confidence": 0,
                "success": False,
                "error": str(e)
            }
    
    def extract_text_from_pdf(self, pdf_path: str) -> Dict:
        """Extract text from PDF by converting to images first"""
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path)
            
            all_text = []
            all_confidence_scores = []
            
            for i, image in enumerate(images):
                # Save image temporarily
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                    image.save(tmp_file.name, 'PNG')
                    tmp_path = tmp_file.name
                
                try:
                    # Extract text from this page
                    page_result = self.extract_text_from_image(tmp_path)
                    if page_result["success"]:
                        all_text.append(f"--- Page {i+1} ---\n{page_result['text']}")
                        all_confidence_scores.extend(page_result["confidence_scores"])
                finally:
                    # Clean up temporary file
                    os.unlink(tmp_path)
            
            return {
                "text": "\n\n".join(all_text),
                "pages": len(images),
                "average_confidence": sum(all_confidence_scores) / len(all_confidence_scores) if all_confidence_scores else 0,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"PDF processing failed for {pdf_path}: {e}")
            return {
                "text": "",
                "pages": 0,
                "average_confidence": 0,
                "success": False,
                "error": str(e)
            }
    
    def process_file(self, file_path: str) -> Dict:
        """Process any file (PDF, image, or text) and extract text"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            return self.extract_text_from_image(file_path)
        elif file_ext == '.txt':
            # For text files, just read the content directly
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                return {
                    "text": text,
                    "lines": text.split('\n'),
                    "confidence_scores": [1.0] * len(text.split('\n')),  # Perfect confidence for text files
                    "average_confidence": 1.0,
                    "success": True
                }
            except Exception as e:
                return {
                    "text": "",
                    "lines": [],
                    "confidence_scores": [],
                    "average_confidence": 0,
                    "success": False,
                    "error": str(e)
                }
        else:
            return {
                "text": "",
                "success": False,
                "error": f"Unsupported file type: {file_ext}"
            }