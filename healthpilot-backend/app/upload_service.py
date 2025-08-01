import os
import uuid
import aiofiles
from datetime import datetime
from typing import Optional, Dict
from fastapi import UploadFile, HTTPException
import logging

logger = logging.getLogger(__name__)

class UploadService:
    def __init__(self, upload_dir: str = "uploads/temp"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)
    
    def _generate_filename(self, original_filename: str) -> str:
        """Generate unique filename"""
        ext = os.path.splitext(original_filename)[1]
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{timestamp}_{unique_id}{ext}"
    
    def _validate_file_type(self, filename: str) -> bool:
        """Validate file type is supported"""
        allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.txt'}
        ext = os.path.splitext(filename.lower())[1]
        return ext in allowed_extensions
    
    def _validate_file_size(self, file_size: int, max_size_mb: int = 10) -> bool:
        """Validate file size"""
        max_size_bytes = max_size_mb * 1024 * 1024
        return file_size <= max_size_bytes
    
    async def save_uploaded_file(self, file: UploadFile) -> Dict:
        """Save uploaded file and return metadata"""
        try:
            # Validate file type
            if not self._validate_file_type(file.filename):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Unsupported file type. Allowed: PDF, PNG, JPG, JPEG, TIFF, BMP, TXT"
                )
            
            # Validate file size (10MB max)
            if not self._validate_file_size(file.size, max_size_mb=10):
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large. Maximum size: 10MB"
                )
            
            # Generate unique filename
            filename = self._generate_filename(file.filename)
            file_path = os.path.join(self.upload_dir, filename)
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            logger.info(f"File saved: {file_path} (size: {len(content)} bytes)")
            
            return {
                "original_filename": file.filename,
                "saved_filename": filename,
                "file_path": file_path,
                "file_size": len(content),
                "uploaded_at": datetime.now().isoformat(),
                "success": True
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"File upload failed: {e}")
            raise HTTPException(status_code=500, detail="File upload failed")
    
    def cleanup_temp_file(self, file_path: str) -> bool:
        """Clean up temporary file after processing"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up: {file_path}")
                return True
        except Exception as e:
            logger.error(f"Failed to cleanup {file_path}: {e}")
        return False