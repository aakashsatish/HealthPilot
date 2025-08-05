from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse
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
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import tempfile
import os


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
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
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
    """Download a report as a PDF file"""
    try:
        # Get report details
        report = history_service.get_report_details(report_id)
        logger.info(f"Download request for report {report_id}, report data: {report}")
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Check if report has required data
        if not isinstance(report, dict):
            logger.error(f"Report data is not a dictionary: {type(report)}")
            raise HTTPException(status_code=500, detail="Invalid report data format")
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        title = Paragraph("HealthPilot Lab Report Analysis", title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Report Information
        info_style = ParagraphStyle(
            'Info',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=6
        )
        
        story.append(Paragraph(f"<b>Report ID:</b> {report_id}", info_style))
        story.append(Paragraph(f"<b>Original File:</b> {report.get('original_filename', 'Unknown')}", info_style))
        story.append(Paragraph(f"<b>Upload Date:</b> {report.get('created_at', 'Unknown')}", info_style))
        if report.get('lab_name'):
            story.append(Paragraph(f"<b>Laboratory:</b> {report.get('lab_name')}", info_style))
        story.append(Spacer(1, 20))
        
        # Risk Level
        risk_level = report.get('risk_level', 'UNKNOWN')
        risk_color = {
            'HIGH': colors.red,
            'MODERATE': colors.orange,
            'LOW': colors.green,
            'UNKNOWN': colors.grey
        }.get(risk_level, colors.grey)
        
        risk_style = ParagraphStyle(
            'Risk',
            parent=styles['Normal'],
            fontSize=14,
            spaceAfter=20,
            textColor=risk_color
        )
        story.append(Paragraph(f"<b>Risk Level:</b> {risk_level}", risk_style))
        
        # Summary Statistics
        story.append(Paragraph("<b>Summary Statistics:</b>", info_style))
        story.append(Paragraph(f"• Abnormal Results: {report.get('abnormal_count', 0)}", info_style))
        story.append(Paragraph(f"• Critical Results: {report.get('critical_count', 0)}", info_style))
        story.append(Spacer(1, 20))
        
        # Analysis Summary
        if report.get('summary'):
            story.append(Paragraph("<b>Analysis Summary:</b>", info_style))
            summary_style = ParagraphStyle(
                'Summary',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=20,
                leftIndent=20
            )
            story.append(Paragraph(report.get('summary'), summary_style))
        else:
            story.append(Paragraph("<b>Analysis Summary:</b>", info_style))
            story.append(Paragraph("Report is still being processed. Analysis will be available soon.", info_style))
        
        # Lab Results Table
        analysis_result = report.get('analysis_result')
        if analysis_result and isinstance(analysis_result, dict) and analysis_result.get('results'):
            story.append(Paragraph("<b>Lab Results:</b>", info_style))
            story.append(Spacer(1, 10))
            
            # Create table data
            table_data = [['Test', 'Value', 'Reference Range', 'Status']]
            for result in analysis_result.get('results', []):
                status_color = {
                    'NORMAL': colors.green,
                    'HIGH': colors.orange,
                    'LOW': colors.orange,
                    'CRITICAL': colors.red
                }.get(result.get('classification', 'UNKNOWN'), colors.grey)
                
                table_data.append([
                    result.get('original_name', 'Unknown'),
                    f"{result.get('value', 'N/A')} {result.get('unit', '')}",
                    result.get('reference_range', 'N/A'),
                    result.get('classification', 'UNKNOWN')
                ])
            
            # Create table
            table = Table(table_data, colWidths=[2*inch, 1.5*inch, 2*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            story.append(table)
        else:
            story.append(Paragraph("<b>Lab Results:</b>", info_style))
            story.append(Paragraph("Lab results are being processed and will be available soon.", info_style))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=1
        )
        story.append(Paragraph(f"Generated by HealthPilot on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}", footer_style))
        
        # Build PDF
        doc.build(story)
        pdf_data = buffer.getvalue()
        buffer.close()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_data)
            tmp_file_path = tmp_file.name
        
        # Create filename with date
        upload_date = report.get('created_at')
        if upload_date:
            try:
                # Parse the date string and format it
                if isinstance(upload_date, str):
                    date_obj = datetime.fromisoformat(upload_date.replace('Z', '+00:00'))
                else:
                    date_obj = upload_date
                date_str = date_obj.strftime('%Y-%m-%d')
            except:
                date_str = datetime.now().strftime('%Y-%m-%d')
        else:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        filename = f"lab_report_{date_str}.pdf"
        
        # Return file response
        return FileResponse(
            path=tmp_file_path,
            filename=filename,
            media_type='application/pdf'
        )
        
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