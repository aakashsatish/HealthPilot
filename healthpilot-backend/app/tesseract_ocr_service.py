import os
import tempfile
from typing import List, Dict, Optional
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class TesseractOCRService:
    def __init__(self):
        """Initialize Tesseract OCR service"""
        try:
            # Test if tesseract is available
            pytesseract.get_tesseract_version()
            logger.info("Tesseract OCR initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Tesseract OCR: {e}")
            raise
    
    def extract_text_from_image(self, image_path: str) -> Dict:
        """Extract text from an image file using Tesseract"""
        try:
            # Open the image
            image = Image.open(image_path)
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(image)
            
            # For Tesseract, we don't have confidence scores, so we'll use a default
            lines = text.split('\n')
            confidence_scores = [0.8] * len(lines)  # Default confidence
            
            return {
                "text": text,
                "lines": lines,
                "confidence_scores": confidence_scores,
                "average_confidence": 0.8,
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
            logger.info(f"Starting PDF processing for: {pdf_path}")
            logger.info(f"PDF file exists: {os.path.exists(pdf_path)}")
            
            # Convert PDF to images
            logger.info("Converting PDF to images...")
            images = convert_from_path(
                pdf_path,
                dpi=150,  # Lower DPI to reduce memory usage
                fmt='PNG',
                thread_count=1  # Single thread to reduce memory usage
            )
            logger.info(f"PDF converted to {len(images)} images")
            
            all_text = []
            all_confidence_scores = []
            
            for i, image in enumerate(images):
                logger.info(f"Processing page {i+1}/{len(images)}")
                
                # Resize image to reduce memory usage if it's too large
                max_size = (2000, 2000)  # Maximum dimensions
                if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                    image.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Save image temporarily
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                    image.save(tmp_file.name, 'PNG', optimize=True)
                    tmp_path = tmp_file.name
                
                try:
                    # Extract text from this page
                    page_result = self.extract_text_from_image(tmp_path)
                    if page_result["success"]:
                        all_text.append(f"--- Page {i+1} ---\n{page_result['text']}")
                        all_confidence_scores.extend(page_result["confidence_scores"])
                        logger.info(f"Page {i+1} text extracted: {len(page_result['text'])} chars")
                    else:
                        logger.warning(f"Page {i+1} OCR failed: {page_result.get('error', 'Unknown error')}")
                    
                    # Clear image from memory
                    image.close()
                    
                finally:
                    # Clean up temporary file
                    try:
                        os.unlink(tmp_path)
                    except:
                        pass
            
            final_text = "\n\n".join(all_text)
            logger.info(f"PDF processing completed. Total text length: {len(final_text)}")
            
            return {
                "text": final_text,
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