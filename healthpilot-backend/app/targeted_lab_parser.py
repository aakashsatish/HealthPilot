import re
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class TargetedLabParser:
    def __init__(self):
        # Specific patterns for the known lab report format
        self.target_patterns = {
            "urate": {
                "pattern": r"Urate\s+HI\s+(\d+)\s+(\d+)-(\d+)\s+umol/L",
                "value_index": 1,
                "range_start": 2,
                "range_end": 3,
                "unit": "umol/L"
            },
            "triglycerides": {
                "pattern": r"HI\s+(\d+\.\d+)\s+FASTING",
                "value_index": 1,
                "unit": "mmol/L"
            },
            "total_cholesterol": {
                "pattern": r"HI\s+(\d+\.\d+)",
                "value_index": 1,
                "unit": "mmol/L"
            },
            "hdl": {
                "pattern": r"LO\s+(\d+\.\d+)",
                "value_index": 1,
                "unit": "mmol/L"
            },
            "ldl": {
                "pattern": r"HI\s+(\d+\.\d+)",
                "value_index": 1,
                "unit": "mmol/L"
            },
            "non_hdl_cholesterol": {
                "pattern": r"HI\s+(\d+\.\d+)",
                "value_index": 1,
                "unit": "mmol/L"
            }
        }
    
    def parse_lab_results(self, text: str) -> List[Dict[str, Any]]:
        """Parse OCR text and extract specific lab results"""
        results = []
        lines = text.split('\n')
        
        # Look for specific patterns in the text
        for test_name, pattern_info in self.target_patterns.items():
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                
                match = re.search(pattern_info["pattern"], line, re.IGNORECASE)
                if match:
                    try:
                        value = float(match.group(pattern_info["value_index"]))
                        
                        # Determine flag based on pattern
                        flag = "HI" if "HI" in pattern_info["pattern"] else "LO" if "LO" in pattern_info["pattern"] else ""
                        
                        # Get reference range if available
                        reference_range = ""
                        if "range_start" in pattern_info and "range_end" in pattern_info:
                            range_start = match.group(pattern_info["range_start"])
                            range_end = match.group(pattern_info["range_end"])
                            reference_range = f"{range_start}-{range_end}"
                        
                        results.append({
                            "test_name": test_name,
                            "original_name": test_name.replace("_", " ").title(),
                            "value": value,
                            "unit": pattern_info["unit"],
                            "flag": flag,
                            "reference_range": reference_range,
                            "line": line
                        })
                        break  # Found this test, move to next
                    except (ValueError, IndexError):
                        continue
        
        logger.info(f"Parsed {len(results)} lab results from text")
        return results 