import time
from datetime import datetime
from .ocr_service import OCRService

def test_job(name="World"):
    """Simple test job"""
    time.sleep(2)  # Simulate work
    return f"Hello {name}! Job completed at {datetime.now().isoformat()}"

def process_upload_job(file_path):
    """Process uploaded file (placeholder for now)"""
    time.sleep(3)  # Simulate OCR processing
    return {
        "file_path": file_path,
        "status": "processed",
        "timestamp": datetime.now().isoformat()
    }

def process_lab_report_job(file_path: str):
    """Process uploaded lab report with OCR"""
    try:
        # Initialize OCR service
        ocr_service = OCRService()
        
        # Extract text from file
        ocr_result = ocr_service.process_file(file_path)
        
        if not ocr_result["success"]:
            return {
                "status": "failed",
                "error": ocr_result.get("error", "OCR processing failed"),
                "file_path": file_path,
                "timestamp": datetime.now().isoformat()
            }
        
        # For now, just return the extracted text
        # Later we'll add analysis logic here
        return {
            "status": "completed",
            "file_path": file_path,
            "extracted_text": ocr_result["text"],
            "confidence": ocr_result.get("average_confidence", 0),
            "pages": ocr_result.get("pages", 1),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "file_path": file_path,
            "timestamp": datetime.now().isoformat()
        }