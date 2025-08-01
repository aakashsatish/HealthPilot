from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ReferenceRange:
    low: float
    high: float
    unit: str
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    sex: Optional[str] = None

class ReferenceRanges:
    def __init__(self):
        self.ranges = {
            # Complete Blood Count (CBC)
            "hemoglobin": {
                "male": ReferenceRange(13.5, 17.5, "g/dL"),
                "female": ReferenceRange(12.0, 15.5, "g/dL")
            },
            "hematocrit": {
                "male": ReferenceRange(41.0, 50.0, "%"),
                "female": ReferenceRange(36.0, 46.0, "%")
            },
            "white_blood_cells": ReferenceRange(4.5, 11.0, "K/uL"),
            "platelets": ReferenceRange(150, 450, "K/uL"),
            "red_blood_cells": ReferenceRange(4.5, 5.9, "M/uL"),
            
            # Comprehensive Metabolic Panel (CMP)
            "glucose": ReferenceRange(70, 100, "mg/dL"),
            "creatinine": ReferenceRange(0.7, 1.3, "mg/dL"),
            "bun": ReferenceRange(7, 20, "mg/dL"),
            "sodium": ReferenceRange(135, 145, "mEq/L"),
            "potassium": ReferenceRange(3.5, 5.0, "mEq/L"),
            "chloride": ReferenceRange(96, 106, "mEq/L"),
            "co2": ReferenceRange(22, 28, "mEq/L"),
            "calcium": ReferenceRange(8.5, 10.5, "mg/dL"),
            "total_protein": ReferenceRange(6.0, 8.3, "g/dL"),
            "albumin": ReferenceRange(3.4, 5.4, "g/dL"),
            "total_bilirubin": ReferenceRange(0.3, 1.2, "mg/dL"),
            "alkaline_phosphatase": ReferenceRange(44, 147, "U/L"),
            "alt": ReferenceRange(7, 55, "U/L"),
            "ast": ReferenceRange(8, 48, "U/L"),
            
            # Lipids
            "total_cholesterol": ReferenceRange(0, 200, "mg/dL"),
            "hdl": ReferenceRange(40, 60, "mg/dL"),
            "ldl": ReferenceRange(0, 100, "mg/dL"),
            "triglycerides": ReferenceRange(0, 150, "mg/dL"),
            
            # Diabetes
            "hba1c": ReferenceRange(4.0, 5.6, "%"),
            
            # Thyroid
            "tsh": ReferenceRange(0.4, 4.0, "mIU/L"),
            "t4": ReferenceRange(0.8, 1.8, "ng/dL"),
        }
    
    def get_range(self, test_name: str, age: Optional[int] = None, sex: Optional[str] = None) -> Optional[ReferenceRange]:
        """Get reference range for a test"""
        test_name = test_name.lower().replace(" ", "_")
        
        if test_name in self.ranges:
            range_data = self.ranges[test_name]
            
            if isinstance(range_data, dict):
                # Sex-specific ranges
                if sex and sex.lower() in range_data:
                    return range_data[sex.lower()]
                elif "male" in range_data:
                    return range_data["male"]  # Default to male
            else:
                return range_data
        
        return None
    
    def classify_value(self, test_name: str, value: float, unit: str, age: Optional[int] = None, sex: Optional[str] = None) -> Dict[str, Any]:
        """Classify a lab value as Normal, Low, High, or Critical"""
        ref_range = self.get_range(test_name, age, sex)
        
        if not ref_range:
            return {
                "classification": "UNKNOWN",
                "status": "No reference range available",
                "reference_range": None
            }
        
        # Convert units if needed
        converted_value = self._convert_units(value, unit, ref_range.unit)
        
        if converted_value < ref_range.low:
            if converted_value < ref_range.low * 0.5:  # Very low
                classification = "CRITICAL_LOW"
            else:
                classification = "LOW"
        elif converted_value > ref_range.high:
            if converted_value > ref_range.high * 2:  # Very high
                classification = "CRITICAL_HIGH"
            else:
                classification = "HIGH"
        else:
            classification = "NORMAL"
        
        return {
            "classification": classification,
            "value": converted_value,
            "unit": ref_range.unit,
            "reference_range": f"{ref_range.low}-{ref_range.high} {ref_range.unit}",
            "status": self._get_status_message(classification, test_name)
        }
    
    def _convert_units(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert between common lab units"""
        # Add common unit conversions here
        if from_unit.lower() == "mg/dl" and to_unit.lower() == "mmol/l":
            return value * 0.0555  # For glucose
        elif from_unit.lower() == "mmol/l" and to_unit.lower() == "mg/dl":
            return value * 18.0  # For glucose
        return value
    
    def _get_status_message(self, classification: str, test_name: str) -> str:
        """Get human-readable status message"""
        messages = {
            "NORMAL": "Within normal range",
            "LOW": "Below normal range",
            "HIGH": "Above normal range",
            "CRITICAL_LOW": "Critically low - requires immediate attention",
            "CRITICAL_HIGH": "Critically high - requires immediate attention"
        }
        return messages.get(classification, "Unknown status")
