"""
AI service for interacting with Groq API
"""
from groq import Groq
from typing import Dict, Any, Optional
from app.config import Config
from app.utils.json_validator import safe_parse_json, JSONValidationError


class AIService:
    """Service for interacting with Groq AI"""
    
    def __init__(self):
        """Initialize Groq AI client"""
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.GROQ_MODEL
    
    def generate_response(
        self,
        prompt: str,
        max_retries: int = 1,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Generate JSON response from Groq AI with retry logic
        
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
        
        last_error = None
        current_prompt = json_prompt
        
        for attempt in range(max_retries + 1):
            try:
                # Generate response using Groq API
                # Note: Groq may not support response_format, so we rely on prompt engineering
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": current_prompt
                        }
                    ],
                    temperature=temperature
                )
                
                if not response.choices or not response.choices[0].message.content:
                    raise ValueError("Empty response from Groq API")
                
                response_text = response.choices[0].message.content
                
                # Parse and validate JSON
                parsed_json = safe_parse_json(response_text)
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
                raise Exception(f"Groq API error: {str(e)}")
        
        # Should not reach here, but handle just in case
        raise last_error or Exception("Failed to generate valid response")
    
    def generate_text_response(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Generate plain text response from Groq AI
        
        Args:
            prompt: Prompt to send to AI
            temperature: Temperature setting for generation
            
        Returns:
            Text response string
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature
            )
            
            if response.choices and response.choices[0].message.content:
                return response.choices[0].message.content
            return ""
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")

