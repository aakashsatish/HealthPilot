from app.ocr_service import OCRService
import os

def test_ocr():
    ocr = OCRService()
    
    # Test with the PDF that was uploaded
    pdf_path = "uploads/temp/20250803_012523_11706120-bd65-4de0-8b9d-99f39363231a.pdf"
    
    if os.path.exists(pdf_path):
        print(f"Testing OCR with PDF: {pdf_path}")
        result = ocr.extract_text_from_pdf(pdf_path)
        print("OCR Result:")
        print(f"Success: {result['success']}")
        print(f"Pages: {result.get('pages', 0)}")
        print(f"Text length: {len(result['text'])}")
        print(f"First 500 chars: {result['text'][:500]}")
        if not result['success']:
            print(f"Error: {result.get('error', 'Unknown error')}")
    else:
        print(f"PDF file not found: {pdf_path}")

if __name__ == "__main__":
    test_ocr()