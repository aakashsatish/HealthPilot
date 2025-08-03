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
            "total_cholesterol": r"total\s*cholesterol|cholesterol",
            "hdl": r"hdl|high\s*density\s*lipoprotein|hdl\s*cholesterol",
            "ldl": r"ldl|low\s*density\s*lipoprotein|ldl\s*cholesterol",
            "triglycerides": r"triglycerides|triglyceride|trig",
            "hba1c": r"hba1c|a1c|glycated\s*hemoglobin",
            "tsh": r"tsh|thyroid\s*stimulating\s*hormone",
            "t4": r"t4|thyroxine|free\s*t4",
            "t3": r"t3|triiodothyronine|free\s*t3",
            "urate": r"urate|uric\s*acid",
            "creatine_kinase": r"creatine\s*kinase|ck",
            "non_hdl_cholesterol": r"non\s*hdl|non\s*hdl\s*cholesterol"
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
    
    def parse_lab_results(self, text: str) -> List[Dict[str, Any]]:
        """Parse OCR text and extract lab results"""
        results = []
        lines = text.split('\n')
        
        # Look for specific lipid panel tests
        lipid_tests = {
            'triglycerides': ['triglyceride', 'triglycerides'],
            'total_cholesterol': ['cholesterol'],
            'hdl': ['hdl cholesterol', 'hdl'],
            'ldl': ['ldl cholesterol', 'ldl'],
            'non_hdl_cholesterol': ['non hdl cholesterol', 'non hdl']
        }
        
        # Also look for other important tests
        other_tests = {
            'urate': ['urate', 'uric acid'],
            'glucose': ['glucose', 'glu'],
            'creatinine': ['creatinine'],
            'hemoglobin': ['hemoglobin', 'hgb'],
            'tsh': ['tsh', 'thyroid stimulating hormone'],
            't4': ['t4', 'free t4'],
            't3': ['t3', 'free t3']
        }
        
        all_tests = {**lipid_tests, **other_tests}
        
        # First pass: identify test names and their positions
        test_positions = []
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Look for test names
            for test_name, patterns in all_tests.items():
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        test_positions.append({
                            'line_index': i,
                            'test_name': test_name,
                            'original_name': line,
                            'line': line
                        })
                        break
                else:
                    continue
                break
        
        # Second pass: find values and flags near test names
        for test_info in test_positions:
            line_index = test_info['line_index']
            
            # Look for values in the next few lines
            for i in range(line_index + 1, min(line_index + 10, len(lines))):
                value_line = lines[i].strip()
                if not value_line:
                    continue
                
                # Look for patterns like "HI 1.98" or "LO 0.95"
                value_match = re.search(r"(HI|LO)\s+([\d.]+)", value_line, re.IGNORECASE)
                if value_match:
                    flag = value_match.group(1)
                    value_str = value_match.group(2)
                    
                    try:
                        value = float(value_str)
                        
                        # Look for units in the same line or next few lines
                        unit = self._find_unit(lines, i)
                        
                        # Look for reference range in subsequent lines
                        reference_range = self._find_reference_range(lines, i)
                        
                        results.append({
                            "test_name": test_info['test_name'],
                            "original_name": test_info['original_name'],
                            "value": value,
                            "unit": unit,
                            "flag": flag,
                            "reference_range": reference_range,
                            "line": test_info['line'] + " -> " + value_line
                        })
                        break
                    except ValueError:
                        continue
        
        logger.info(f"Parsed {len(results)} lab results from text")
        return results
    
    def _find_unit(self, lines: List[str], start_index: int) -> str:
        """Find unit in the same line or nearby lines"""
        # Look in the same line first
        line = lines[start_index]
        for unit, pattern in self.unit_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                return unit
        
        # Look in next few lines
        for i in range(start_index + 1, min(start_index + 5, len(lines))):
            line = lines[i].strip()
            if not line:
                continue
            for unit, pattern in self.unit_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    return unit
        
        return ""
    
    def _find_reference_range(self, lines: List[str], start_index: int) -> str:
        """Find reference range in subsequent lines"""
        for i in range(start_index + 1, min(start_index + 10, len(lines))):
            line = lines[i].strip()
            if not line:
                continue
            
            # Look for patterns like "230-480" or "Desired: <4.40"
            range_match = re.search(r"([\d.-]+)\s*[-–]\s*([\d.-]+)", line)
            if range_match:
                return f"{range_match.group(1)}-{range_match.group(2)}"
            
            # Look for "Desired: <X" or "Desired: >X"
            desired_match = re.search(r"Desired:\s*([<>]\s*[\d.]+)", line)
            if desired_match:
                return desired_match.group(1)
        
        return ""
    
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
