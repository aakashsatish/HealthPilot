from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from .upload_service import UploadService
from .queue import enqueue_lab_report_job
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
from .queue import enqueue_test_job, enqueue_upload_job, enqueue_lab_report_job
from rq import Queue
from redis import Redis
from .database import DatabaseService
from .auth import AuthService
from .models import UploadRequest
from fastapi import Depends, Form
from typing import Optional
from .analysis_engine import AnalysisEngine
from .history_service import HistoryService
from .email_service import EmailService


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
upload_service = UploadService()
history_service = HistoryService()

app = FastAPI(
    title="HealthPilot API",
    description="Blood test report analysis service",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "healthpilot-api"
    }

@app.post("/jobs/test")
async def create_test_job(name: str = "World"):
    """Create a test background job"""
    result = enqueue_test_job(name)
    return result

@app.post("/upload/lab-report")
async def upload_lab_report(file_path: str):
    """Upload a lab report for processing"""
    result = enqueue_lab_report_job(file_path)
    return result

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Get job status"""
    redis_conn = Redis(host='localhost', port=6379, db=0)
    queue = Queue('default', connection=redis_conn)
    job = queue.fetch_job(job_id)
    
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "job_id": job.id,
        "status": job.get_status(),
        "result": job.result if job.is_finished else None,
        "created_at": job.created_at.isoformat() if job.created_at else None
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "HealthPilot API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Initialize services
db_service = DatabaseService()
auth_service = AuthService(db_service.supabase)
email_service = EmailService()

@app.post("/auth/profile")
async def create_profile(request: UploadRequest):
    """Create or update user profile"""
    try:
        # Check if profile already exists
        existing_profile = None
        try:
            response = db_service.supabase.table("profiles").select("*").eq("supabase_user_id", request.user_id).execute()
            if response.data:
                existing_profile = response.data[0]
        except Exception as e:
            logger.info(f"Error finding existing profile: {e}")
        
        if existing_profile:
            # Update existing profile
            update_data = {
                "email": request.email,
                "age": request.age,
                "sex": request.sex,
                "weight": request.weight,
                "height": request.height,
                "weight_unit": request.weight_unit,
                "height_unit": request.height_unit,
                "medical_conditions": request.medical_conditions,
                "medications": request.medications,
                "lifestyle_factors": request.lifestyle_factors
            }
            
            response = db_service.supabase.table("profiles").update(update_data).eq("id", existing_profile["id"]).execute()
            
            if response.data:
                return {
                    "success": True,
                    "profile": response.data[0],
                    "message": "Profile updated successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to update profile"
                }
        else:
            # Create new profile
            profile = db_service.create_user_profile(
                user_id=request.user_id,
                email=request.email,
                age=request.age,
                sex=request.sex,
                weight=request.weight,
                height=request.height,
                weight_unit=request.weight_unit,
                height_unit=request.height_unit,
                medical_conditions=request.medical_conditions,
                medications=request.medications,
                lifestyle_factors=request.lifestyle_factors
            )
            
            if profile:
                return {
                    "success": True,
                    "profile": profile,
                    "message": "Profile created successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to create profile"
                }
    except Exception as e:
        logger.error(f"Error creating/updating profile: {e}")
        return {
            "success": False,
            "message": f"Error creating/updating profile: {str(e)}"
        }

@app.get("/auth/profile/{user_id}")
async def get_profile(user_id: str):
    """Get user profile"""
    try:
        # Try to find profile by Supabase Auth user ID
        response = db_service.supabase.table("profiles").select("*").eq("supabase_user_id", user_id).execute()
        
        if response.data:
            return {
                "success": True,
                "profile": response.data[0]
            }
        else:
            return {
                "success": False,
                "message": "Profile not found"
            }
    except Exception as e:
        logger.error(f"Error getting profile: {e}")
        return {
            "success": False,
            "message": f"Error getting profile: {str(e)}"
        }

# Update the existing upload endpoint
@app.post("/upload/file")
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    age: Optional[int] = Form(None),
    sex: Optional[str] = Form(None)
):
    """Upload a lab report file for processing"""
    try:
        print(f"DEBUG: Starting upload for user {user_id}")
        
        # Save the uploaded file
        upload_result = await upload_service.save_uploaded_file(file)
        print(f"DEBUG: File saved: {upload_result}")
        
        # Save to database
        print(f"DEBUG: About to save to database...")
        report = db_service.save_lab_report(
            user_id, 
            upload_result["file_path"], 
            upload_result["original_filename"]
        )
        print(f"DEBUG: Report saved: {report}")
        print(f"DEBUG: Report type: {type(report)}")
        
        if not report:
            print(f"DEBUG: Report is None, raising error")
            raise HTTPException(status_code=500, detail="Failed to save report to database")
        
        # Enqueue processing job with report ID
        job_result = enqueue_lab_report_job(upload_result["file_path"], report["id"])
        print(f"DEBUG: Job queued: {job_result}")
        
        return {
            "upload": upload_result,
            "report": report,
            "job": job_result,
            "message": "File uploaded and processing started"
        }
        
    except HTTPException as e:
        print(f"DEBUG: HTTPException: {e}")
        raise e
    except Exception as e:
        print(f"DEBUG: Exception: {e}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.get("/jobs/{job_id}/result")
async def get_job_result(job_id: str):
    """Get detailed job result including OCR text"""
    redis_conn = Redis(host='localhost', port=6379, db=0)
    queue = Queue('default', connection=redis_conn)
    job = queue.fetch_job(job_id)
    
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    
    result = {
        "job_id": job.id,
        "status": job.get_status(),
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "result": job.result if job.is_finished else None
    }
    
    # If job failed, include error info
    if job.is_failed:
        result["error"] = str(job.exc_info)
    
    return result

@app.get("/reports/history/{user_id}")
async def get_user_history(user_id: str):
    """Get user's report history"""
    try:
        # First, get the profile for this Supabase Auth user ID
        db_service = DatabaseService()
        profile = None
        
        try:
            response = db_service.supabase.table("profiles").select("*").eq("supabase_user_id", user_id).execute()
            if response.data:
                profile = response.data[0]
        except Exception as e:
            logger.error(f"Error finding profile for user {user_id}: {e}")
        
        if not profile:
            return {"success": True, "history": []}
        
        history = history_service.get_user_report_history(profile["id"])
        return {"success": True, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reports/{report_id}")
async def get_report_details(report_id: str):
    """Get detailed information for a specific report"""
    try:
        details = history_service.get_report_details(report_id)
        if not details:
            raise HTTPException(status_code=404, detail="Report not found")
        return {"success": True, "report": details}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/reports/{report_id}")
async def delete_report(report_id: str):
    """Delete a specific report and its associated analysis"""
    try:
        # Delete the analysis first (due to foreign key constraints)
        db_service.supabase.table("analyses").delete().eq("report_id", report_id).execute()
        
        # Delete the report
        result = db_service.supabase.table("reports").delete().eq("id", report_id).execute()
        
        if result.data:
            return {"success": True, "message": "Report deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Report not found")
    except Exception as e:
        logger.error(f"Error deleting report {report_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reports/{report_id}/email")
async def email_report(report_id: str, request: dict):
    """Send a report analysis via email"""
    try:
        # Get report details
        report = history_service.get_report_details(report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Get user profile for name
        user_name = "User"
        if report.get("profile_id"):
            try:
                profile_response = db_service.supabase.table("profiles").select("email").eq("id", report["profile_id"]).execute()
                if profile_response.data:
                    user_name = profile_response.data[0].get("email", "User")
            except Exception as e:
                logger.error(f"Error getting user profile: {e}")
        
        # Get email from request body
        email = request.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")
        
        # Send email
        success = email_service.send_report_email(email, report, user_name)
        
        if success:
            return {"success": True, "message": f"Report sent to {email}"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")
            
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error sending report email: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reports/{report_id}/download")
async def download_report(report_id: str):
    """Download a report as a JSON file"""
    try:
        # Get report details
        report = history_service.get_report_details(report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Create a comprehensive report object
        download_data = {
            "report_id": report_id,
            "filename": report.get("original_filename", "lab_report"),
            "upload_date": report.get("created_at"),
            "risk_level": report.get("risk_level"),
            "summary": report.get("summary"),
            "abnormal_count": report.get("abnormal_count", 0),
            "critical_count": report.get("critical_count", 0),
            "lab_name": report.get("lab_name"),
            "analysis_result": report.get("analysis_result", {}),
            "download_timestamp": datetime.utcnow().isoformat()
        }
        
        # Convert to JSON string
        import json
        json_data = json.dumps(download_data, indent=2, default=str)
        
        # Create filename
        filename = f"{report.get('original_filename', 'lab_report')}_{report_id}.json"
        
        return {
            "success": True,
            "filename": filename,
            "data": json_data,
            "content_type": "application/json"
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error downloading report {report_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reports/compare")
async def compare_reports(report_id_1: str, report_id_2: str):
    """Compare two reports"""
    try:
        comparison = history_service.compare_reports(report_id_1, report_id_2)
        return {"success": True, "comparison": comparison}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tests/trends/{profile_id}/{test_name}")
async def get_test_trends(profile_id: str, test_name: str, limit: int = 10):
    """Get trend data for a specific test"""
    try:
        trends = history_service.get_test_trends(profile_id, test_name, limit)
        return {"success": True, "trends": trends}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))