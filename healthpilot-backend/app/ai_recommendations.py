import requests
import json
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AIRecommendationService:
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
    
    def generate_recommendations(self, lab_results: List[Dict], age: int = None, sex: str = None) -> List[str]:
        """Generate AI-powered recommendations based on lab results"""
        try:
            # Create prompt for the AI
            prompt = self._create_prompt(lab_results, age, sex)
            
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
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                recommendations = self._parse_ai_response(result['response'])
                return recommendations
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return self._get_fallback_recommendations(lab_results)
                
        except Exception as e:
            logger.error(f"AI recommendation error: {e}")
            return self._get_fallback_recommendations(lab_results)
    
    def _create_prompt(self, lab_results: List[Dict], age: int = None, sex: str = None) -> str:
        """Create a prompt for the AI based on lab results"""
        
        # Format lab results for the prompt
        results_text = ""
        for result in lab_results:
            status = "NORMAL" if result["classification"] == "NORMAL" else f"{result['classification']}"
            results_text += f"- {result['original_name']}: {result['value']} {result['unit']} ({status})\n"
        
        prompt = f"""You are a helpful medical AI assistant. Based on the following lab results, provide 5-8 concise, actionable health recommendations in plain English. Focus on lifestyle changes, dietary advice, and when to see a doctor.

Lab Results:
{results_text}

Patient Info: {age} year old {sex if sex else 'person'}

Instructions:
- Keep each recommendation under 15 words
- Focus on practical, actionable advice
- Use simple, non-medical language
- Prioritize the most important recommendations first
- Include both immediate actions and long-term lifestyle changes

Provide only the recommendations, one per line, starting with a bullet point (•). Do not include explanations or additional text."""

        return prompt
    
    def _parse_ai_response(self, response: str) -> List[str]:
        """Parse the AI response into a list of recommendations"""
        recommendations = []
        
        # Split by lines and clean up
        lines = response.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('•') or line.startswith('-'):
                # Remove bullet point and clean
                clean_line = line[1:].strip()
                if clean_line and len(clean_line) > 5:
                    recommendations.append(clean_line)
            elif line and not line.startswith('Lab Results:') and not line.startswith('Patient Info:'):
                # If no bullet point, treat as recommendation if it looks like one
                if len(line) > 5 and len(line) < 100:
                    recommendations.append(line)
        
        # Limit to 8 recommendations max
        return recommendations[:8]
    
    def _get_fallback_recommendations(self, lab_results: List[Dict]) -> List[str]:
        """Fallback recommendations if AI fails"""
        return [
            "Discuss these results with your healthcare provider.",
            "Consider lifestyle modifications based on your results.",
            "Schedule follow-up testing as recommended by your doctor."
        ]