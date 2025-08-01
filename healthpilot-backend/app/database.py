import os
from supabase import create_client, Client
from typing import Optional
import logging
import uuid

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        """Initialize Supabase client"""
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        
        self.supabase: Client = create_client(url, key)
        logger.info("Supabase client initialized")
    
    def get_user_by_id(self, user_id: str):
        """Get user by ID"""
        try:
            response = self.supabase.table("profiles").select("*").eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None
    
    def create_user_profile(self, user_id: str, email: str, age: Optional[int] = None, sex: Optional[str] = None):
        """Create user profile"""
        try:
            data = {
                "email": email,
                "age": age,
                "sex": sex
            }
            logger.info(f"Creating profile with data: {data}")
            
            # Test the Supabase connection first
            logger.info(f"Supabase URL: {self.supabase.supabase_url}")
            
            response = self.supabase.table("profiles").insert(data).execute()
            logger.info(f"Supabase response: {response}")
            logger.info(f"Response data: {response.data}")
            logger.info(f"Response error: {getattr(response, 'error', None)}")
            
            if response.data:
                logger.info(f"Successfully created profile: {response.data[0]}")
                return response.data[0]
            else:
                logger.error(f"No data returned from Supabase: {response}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating user profile: {e}")
            logger.error(f"Error type: {type(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
    
    def save_lab_report(self, user_id: str, file_path: str, original_filename: str):
        """Save lab report metadata"""
        try:
            data = {
                "profile_id": user_id,
                "file_path": file_path,
                "original_filename": original_filename,
                "status": "uploaded"
            }
            response = self.supabase.table("reports").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error saving lab report: {e}")
            return None
    
    def save_analysis_result(self, report_id: str, ocr_result: dict, analysis_result: dict = None):
        """Save analysis results"""
        try:
            data = {
                "report_id": report_id,
                "ocr_text": ocr_result.get("text", ""),
                "ocr_confidence": ocr_result.get("average_confidence", 0),
                "analysis_result": analysis_result or {},
                "status": "completed"
            }
            response = self.supabase.table("analyses").insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error saving analysis: {e}")
            return None