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
            # Generate a proper UUID for the profile
            import uuid
            profile_id = str(uuid.uuid4())
            
            data = {
                "id": profile_id,
                "email": email,
                "age": age,
                "sex": sex
            }
            
            logger.info(f"Creating profile with data: {data}")
            response = self.supabase.table("profiles").insert(data).execute()
            logger.info(f"Supabase response: {response}")
            
            if response.data:
                return response.data[0]
            else:
                logger.error(f"No data returned from Supabase: {response}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating user profile: {e}")
            return None
    
    def save_lab_report(self, user_id: str, file_path: str, original_filename: str):
        """Save lab report metadata"""
        try:
            # First, try to get an existing profile by email
            profile = None
            
            # Try to find profile by email first
            try:
                email = f"{user_id}@example.com"
                response = self.supabase.table("profiles").select("*").eq("email", email).execute()
                if response.data:
                    profile = response.data[0]
                    logger.info(f"Found existing profile: {profile['id']}")
            except Exception as e:
                logger.info(f"Error finding profile by email: {e}")
            
            # If no profile found, create a new one with a unique email
            if not profile:
                try:
                    import uuid
                    unique_id = str(uuid.uuid4())[:8]  # Use first 8 chars of UUID
                    email = f"{user_id}-{unique_id}@example.com"
                    profile = self.create_user_profile(user_id, email)
                    logger.info(f"Created new profile: {profile['id'] if profile else None}")
                except Exception as e:
                    logger.error(f"Error creating profile: {e}")
            
            if not profile:
                logger.error("Failed to create or find profile")
                return None
            
            data = {
                "profile_id": profile["id"],  # Use the actual UUID from the profile
                "file_path": file_path,
                "original_filename": original_filename,
                "status": "uploaded"
            }
            
            logger.info(f"Saving lab report with data: {data}")
            response = self.supabase.table("reports").insert(data).execute()
            logger.info(f"Supabase response: {response}")
            
            if response.data:
                return response.data[0]
            else:
                logger.error(f"No data returned from Supabase: {response}")
                return None
                
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