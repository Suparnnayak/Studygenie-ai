"""
AI service for interacting with Groq API
"""
from typing import Dict, Any
from groq import Groq

from app.config import Config
from app.utils.json_validator import safe_parse_json, JSONValidationError


class AIService:
    """
    Service for interacting with Groq LLMs
    """

    def __init__(self) -> None:
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.GROQ_MODEL

    def generate_json_response(
        self,
        prompt: str,
        max_retries: int = 1,
        temperature: float = 0.2
    ) -> Dict[str, Any]:
        """
        Generate a strict JSON response from Groq

        Args:
            prompt: User prompt
            max_retries: Retry attempts if JSON parsing fails
            temperature: Sampling temperature (keep low for JSON)

        Returns:
            Parsed JSON dictionary

        Raises:
            JSONValidationError
            RuntimeError
        """

        system_prompt = (
            "You are an AI that MUST return ONLY valid JSON.\n"
            "Do not include markdown, explanations, comments, or extra text.\n"
            "The response must start with '{' and end with '}'."
        )

        last_error: Exception | None = None

        for attempt in range(max_retries + 1):
            try:
                # 🥈 FIX 2: Add max_tokens to prevent cutoff and runaway generation
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=temperature,
                    max_tokens=3500,  # Prevent half-finished JSON and keep response bounded
                )

                if not response.choices:
                    raise RuntimeError("Groq API returned no choices")

                content = response.choices[0].message.content
                if not content:
                    raise RuntimeError("Groq API returned empty content")

                return safe_parse_json(content)

            except JSONValidationError as e:
                last_error = e
                
                # 🥉 FIX 3: JSON repair retry - fixes 90% of JSON issues
                if attempt < max_retries:
                    try:
                        repair_prompt = f"""Fix the following invalid JSON.
Return ONLY corrected valid JSON.
Do NOT add or remove fields.
Do NOT include markdown code blocks or explanations.

INVALID JSON:
{content}
"""
                        repair_response = self.client.chat.completions.create(
                            model=self.model,
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": repair_prompt}
                            ],
                            temperature=0,  # Low temperature for repair
                            max_tokens=3000
                        )
                        
                        if repair_response.choices and repair_response.choices[0].message.content:
                            repaired_text = repair_response.choices[0].message.content
                            return safe_parse_json(repaired_text)
                    except Exception:
                        # If repair fails, continue to next retry or raise
                        pass
                
                if attempt >= max_retries:
                    raise
                continue

            except Exception as e:
                last_error = e
                if attempt >= max_retries:
                    raise RuntimeError(f"Groq API error: {str(e)}")
                continue

        raise last_error or RuntimeError("Unknown Groq generation failure")

    def generate_text_response(
        self,
        prompt: str,
        temperature: float = 0.5
    ) -> str:
        """
        Generate a plain-text response from Groq
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
            )

            if response.choices and response.choices[0].message.content:
                return response.choices[0].message.content

            return ""

        except Exception as e:
            raise RuntimeError(f"Groq API error: {str(e)}")
