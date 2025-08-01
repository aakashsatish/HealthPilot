import time
from datetime import datetime
from dotenv import load_dotenv
from .ocr_service import OCRService
from .upload_service import UploadService
from .analysis_engine import AnalysisEngine
from .database import DatabaseService  # Add this import
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

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

def process_lab_report_job(file_path: str, report_id: str):
    """Process uploaded lab report with OCR and analysis"""
    upload_service = UploadService()
    db_service = DatabaseService()
    
    try:
        # Initialize services
        ocr_service = OCRService()
        analysis_engine = AnalysisEngine()
        
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
        
        # Analyze the lab results
        analysis_result = analysis_engine.analyze_lab_report(ocr_result["text"])
        
        # Save analysis result to database
        analysis = db_service.save_analysis_result(report_id, ocr_result, analysis_result)
        
        # Cleanup temporary file after successful processing
        upload_service.cleanup_temp_file(file_path)
        
        return {
            "status": "completed",
            "file_path": file_path,
            "report_id": report_id,
            "analysis_id": analysis["id"] if analysis else None,
            "extracted_text": ocr_result["text"],
            "confidence": ocr_result.get("average_confidence", 0),
            "pages": ocr_result.get("pages", 1),
            "analysis": analysis_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        # Cleanup file on any error
        upload_service.cleanup_temp_file(file_path)
        logger.error(f"Job failed: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "file_path": file_path,
            "timestamp": datetime.now().isoformat()
        }