from typing import List, Dict, Any, Optional
from .reference_ranges import ReferenceRanges
from .comprehensive_lab_parser import ComprehensiveLabParser
from .ai_analysis_service import AIAnalysisService
import logging

logger = logging.getLogger(__name__)

class AnalysisEngine:
    def __init__(self):
        self.reference_ranges = ReferenceRanges()
        self.lab_parser = ComprehensiveLabParser()
        self.ai_analysis = AIAnalysisService()
    
    def analyze_lab_report(self, ocr_text: str, age: Optional[int] = None, sex: Optional[str] = None) -> Dict[str, Any]:
        """Analyze a complete lab report using AI"""
        try:
            # Parse lab results from OCR text
            lab_results = self.lab_parser.parse_lab_results(ocr_text)
            
            if not lab_results:
                return {
                    "success": False,
                    "error": "No lab results found in the text",
                    "results": []
                }
            
            # Use AI for full analysis
            try:
                ai_analysis = self.ai_analysis.generate_full_analysis(lab_results, age, sex)
                
                return {
                    "success": True,
                    "results": lab_results,
                    "summary": ai_analysis["summary"],
                    "recommendations": ai_analysis["recommendations"],
                    "risk_assessment": {
                        "risk_level": ai_analysis["risk_level"],
                        "risk_factors": ai_analysis["risk_factors"],
                        "recommendations": ai_analysis["recommendations"]
                    },
                    "early_warnings": ai_analysis["early_warnings"],
                    "critical_findings": [],
                    "abnormal_findings": [r for r in lab_results if r["classification"] != "NORMAL"],
                    "total_tests": len(lab_results),
                    "normal_count": len([r for r in lab_results if r["classification"] == "NORMAL"]),
                    "abnormal_count": len([r for r in lab_results if r["classification"] != "NORMAL"]),
                    "critical_count": 0
                }
                
            except Exception as e:
                logger.error(f"AI analysis failed: {e}")
                # Fallback to rule-based analysis
                return self._get_fallback_analysis(lab_results, age, sex)
            
        except Exception as e:
            logger.error(f"Error analyzing lab report: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": []
            }
    
    def _get_fallback_analysis(self, lab_results: List[Dict], age: Optional[int], sex: Optional[str]) -> Dict[str, Any]:
        """Fallback to rule-based analysis if AI fails"""
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
        
        # Generate risk assessment
        risk_assessment = self._generate_risk_assessment(analyzed_results, age, sex)
        
        # Generate early warning signals
        early_warnings = self._generate_early_warnings(analyzed_results)
        
        return {
            "success": True,
            "results": analyzed_results,
            "summary": summary,
            "recommendations": recommendations,
            "risk_assessment": risk_assessment,
            "early_warnings": early_warnings,
            "critical_findings": critical_findings,
            "abnormal_findings": abnormal_findings,
            "total_tests": len(analyzed_results),
            "normal_count": len([r for r in analyzed_results if r["classification"] == "NORMAL"]),
            "abnormal_count": len(abnormal_findings),
            "critical_count": len(critical_findings)
        }
    
    def _analyze_single_result(self, result: Dict[str, Any], age: Optional[int], sex: Optional[str]) -> Dict[str, Any]:
        """Analyze a single lab result"""
        # If the result already has a classification from the parser, use it
        if "classification" in result and result["classification"] != "UNKNOWN":
            classification = {
                "classification": result["classification"],
                "status": self._get_status_message(result["classification"]),
                "reference_range": result.get("reference_range", "")
            }
        else:
            # Otherwise, classify using the reference ranges
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
    
    def _get_status_message(self, classification: str) -> str:
        """Get status message for classification"""
        status_messages = {
            "NORMAL": "Within normal range",
            "LOW": "Below normal range",
            "HIGH": "Above normal range",
            "CRITICAL_LOW": "Critically low - requires immediate attention",
            "CRITICAL_HIGH": "Critically high - requires immediate attention"
        }
        return status_messages.get(classification, "Result outside normal range")
    
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
        """Generate a comprehensive plain-English summary in simple language"""
        if critical_findings:
            return f"⚠️ URGENT: {len(critical_findings)} of your test results are dangerously high or low and need immediate medical attention. {len(abnormal_findings)} other results are outside the normal range."
        elif abnormal_findings:
            # Create a more conversational summary
            summary_parts = []
            summary_parts.append(f"📊 Your lab results show {len(abnormal_findings)} values that are outside the normal range.")
            
            # Group by type of abnormality in simple terms
            lipid_issues = [r for r in abnormal_findings if r["test_name"] in ["total_cholesterol", "hdl", "ldl", "triglycerides", "non_hdl_cholesterol"]]
            metabolic_issues = [r for r in abnormal_findings if r["test_name"] in ["urate", "glucose", "hba1c"]]
            
            if lipid_issues:
                if len(lipid_issues) == 1:
                    summary_parts.append("You have 1 cholesterol-related result that needs attention.")
                else:
                    summary_parts.append(f"You have {len(lipid_issues)} cholesterol-related results that need attention.")
            
            if metabolic_issues:
                if len(metabolic_issues) == 1:
                    summary_parts.append("You have 1 metabolism-related result that needs attention.")
                else:
                    summary_parts.append(f"You have {len(metabolic_issues)} metabolism-related results that need attention.")
            
            # Add simple explanation of what this means
            if lipid_issues and metabolic_issues:
                summary_parts.append("This suggests your body's processing of fats and sugars may need some adjustments.")
            elif lipid_issues:
                summary_parts.append("This suggests your cholesterol levels may need some lifestyle changes or medical attention.")
            elif metabolic_issues:
                summary_parts.append("This suggests your body's processing of certain substances may need some attention.")
            
            summary_parts.append("It's a good idea to discuss these results with your doctor.")
            
            return " ".join(summary_parts)
        else:
            return "✅ Great news! All your lab results are within the normal range."
    
    def _generate_recommendations(self, results: List[Dict], age: Optional[int], sex: Optional[str]) -> List[str]:
        """Generate comprehensive personalized recommendations"""
        recommendations = []
        
        # Group results by category
        lipid_results = [r for r in results if r["test_name"] in ["total_cholesterol", "hdl", "ldl", "triglycerides", "non_hdl_cholesterol"]]
        metabolic_results = [r for r in results if r["test_name"] in ["urate", "glucose", "hba1c"]]
        cbc_results = [r for r in results if r["test_name"] in ["hemoglobin", "white_blood_cells", "platelets"]]
        
        # Lipid profile recommendations
        if lipid_results:
            recommendations.extend(self._get_lipid_recommendations(lipid_results))
        
        # Metabolic recommendations
        if metabolic_results:
            recommendations.extend(self._get_metabolic_recommendations(metabolic_results))
        
        # General health recommendations
        recommendations.extend(self._get_general_recommendations(results, age, sex))
        
        # Follow-up recommendations
        recommendations.extend(self._get_followup_recommendations(results))
        
        return recommendations
    
    def _get_lipid_recommendations(self, lipid_results: List[Dict]) -> List[str]:
        """Get specific recommendations for lipid profile abnormalities in plain English"""
        recommendations = []
        
        hdl_result = next((r for r in lipid_results if r["test_name"] == "hdl"), None)
        ldl_result = next((r for r in lipid_results if r["test_name"] == "ldl"), None)
        triglycerides_result = next((r for r in lipid_results if r["test_name"] == "triglycerides"), None)
        
        # HDL recommendations
        if hdl_result and hdl_result["classification"] == "LOW":
            recommendations.append("Try to exercise more - even a 30-minute walk daily can help raise your good cholesterol.")
            recommendations.append("Consider eating more healthy fats like olive oil, nuts, and fatty fish like salmon.")
            recommendations.append("If you smoke, quitting can help improve your cholesterol levels.")
        
        # LDL recommendations
        if ldl_result and ldl_result["classification"] in ["HIGH", "CRITICAL_HIGH"]:
            recommendations.append("Try to eat less fatty meats and fried foods.")
            recommendations.append("Add more fiber to your diet through whole grains, fruits, and vegetables.")
            recommendations.append("Look for foods with plant sterols (often added to margarine and orange juice).")
            recommendations.append("Talk to your doctor about whether you need medication to lower cholesterol.")
        
        # Triglycerides recommendations
        if triglycerides_result and triglycerides_result["classification"] in ["HIGH", "CRITICAL_HIGH"]:
            recommendations.append("Cut back on sugary foods and drinks, including alcohol.")
            recommendations.append("Try to exercise regularly - even walking can help lower triglycerides.")
            recommendations.append("Consider eating more fish or taking fish oil supplements.")
        
        # General lipid recommendations
        if len([r for r in lipid_results if r["classification"] in ["HIGH", "CRITICAL_HIGH", "LOW"]]) >= 2:
            recommendations.append("Your doctor might want to check your heart health more thoroughly.")
            recommendations.append("Keep an eye on your blood pressure - high cholesterol and high blood pressure often go together.")
        
        return recommendations
    
    def _get_metabolic_recommendations(self, metabolic_results: List[Dict]) -> List[str]:
        """Get specific recommendations for metabolic abnormalities in plain English"""
        recommendations = []
        
        urate_result = next((r for r in metabolic_results if r["test_name"] == "urate"), None)
        glucose_result = next((r for r in metabolic_results if r["test_name"] == "glucose"), None)
        hba1c_result = next((r for r in metabolic_results if r["test_name"] == "hba1c"), None)
        
        # Urate (gout) recommendations
        if urate_result and urate_result["classification"] in ["HIGH", "CRITICAL_HIGH"]:
            recommendations.append("Try to eat less red meat, organ meats (like liver), and shellfish.")
            recommendations.append("Cut back on alcohol, especially beer.")
            recommendations.append("Drink plenty of water - aim for 8 glasses a day.")
            recommendations.append("Low-fat dairy products like milk and yogurt might help lower urate levels.")
            recommendations.append("Talk to your doctor about medications that can help with high urate levels.")
        
        # Glucose recommendations
        if glucose_result and glucose_result["classification"] in ["HIGH", "CRITICAL_HIGH"]:
            recommendations.append("Keep track of your blood sugar levels regularly.")
            recommendations.append("Try to eat balanced meals and watch your carbohydrate intake.")
            recommendations.append("Regular exercise can help keep your blood sugar in check.")
            recommendations.append("Your doctor might want to check for diabetes.")
        
        # HbA1c recommendations
        if hba1c_result and hba1c_result["classification"] in ["HIGH", "CRITICAL_HIGH"]:
            recommendations.append("Work with your doctor to create a plan to manage your blood sugar.")
            recommendations.append("You might need to check your blood sugar more often.")
            recommendations.append("Consider meeting with a diabetes educator or dietitian for help.")
        
        return recommendations
    
    def _get_general_recommendations(self, results: List[Dict], age: Optional[int], sex: Optional[str]) -> List[str]:
        """Get general health recommendations in plain English"""
        recommendations = []
        
        abnormal_count = len([r for r in results if r["classification"] in ["HIGH", "LOW", "CRITICAL_HIGH", "CRITICAL_LOW"]])
        
        if abnormal_count >= 3:
            recommendations.append("Since you have several results that need attention, it's a good idea to see your doctor for a complete checkup.")
            recommendations.append("Focus on making healthy lifestyle changes - diet, exercise, and stress management can make a big difference.")
        
        # Age-specific recommendations
        if age:
            if age >= 50:
                recommendations.append("As we get older, it's important to have regular health checkups.")
            elif age >= 30:
                recommendations.append("It's a good time to establish regular health checkups if you haven't already.")
        
        # General lifestyle recommendations
        recommendations.append("Try to get at least 150 minutes of moderate exercise each week - that's about 30 minutes, 5 days a week.")
        recommendations.append("Eat a balanced diet with plenty of fruits, vegetables, and whole grains.")
        recommendations.append("Aim for 7-9 hours of good sleep each night.")
        recommendations.append("Find ways to manage stress - meditation, yoga, or just taking time to relax can help.")
        
        return recommendations
    
    def _get_followup_recommendations(self, results: List[Dict]) -> List[str]:
        """Get follow-up testing and monitoring recommendations in plain English"""
        recommendations = []
        
        # Determine appropriate follow-up timing based on severity
        critical_count = len([r for r in results if r["classification"] in ["CRITICAL_HIGH", "CRITICAL_LOW"]])
        high_count = len([r for r in results if r["classification"] in ["HIGH", "LOW"]])
        
        if critical_count > 0:
            recommendations.append("You should get retested in 2-4 weeks to see if these levels improve.")
            recommendations.append("Your doctor might want you to see a specialist right away.")
        elif high_count >= 3:
            recommendations.append("Plan to get retested in 1-2 months to track your progress.")
        elif high_count > 0:
            recommendations.append("Consider getting retested in 3-6 months to see if lifestyle changes help.")
        
        # Specific test follow-up recommendations
        lipid_abnormal = any(r["test_name"] in ["total_cholesterol", "hdl", "ldl", "triglycerides"] and r["classification"] in ["HIGH", "LOW"] for r in results)
        if lipid_abnormal:
            recommendations.append("Your doctor will likely want to check your cholesterol every 3-6 months until it improves.")
        
        urate_high = any(r["test_name"] == "urate" and r["classification"] in ["HIGH", "CRITICAL_HIGH"] for r in results)
        if urate_high:
            recommendations.append("Your urate levels should be checked every 3-6 months to see if treatment is working.")
        
        return recommendations
    
    def _generate_risk_assessment(self, results: List[Dict], age: Optional[int], sex: Optional[str]) -> Dict[str, Any]:
        """Generate cardiovascular and metabolic risk assessment"""
        risk_factors = []
        risk_level = "LOW"
        
        # Cardiovascular risk factors
        lipid_results = [r for r in results if r["test_name"] in ["total_cholesterol", "hdl", "ldl", "triglycerides"]]
        if lipid_results:
            high_ldl = any(r["test_name"] == "ldl" and r["classification"] in ["HIGH", "CRITICAL_HIGH"] for r in lipid_results)
            low_hdl = any(r["test_name"] == "hdl" and r["classification"] == "LOW" for r in lipid_results)
            high_triglycerides = any(r["test_name"] == "triglycerides" and r["classification"] in ["HIGH", "CRITICAL_HIGH"] for r in lipid_results)
            
            if high_ldl:
                risk_factors.append("Elevated LDL cholesterol")
            if low_hdl:
                risk_factors.append("Low HDL cholesterol")
            if high_triglycerides:
                risk_factors.append("Elevated triglycerides")
            
            # Determine risk level
            if high_ldl and low_hdl:
                risk_level = "HIGH"
            elif high_ldl or low_hdl:
                risk_level = "MODERATE"
        
        # Metabolic risk factors
        urate_result = next((r for r in results if r["test_name"] == "urate"), None)
        if urate_result and urate_result["classification"] in ["HIGH", "CRITICAL_HIGH"]:
            risk_factors.append("Elevated urate levels (gout risk)")
            if risk_level == "LOW":
                risk_level = "MODERATE"
        
        # Age and sex considerations
        if age and age >= 45:
            risk_factors.append("Age-related cardiovascular risk")
            if risk_level == "LOW":
                risk_level = "MODERATE"
        
        return {
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "recommendations": self._get_risk_based_recommendations(risk_level, risk_factors)
        }
    
    def _generate_early_warnings(self, results: List[Dict]) -> List[Dict[str, Any]]:
        """Generate early warning signals for potential health issues"""
        warnings = []
        
        # Lipid pattern warnings
        lipid_results = [r for r in results if r["test_name"] in ["total_cholesterol", "hdl", "ldl", "triglycerides"]]
        if lipid_results:
            hdl_result = next((r for r in lipid_results if r["test_name"] == "hdl"), None)
            ldl_result = next((r for r in lipid_results if r["test_name"] == "ldl"), None)
            
            if hdl_result and ldl_result:
                if hdl_result["classification"] == "LOW" and ldl_result["classification"] in ["HIGH", "CRITICAL_HIGH"]:
                    warnings.append({
                        "type": "CARDIOVASCULAR",
                        "severity": "HIGH",
                        "message": "Atherogenic lipid pattern detected (low HDL + high LDL)",
                        "action": "Immediate lifestyle modification and medical consultation recommended"
                    })
        
        # Metabolic syndrome indicators
        metabolic_markers = [r for r in results if r["test_name"] in ["triglycerides", "hdl", "glucose"]]
        if len(metabolic_markers) >= 2:
            abnormal_metabolic = [r for r in metabolic_markers if r["classification"] in ["HIGH", "LOW"]]
            if len(abnormal_metabolic) >= 2:
                warnings.append({
                    "type": "METABOLIC",
                    "severity": "MODERATE",
                    "message": "Multiple metabolic markers abnormal - possible metabolic syndrome",
                    "action": "Comprehensive metabolic assessment recommended"
                })
        
        # Urate-related warnings
        urate_result = next((r for r in results if r["test_name"] == "urate"), None)
        if urate_result and urate_result["classification"] in ["HIGH", "CRITICAL_HIGH"]:
            warnings.append({
                "type": "JOINT",
                "severity": "MODERATE",
                "message": "Elevated urate levels - increased gout risk",
                "action": "Dietary modifications and urate monitoring recommended"
            })
        
        return warnings
    
    def _get_risk_based_recommendations(self, risk_level: str, risk_factors: List[str]) -> List[str]:
        """Get recommendations based on risk level"""
        recommendations = []
        
        if risk_level == "HIGH":
            recommendations.append("Immediate consultation with cardiologist recommended.")
            recommendations.append("Consider advanced cardiac imaging if recommended by provider.")
            recommendations.append("Aggressive lifestyle modification program needed.")
        elif risk_level == "MODERATE":
            recommendations.append("Regular cardiovascular monitoring recommended.")
            recommendations.append("Consider cardiac stress testing if recommended by provider.")
            recommendations.append("Moderate lifestyle modifications needed.")
        else:
            recommendations.append("Continue regular preventive care.")
            recommendations.append("Maintain healthy lifestyle habits.")
        
        return recommendations