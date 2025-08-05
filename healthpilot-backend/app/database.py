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
    
    def create_user_profile(self, user_id: str, email: str, age: Optional[int] = None, sex: Optional[str] = None, 
                          weight: Optional[float] = None, height: Optional[float] = None,
                          weight_unit: Optional[str] = None, height_unit: Optional[str] = None,
                          medical_conditions: Optional[list] = None, medications: Optional[list] = None,
                          lifestyle_factors: Optional[list] = None):
        """Create user profile"""
        try:
            # Generate a proper UUID for the profile
            import uuid
            profile_id = str(uuid.uuid4())
            
            data = {
                "id": profile_id,
                "supabase_user_id": user_id,  # Link to Supabase Auth user
                "email": email,
                "age": age,
                "sex": sex,
                "weight": weight,
                "height": height,
                "weight_unit": weight_unit,
                "height_unit": height_unit,
                "medical_conditions": medical_conditions,
                "medications": medications,
                "lifestyle_factors": lifestyle_factors
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
            # First, try to get an existing profile by Supabase Auth user ID
            profile = None
            
            # Try to find profile by Supabase Auth user ID
            try:
                response = self.supabase.table("profiles").select("*").eq("supabase_user_id", user_id).execute()
                if response.data:
                    profile = response.data[0]
                    logger.info(f"Found existing profile: {profile['id']}")
                else:
                    logger.info(f"No profile found for Supabase user ID: {user_id}")
            except Exception as e:
                logger.info(f"Error finding profile by Supabase user ID: {e}")
            
            # If no profile found, create a new one
            if not profile:
                try:
                    # Get user email from Supabase Auth
                    auth_response = self.supabase.auth.admin.get_user(user_id)
                    email = auth_response.user.email if auth_response.user else f"{user_id}@example.com"
                    
                    profile = self.create_user_profile(user_id, email)
                    logger.info(f"Created new profile: {profile['id'] if profile else None}")
                except Exception as e:
                    logger.error(f"Error creating profile: {e}")
                    # Fallback: create profile with basic info
                    profile = self.create_user_profile(user_id, f"{user_id}@example.com")
            
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
            # Save analysis to analyses table
            analysis_data = {
                "report_id": report_id,
                "ocr_text": ocr_result.get("text", ""),
                "ocr_confidence": ocr_result.get("average_confidence", 0),
                "analysis_result": analysis_result or {},
                "status": "completed"
            }
            analysis_response = self.supabase.table("analyses").insert(analysis_data).execute()
            
            # Update report status to completed
            report_update_data = {
                "status": "completed",
                "summary": analysis_result.get("summary", "") if analysis_result else "",
                "risk_level": analysis_result.get("risk_assessment", {}).get("risk_level", "") if analysis_result else "",
                "abnormal_count": analysis_result.get("abnormal_count", 0) if analysis_result else 0,
                "critical_count": analysis_result.get("critical_count", 0) if analysis_result else 0
            }
            report_response = self.supabase.table("reports").update(report_update_data).eq("id", report_id).execute()
            
            logger.info(f"Analysis saved and report updated: {report_id}")
            return analysis_response.data[0] if analysis_response.data else None
        except Exception as e:
            logger.error(f"Error saving analysis: {e}")
            return None