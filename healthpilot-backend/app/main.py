from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
from .queue import enqueue_test_job, enqueue_upload_job, enqueue_lab_report_job
from rq import Queue
from redis import Redis



# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

