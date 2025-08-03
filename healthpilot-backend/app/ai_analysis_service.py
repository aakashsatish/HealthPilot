import requests
import json
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AIAnalysisService:
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
    
    def generate_full_analysis(self, lab_results: List[Dict], age: int = None, sex: str = None) -> Dict[str, Any]:
        """Generate complete AI-powered analysis"""
        try:
            # Create comprehensive prompt for full analysis
            prompt = self._create_full_analysis_prompt(lab_results, age, sex)
            
            # Call Ollama API
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "llama3.1:8b",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = self._parse_full_analysis_response(result['response'], lab_results)
                return analysis
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return self._get_fallback_analysis(lab_results)
                
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            return self._get_fallback_analysis(lab_results)
    
    def _create_full_analysis_prompt(self, lab_results: List[Dict], age: int = None, sex: str = None) -> str:
        """Create a comprehensive prompt for full analysis"""
        
        # Format lab results for the prompt
        results_text = ""
        abnormal_count = 0
        for result in lab_results:
            status = "NORMAL" if result["classification"] == "NORMAL" else f"{result['classification']}"
            if result["classification"] != "NORMAL":
                abnormal_count += 1
            results_text += f"- {result['original_name']}: {result['value']} {result['unit']} ({status})\n"
        
        prompt = f"""You are a medical AI assistant. Analyze these lab results and provide a comprehensive health assessment in JSON format.

Lab Results:
{results_text}

Patient Info: {age} year old {sex if sex else 'person'}
Abnormal Results: {abnormal_count} out of {len(lab_results)} tests

Provide a JSON response with the following structure:
{{
  "summary": "Plain English summary of the results in 2-3 sentences",
  "risk_level": "LOW/MODERATE/HIGH",
  "risk_factors": ["factor1", "factor2"],
  "early_warnings": [
    {{
      "type": "CARDIOVASCULAR/METABOLIC/JOINT/etc",
      "severity": "LOW/MODERATE/HIGH",
      "message": "Brief warning message",
      "action": "Recommended action"
    }}
  ],
  "recommendations": [
    "Recommendation 1 (under 15 words)",
    "Recommendation 2 (under 15 words)",
    "Recommendation 3 (under 15 words)"
  ]
}}

Focus on:
- Cardiovascular risk (cholesterol, triglycerides)
- Metabolic health (urate, glucose)
- Lifestyle recommendations
- Medical follow-up needs
- Age and sex considerations

Provide only valid JSON, no additional text."""

        return prompt
    
    def _parse_full_analysis_response(self, response: str, lab_results: List[Dict]) -> Dict[str, Any]:
        """Parse the AI response into structured analysis"""
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                analysis = json.loads(json_str)
                
                # Ensure all required fields exist
                analysis.setdefault("summary", "Analysis completed")
                analysis.setdefault("risk_level", "LOW")
                analysis.setdefault("risk_factors", [])
                analysis.setdefault("early_warnings", [])
                analysis.setdefault("recommendations", [])
                
                return analysis
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as e:
            logger.error(f"Failed to parse AI response: {e}")
            return self._get_fallback_analysis(lab_results)
    
    def _get_fallback_analysis(self, lab_results: List[Dict]) -> Dict[str, Any]:
        """Fallback analysis if AI fails"""
        return {
            "summary": "Lab results analyzed. Discuss with your healthcare provider.",
            "risk_level": "MODERATE",
            "risk_factors": ["Multiple abnormal results"],
            "early_warnings": [],
            "recommendations": [
                "Discuss these results with your healthcare provider.",
                "Consider lifestyle modifications based on your results.",
                "Schedule follow-up testing as recommended by your doctor."
            ]
        }