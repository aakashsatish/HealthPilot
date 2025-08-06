import os
import openai
from typing import Dict, Any, Optional

class AIAnalysisService:
    def __init__(self):
        self.use_openai = os.getenv("USE_OPENAI", "false").lower() == "true"
        
        if self.use_openai:
            # Initialize OpenAI client
            openai.api_key = os.getenv("OPENAI_API_KEY")
            if not openai.api_key:
                raise ValueError("OPENAI_API_KEY environment variable is required when USE_OPENAI=true")
        else:
            # Initialize Ollama client (for local development)
            try:
                import ollama
                self.ollama_client = ollama
            except ImportError:
                raise ImportError("Ollama package not installed. Install with: pip install ollama")

    def analyze_lab_results(self, text: str) -> Dict[str, Any]:
        """
        Analyze lab report text and return structured results
        """
        prompt = f"""
        Analyze this lab report and provide a JSON response with the following structure:
        {{
            "risk_level": "LOW|MODERATE|HIGH|UNKNOWN",
            "summary": "A clear, concise summary of the findings",
            "abnormal_count": number,
            "critical_count": number,
            "recommendations": "Any recommendations for follow-up"
        }}

        Lab Report Text:
        {text}
        """

        if self.use_openai:
            return self._analyze_with_openai(prompt)
        else:
            return self._analyze_with_ollama(prompt)

    def _analyze_with_openai(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze using OpenAI API
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a medical lab report analyzer. Provide accurate, helpful analysis in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            # Parse the response
            content = response.choices[0].message.content
            return self._parse_ai_response(content)
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._get_fallback_response()

    def _analyze_with_ollama(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze using local Ollama
        """
        try:
            response = self.ollama_client.chat(
                model="llama3.1",
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response['message']['content']
            return self._parse_ai_response(content)
            
        except Exception as e:
            print(f"Ollama error: {e}")
            return self._get_fallback_response()

    def _parse_ai_response(self, content: str) -> Dict[str, Any]:
        """
        Parse AI response and extract structured data
        """
        try:
            import json
            # Try to extract JSON from the response
            if "{" in content and "}" in content:
                start = content.find("{")
                end = content.rfind("}") + 1
                json_str = content[start:end]
                result = json.loads(json_str)
                
                # Validate required fields
                required_fields = ["risk_level", "summary", "abnormal_count", "critical_count"]
                for field in required_fields:
                    if field not in result:
                        result[field] = "UNKNOWN" if field == "risk_level" else 0
                
                return result
            else:
                return self._get_fallback_response()
                
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return self._get_fallback_response()

    def _get_fallback_response(self) -> Dict[str, Any]:
        """
        Return fallback response when AI analysis fails
        """
        return {
            "risk_level": "UNKNOWN",
            "summary": "Unable to analyze report at this time. Please try again later.",
            "abnormal_count": 0,
            "critical_count": 0,
            "recommendations": "Please consult with a healthcare provider for proper interpretation."
        }