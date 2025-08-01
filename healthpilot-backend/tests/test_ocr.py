import os
import tempfile
from app.ocr_service import OCRService

def test_ocr_initialization():
    """Test that OCR service initializes correctly"""
    try:
        ocr = OCRService()
        print("✅ OCR service initialized successfully")
        return True
    except Exception as e:
        print(f"❌ OCR initialization failed: {e}")
        return False

if __name__ == "__main__":
    test_ocr_initialization()