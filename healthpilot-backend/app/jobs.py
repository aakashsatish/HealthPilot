import time
from datetime import datetime
from .ocr_service import OCRService
from .upload_service import UploadService

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
    upload_service = UploadService()
    
    try:
        # Initialize OCR service
        ocr_service = OCRService()
        
        # Extract text from file
        ocr_result = ocr_service.process_file(file_path)
        
        if not ocr_result["success"]:
            # Cleanup file even if OCR failed
            upload_service.cleanup_temp_file(file_path)
            return {
                "status": "failed",
                "error": ocr_result.get("error", "OCR processing failed"),
                "file_path": file_path,
                "timestamp": datetime.now().isoformat()
            }
        
        # Cleanup temporary file after successful processing
        upload_service.cleanup_temp_file(file_path)
        
        return {
            "status": "completed",
            "file_path": file_path,
            "extracted_text": ocr_result["text"],
            "confidence": ocr_result.get("average_confidence", 0),
            "pages": ocr_result.get("pages", 1),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        # Cleanup file on any error
        upload_service.cleanup_temp_file(file_path)
        return {
            "status": "failed",
            "error": str(e),
            "file_path": file_path,
            "timestamp": datetime.now().isoformat()
        }