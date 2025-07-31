import time
from datetime import datetime

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