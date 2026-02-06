"""
JSON validation utilities for AI responses
"""
import json
import re
from typing import Dict, Any, Optional


class JSONValidationError(Exception):
    """Custom exception for JSON validation errors"""
    pass


def extract_json_from_text(text: str) -> str:
    """
    Extract JSON from text that may contain markdown or other formatting
    
    Args:
        text: Text that may contain JSON
        
    Returns:
        Extracted JSON string
        
    Raises:
        JSONValidationError: If no valid JSON found
    """
    # Remove markdown code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    # Try to find JSON object boundaries
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        return json_match.group(0)
    
    # If no match, return original text
    return text.strip()


def safe_parse_json(text: str) -> Dict[str, Any]:
    """
    Safely parse JSON string with error handling
    
    Args:
        text: JSON string to parse
        
    Returns:
        Parsed JSON dictionary
        
    Raises:
        JSONValidationError: If JSON is invalid
    """
    if not text:
        raise JSONValidationError("Empty JSON string provided")
    
    try:
        # First, try to extract JSON if wrapped in markdown
        json_str = extract_json_from_text(text)
        
        # Parse JSON
        parsed = json.loads(json_str)
        
        if not isinstance(parsed, dict):
            raise JSONValidationError("JSON root must be an object")
        
        return parsed
        
    except json.JSONDecodeError as e:
        raise JSONValidationError(f"Invalid JSON format: {str(e)}")
    except Exception as e:
        raise JSONValidationError(f"Error parsing JSON: {str(e)}")


def validate_json_structure(data: Dict[str, Any], required_keys: list) -> bool:
    """
    Validate that JSON contains required keys
    
    Args:
        data: JSON dictionary to validate
        required_keys: List of required key names
        
    Returns:
        True if valid
        
    Raises:
        JSONValidationError: If validation fails
    """
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        raise JSONValidationError(f"Missing required keys: {', '.join(missing_keys)}")
    return True

