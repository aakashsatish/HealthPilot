import re
from typing import List, Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class IntelligentLabParser:
    def __init__(self):
        # Common lab test names with more specific patterns
        self.test_patterns = {
            "hemoglobin": r"^hemoglobin$|^hgb$|^hb$",
            "hematocrit": r"^hematocrit$|^hct$",
            "white_blood_cells": r"^white\s*blood\s*cells$|^wbc$|^leukocytes$",
            "platelets": r"^platelets$|^plt$",
            "red_blood_cells": r"^red\s*blood\s*cells$|^rbc$",
            "glucose": r"^glucose$|^glu$",
            "creatinine": r"^creatinine$|^creat$",
            "bun": r"^bun$|^blood\s*urea\s*nitrogen$",
            "sodium": r"^sodium$|^na$",
            "potassium": r"^potassium$|^k$",
            "chloride": r"^chloride$|^cl$",
            "co2": r"^co2$|^bicarbonate$|^hco3$",
            "calcium": r"^calcium$|^ca$",
            "total_protein": r"^total\s*protein$|^tp$",
            "albumin": r"^albumin$|^alb$",
            "total_bilirubin": r"^total\s*bilirubin$|^tbil$",
            "alkaline_phosphatase": r"^alkaline\s*phosphatase$|^alp$",
            "alt": r"^alt$|^alanine\s*aminotransferase$",
            "ast": r"^ast$|^aspartate\s*aminotransferase$",
            "total_cholesterol": r"^cholesterol$",
            "hdl": r"^hdl\s*cholesterol$|^hdl$",
            "ldl": r"^ldl\s*cholesterol$|^ldl$",
            "triglycerides": r"^triglyceride$|^triglycerides$|^trig$",
            "hba1c": r"^hba1c$|^a1c$|^glycated\s*hemoglobin$",
            "tsh": r"^tsh$|^thyroid\s*stimulating\s*hormone$",
            "t4": r"^t4$|^thyroxine$|^free\s*t4$",
            "t3": r"^t3$|^triiodothyronine$|^free\s*t3$",
            "urate": r"^urate$|^uric\s*acid$",
            "creatine_kinase": r"^creatine\s*kinase$|^ck$",
            "non_hdl_cholesterol": r"^non\s*hdl\s*cholesterol$|^non\s*hdl$"
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
            "ng/dL": r"ng/dl|ng/dL",
            "mmol/L": r"mmol/l|mmol/L",
            "umol/L": r"umol/l|umol/L",
            "pmol/L": r"pmol/l|pmol/L"
        }
        
        # Valid value ranges for common tests (for validation)
        self.valid_ranges = {
            "glucose": (50, 500),  # mg/dL
            "hemoglobin": (5, 25),  # g/dL
            "sodium": (120, 160),   # mEq/L
            "potassium": (2, 8),    # mEq/L
            "chloride": (90, 120),  # mEq/L
            "creatinine": (0.5, 15), # mg/dL
            "total_cholesterol": (100, 600), # mg/dL
            "hdl": (20, 100),       # mg/dL
            "ldl": (50, 300),       # mg/dL
            "triglycerides": (30, 1000), # mg/dL
            "urate": (2, 15),       # mg/dL
            "alt": (5, 200),        # U/L
            "ast": (5, 200),        # U/L
            "tsh": (0.1, 20),       # mIU/L
            "t4": (0.5, 4),         # ng/dL
            "t3": (0.5, 4),         # ng/dL
        }
    
    def parse_lab_results(self, text: str) -> List[Dict[str, Any]]:
        """Parse OCR text and extract lab results using intelligent pattern matching"""
        results = []
        lines = text.split('\n')
        
        # Step 1: Find test names and their positions
        test_positions = self._find_test_positions(lines)
        
        # Step 2: For each test, find associated values with validation
        for test_info in test_positions:
            value_info = self._find_test_value_with_validation(lines, test_info)
            if value_info:
                results.append({
                    "test_name": test_info['test_name'],
                    "original_name": test_info['original_name'],
                    "value": value_info['value'],
                    "unit": value_info['unit'],
                    "flag": value_info['flag'],
                    "reference_range": value_info['reference_range'],
                    "line": test_info['line'] + " -> " + value_info['line']
                })
        
        logger.info(f"Parsed {len(results)} lab results from text")
        return results
    
    def _find_test_positions(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Find test names using strict matching"""
        test_positions = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Use strict matching for test names
            for test_name, pattern in self.test_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    test_positions.append({
                        'line_index': i,
                        'test_name': test_name,
                        'original_name': line,
                        'line': line
                    })
                    break
        
        return test_positions
    
    def _find_test_value_with_validation(self, lines: List[str], test_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find and validate test values"""
        line_index = test_info['line_index']
        test_name = test_info['test_name']
        
        # Look in a window around the test name
        start_idx = max(0, line_index - 3)
        end_idx = min(len(lines), line_index + 10)
        
        for i in range(start_idx, end_idx):
            line = lines[i].strip()
            if not line:
                continue
            
            # Try to extract value from this line
            value_info = self._extract_value_from_line(line)
            if value_info:
                # Validate the value
                if self._validate_value(test_name, value_info['value']):
                    # Look for units and reference ranges
                    unit = self._find_unit_in_context(lines, i)
                    reference_range = self._find_reference_range_in_context(lines, i)
                    
                    return {
                        'value': value_info['value'],
                        'unit': unit,
                        'flag': value_info['flag'],
                        'reference_range': reference_range,
                        'line': line
                    }
        
        return None
    
    def _extract_value_from_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Extract numeric values using multiple patterns"""
        
        # Pattern 1: "HI 1.98" or "LO 0.95"
        pattern1 = r"^(HI|LO)\s+([\d.]+)$"
        match = re.search(pattern1, line, re.IGNORECASE)
        if match:
            try:
                return {
                    'value': float(match.group(2)),
                    'flag': match.group(1)
                }
            except ValueError:
                pass
        
        # Pattern 2: "590" (just a number)
        pattern2 = r"^([\d.]+)$"
        match = re.search(pattern2, line)
        if match:
            try:
                return {
                    'value': float(match.group(1)),
                    'flag': ""
                }
            except ValueError:
                pass
        
        # Pattern 3: "Value (HI)" or "Value (LO)"
        pattern3 = r"^([\d.]+)\s*\(?(HI|LO)\)?$"
        match = re.search(pattern3, line, re.IGNORECASE)
        if match:
            try:
                return {
                    'value': float(match.group(1)),
                    'flag': match.group(2)
                }
            except ValueError:
                pass
        
        return None
    
    def _validate_value(self, test_name: str, value: float) -> bool:
        """Validate if a value is reasonable for a given test"""
        if test_name in self.valid_ranges:
            min_val, max_val = self.valid_ranges[test_name]
            return min_val <= value <= max_val
        
        # For tests without defined ranges, use general validation
        return 0 < value < 10000  # Reasonable range for most lab values
    
    def _find_unit_in_context(self, lines: List[str], value_line_index: int) -> str:
        """Find unit in the same line or nearby lines"""
        # Look in the same line first
        line = lines[value_line_index]
        for unit, pattern in self.unit_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                return unit
        
        # Look in nearby lines
        for i in range(max(0, value_line_index - 2), min(len(lines), value_line_index + 3)):
            line = lines[i].strip()
            if not line:
                continue
            for unit, pattern in self.unit_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    return unit
        
        return ""
    
    def _find_reference_range_in_context(self, lines: List[str], value_line_index: int) -> str:
        """Find reference range in nearby lines"""
        for i in range(max(0, value_line_index - 3), min(len(lines), value_line_index + 5)):
            line = lines[i].strip()
            if not line:
                continue
            
            # Look for various reference range patterns
            patterns = [
                r"([\d.-]+)\s*[-–]\s*([\d.-]+)",  # "230-480"
                r"Desired:\s*([<>]\s*[\d.]+)",     # "Desired: <4.40"
                r"Reference:\s*([\d.-]+)",         # "Reference: 230-480"
                r"Normal:\s*([\d.-]+)",           # "Normal: 230-480"
                r"Range:\s*([\d.-]+)"             # "Range: 230-480"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    if len(match.groups()) == 2:
                        return f"{match.group(1)}-{match.group(2)}"
                    else:
                        return match.group(1)
        
        return "" 