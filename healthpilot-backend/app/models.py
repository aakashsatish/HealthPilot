from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class UserProfile(BaseModel):
    id: str
    email: str
    age: Optional[int] = None
    sex: Optional[str] = None
    weight: Optional[float] = None  # in kg
    height: Optional[float] = None  # in cm
    weight_unit: Optional[str] = None  # kg or lbs
    height_unit: Optional[str] = None  # cm or ft
    medical_conditions: Optional[list[str]] = None
    medications: Optional[list[str]] = None
    lifestyle_factors: Optional[list[str]] = None
    created_at: Optional[datetime] = None

class LabReport(BaseModel):
    id: Optional[str] = None
    profile_id: str
    file_path: str
    original_filename: str
    status: str = "uploaded"
    created_at: Optional[datetime] = None

class AnalysisResult(BaseModel):
    id: Optional[str] = None
    report_id: str
    ocr_text: str
    ocr_confidence: float
    analysis_result: Dict[str, Any] = {}
    status: str = "completed"
    created_at: Optional[datetime] = None

class UploadRequest(BaseModel):
    user_id: str
    email: str
    age: Optional[int] = None
    sex: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    weight_unit: Optional[str] = None
    height_unit: Optional[str] = None
    medical_conditions: Optional[list[str]] = None
    medications: Optional[list[str]] = None
    lifestyle_factors: Optional[list[str]] = None