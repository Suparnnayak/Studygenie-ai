"""
AI service for interacting with Google Gemini API
"""
import google.generativeai as genai
from typing import Dict, Any, Optional
from app.config import Config
from app.utils.json_validator import safe_parse_json, JSONValidationError


class AIService:
    """Service for interacting with Gemini AI"""
    
    def __init__(self):
        """Initialize Gemini AI client"""
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
    
    def generate_response(
        self,
        prompt: str,
        max_retries: int = 1,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate JSON response from Gemini AI with retry logic
        
        Args:
            prompt: Prompt to send to AI
            max_retries: Maximum number of retries if JSON is invalid
            temperature: Temperature setting for generation
            
        Returns:
            Parsed JSON dictionary
            
        Raises:
            JSONValidationError: If JSON cannot be parsed after retries
            Exception: If API call fails
        """
        # Enhance prompt to ensure JSON output
        json_prompt = f"""{prompt}

CRITICAL: You must respond with ONLY valid JSON. Do not include markdown code blocks, explanations, or any text outside the JSON. Start your response directly with {{ and end with }}."""
        
        generation_config = {
            'temperature': temperature,
        }
        
        last_error = None
        current_prompt = json_prompt
        
        for attempt in range(max_retries + 1):
            try:
                # Generate response
                response = self.model.generate_content(
                    current_prompt,
                    generation_config=generation_config
                )
                
                if not response.text:
                    raise ValueError("Empty response from Gemini API")
                
                # Parse and validate JSON
                parsed_json = safe_parse_json(response.text)
                return parsed_json
                
            except JSONValidationError as e:
                last_error = e
                if attempt < max_retries:
                    # Retry with even stricter prompt
                    current_prompt = f"""{prompt}

URGENT: Return ONLY valid JSON. No markdown, no code blocks, no explanations. Pure JSON only. Start with {{ and end with }}."""
                    continue
                else:
                    raise
            except Exception as e:
                if attempt < max_retries:
                    continue
                raise Exception(f"Gemini API error: {str(e)}")
        
        # Should not reach here, but handle just in case
        raise last_error or Exception("Failed to generate valid response")
    
    def generate_text_response(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Generate plain text response from Gemini AI
        
        Args:
            prompt: Prompt to send to AI
            temperature: Temperature setting for generation
            
        Returns:
            Text response string
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={'temperature': temperature}
            )
            return response.text if response.text else ""
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")

