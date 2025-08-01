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


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
upload_service = UploadService()

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

@app.post("/auth/profile")
async def create_profile(request: UploadRequest):
    """Create or update user profile"""
    # Generate a new UUID for the user
    import uuid
    user_id = str(uuid.uuid4())
    
    profile = db_service.create_user_profile(
        user_id, 
        request.email, 
        request.age, 
        request.sex
    )
    return {"profile": profile, "user_id": user_id}

@app.get("/auth/profile/{user_id}")
async def get_profile(user_id: str):
    """Get user profile"""
    profile = db_service.get_user_by_id(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"profile": profile}

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
        # Save the uploaded file
        upload_result = await upload_service.save_uploaded_file(file)
        
        # Save to database
        report = db_service.save_lab_report(
            user_id, 
            upload_result["file_path"], 
            upload_result["original_filename"]
        )
        
        # Enqueue processing job with report ID
        job_result = enqueue_lab_report_job(upload_result["file_path"], report["id"])
        
        return {
            "upload": upload_result,
            "report": report,
            "job": job_result,
            "message": "File uploaded and processing started"
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail="Upload failed")

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