from typing import List, Dict, Any, Optional
from .reference_ranges import ReferenceRanges
from .lab_parser import LabParser
import logging

logger = logging.getLogger(__name__)

class AnalysisEngine:
    def __init__(self):
        self.reference_ranges = ReferenceRanges()
        self.lab_parser = LabParser()
    
    def analyze_lab_report(self, ocr_text: str, age: Optional[int] = None, sex: Optional[str] = None) -> Dict[str, Any]:
        """Analyze a complete lab report"""
        try:
            # Parse lab results from OCR text
            lab_results = self.lab_parser.parse_lab_results(ocr_text)
            
            if not lab_results:
                return {
                    "success": False,
                    "error": "No lab results found in the text",
                    "results": []
                }
            
            # Analyze each result
            analyzed_results = []
            critical_findings = []
            abnormal_findings = []
            
            for result in lab_results:
                analysis = self._analyze_single_result(result, age, sex)
                analyzed_results.append(analysis)
                
                # Track critical and abnormal findings
                if analysis["classification"] in ["CRITICAL_LOW", "CRITICAL_HIGH"]:
                    critical_findings.append(analysis)
                elif analysis["classification"] in ["LOW", "HIGH"]:
                    abnormal_findings.append(analysis)
            
            # Generate summary
            summary = self._generate_summary(analyzed_results, critical_findings, abnormal_findings)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(analyzed_results, age, sex)
            
            return {
                "success": True,
                "results": analyzed_results,
                "summary": summary,
                "recommendations": recommendations,
                "critical_findings": critical_findings,
                "abnormal_findings": abnormal_findings,
                "total_tests": len(analyzed_results),
                "normal_count": len([r for r in analyzed_results if r["classification"] == "NORMAL"]),
                "abnormal_count": len(abnormal_findings),
                "critical_count": len(critical_findings)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing lab report: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": []
            }
    
    def _analyze_single_result(self, result: Dict[str, Any], age: Optional[int], sex: Optional[str]) -> Dict[str, Any]:
        """Analyze a single lab result"""
        classification = self.reference_ranges.classify_value(
            result["test_name"],
            result["value"],
            result["unit"],
            age,
            sex
        )
        
        return {
            **result,
            **classification,
            "interpretation": self._get_interpretation(result["test_name"], classification)
        }
    
    def _get_interpretation(self, test_name: str, classification: Dict[str, Any]) -> str:
        """Get interpretation for a test result"""
        interpretations = {
            "glucose": {
                "HIGH": "Elevated blood sugar levels. May indicate prediabetes or diabetes.",
                "LOW": "Low blood sugar levels. May indicate hypoglycemia.",
                "CRITICAL_HIGH": "Very high blood sugar. Requires immediate medical attention.",
                "CRITICAL_LOW": "Very low blood sugar. Requires immediate medical attention."
            },
            "hemoglobin": {
                "LOW": "Low hemoglobin may indicate anemia.",
                "HIGH": "High hemoglobin may indicate dehydration or other conditions."
            },
            "hdl": {
                "LOW": "Low HDL cholesterol increases heart disease risk.",
                "HIGH": "High HDL cholesterol is protective against heart disease."
            },
            "ldl": {
                "HIGH": "High LDL cholesterol increases heart disease risk.",
                "CRITICAL_HIGH": "Very high LDL cholesterol. High risk for heart disease."
            },
            "hba1c": {
                "HIGH": "Elevated HbA1c indicates poor blood sugar control over time.",
                "CRITICAL_HIGH": "Very high HbA1c suggests diabetes or poor diabetes control."
            }
        }
        
        test_interpretations = interpretations.get(test_name, {})
        return test_interpretations.get(classification["classification"], "Result outside normal range.")
    
    def _generate_summary(self, results: List[Dict], critical_findings: List[Dict], abnormal_findings: List[Dict]) -> str:
        """Generate a plain-English summary"""
        if critical_findings:
            return f"⚠️ CRITICAL: {len(critical_findings)} critical findings require immediate medical attention. {len(abnormal_findings)} other values are outside normal range."
        elif abnormal_findings:
            return f"📊 ABNORMAL: {len(abnormal_findings)} values are outside normal range. Consider discussing with your healthcare provider."
        else:
            return "✅ NORMAL: All lab values are within normal ranges."
    
    def _generate_recommendations(self, results: List[Dict], age: Optional[int], sex: Optional[str]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Check for specific conditions
        glucose_results = [r for r in results if r["test_name"] == "glucose"]
        cholesterol_results = [r for r in results if r["test_name"] in ["hdl", "ldl", "total_cholesterol"]]
        
        if glucose_results and glucose_results[0]["classification"] in ["HIGH", "CRITICAL_HIGH"]:
            recommendations.append("Consider monitoring blood sugar levels more frequently.")
            recommendations.append("Discuss diabetes screening with your healthcare provider.")
        
        if cholesterol_results:
            ldl_result = next((r for r in cholesterol_results if r["test_name"] == "ldl"), None)
            if ldl_result and ldl_result["classification"] in ["HIGH", "CRITICAL_HIGH"]:
                recommendations.append("Consider heart-healthy diet changes to lower cholesterol.")
                recommendations.append("Discuss cholesterol management with your healthcare provider.")
        
        if not recommendations:
            recommendations.append("Continue with regular health checkups.")
            recommendations.append("Maintain a healthy lifestyle with balanced diet and exercise.")
        
        return recommendations
