import re
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class LabParser:
    def __init__(self):
        # Common lab test patterns
        self.test_patterns = {
            "hemoglobin": r"hemoglobin|hgb|hb",
            "hematocrit": r"hematocrit|hct",
            "white_blood_cells": r"white\s*blood\s*cells|wbc|leukocytes",
            "platelets": r"platelets|plt",
            "red_blood_cells": r"red\s*blood\s*cells|rbc",
            "glucose": r"glucose|glu",
            "creatinine": r"creatinine|creat",
            "bun": r"bun|blood\s*urea\s*nitrogen",
            "sodium": r"sodium|na",
            "potassium": r"potassium|k",
            "chloride": r"chloride|cl",
            "co2": r"co2|bicarbonate|hco3",
            "calcium": r"calcium|ca",
            "total_protein": r"total\s*protein|tp",
            "albumin": r"albumin|alb",
            "total_bilirubin": r"total\s*bilirubin|tbil",
            "alkaline_phosphatase": r"alkaline\s*phosphatase|alp",
            "alt": r"alt|alanine\s*aminotransferase",
            "ast": r"ast|aspartate\s*aminotransferase",
            "total_cholesterol": r"total\s*cholesterol|chol",
            "hdl": r"hdl|high\s*density\s*lipoprotein",
            "ldl": r"ldl|low\s*density\s*lipoprotein",
            "triglycerides": r"triglycerides|trig",
            "hba1c": r"hba1c|a1c|glycated\s*hemoglobin",
            "tsh": r"tsh|thyroid\s*stimulating\s*hormone",
            "t4": r"t4|thyroxine"
        }
        
        # Unit patterns
        self.unit_patterns = {
            "g/dL": r"g/dl|g/dL",
            "mg/dL": r"mg/dl|mg/dL",
            "mEq/L": r"meq/l|mEq/L",
            "U/L": r"u/l|U/L",
            "K/uL": r"k/ul|K/uL",
            "M/uL": r"m/ul|M/uL",
            "%": r"%|percent",
            "mIU/L": r"miu/l|mIU/L",
            "ng/dL": r"ng/dl|ng/dL"
        }
    
    def parse_lab_results(self, text: str) -> List[Dict[str, Any]]:
        """Parse OCR text and extract lab results"""
        results = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Try to extract test name, value, and unit
            parsed = self._parse_line(line)
            if parsed:
                results.append(parsed)
        
        logger.info(f"Parsed {len(results)} lab results from text")
        return results
    
    def _parse_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a single line for lab results"""
        # Look for patterns like "Glucose: 120 mg/dL" or "Hemoglobin 14.2 g/dL"
        
        # Try different patterns
        patterns = [
            # Pattern: Test Name: Value Unit
            r"([a-zA-Z\s]+):\s*([\d.]+)\s*([a-zA-Z/%]+)",
            # Pattern: Test Name Value Unit
            r"([a-zA-Z\s]+)\s+([\d.]+)\s+([a-zA-Z/%]+)",
            # Pattern: Test Name = Value Unit
            r"([a-zA-Z\s]+)\s*=\s*([\d.]+)\s*([a-zA-Z/%]+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                test_name = match.group(1).strip()
                value_str = match.group(2)
                unit = match.group(3).strip()
                
                try:
                    value = float(value_str)
                    
                    # Identify the test
                    identified_test = self._identify_test(test_name)
                    if identified_test:
                        return {
                            "test_name": identified_test,
                            "original_name": test_name,
                            "value": value,
                            "unit": unit,
                            "line": line
                        }
                except ValueError:
                    continue
        
        return None
    
    def _identify_test(self, test_name: str) -> Optional[str]:
        """Identify standardized test name from various formats"""
        test_name_lower = test_name.lower()
        
        for standard_name, pattern in self.test_patterns.items():
            if re.search(pattern, test_name_lower, re.IGNORECASE):
                return standard_name
        
        return None
    
    def _normalize_unit(self, unit: str) -> str:
        """Normalize unit format"""
        unit_lower = unit.lower()
        
        for standard_unit, pattern in self.unit_patterns.items():
            if re.search(pattern, unit_lower, re.IGNORECASE):
                return standard_unit
        
        return unit
