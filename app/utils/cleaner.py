"""
Text cleaning utilities for PDF extraction
"""
import re


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text by removing artifacts and normalizing whitespace
    
    Args:
        text: Raw text extracted from PDF
        
    Returns:
        Cleaned text string
    """
    if not text:
        return ""
    
    # Remove excessive whitespace (multiple spaces, tabs, newlines)
    text = re.sub(r'\s+', ' ', text)
    
    # Normalize bullets (various bullet characters to standard dash)
    text = re.sub(r'[•▪▫◦‣⁃]', '-', text)
    
    # Remove page numbers and headers/footers (common patterns)
    text = re.sub(r'Page \d+', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\d+\s*$', '', text, flags=re.MULTILINE)
    
    # Remove excessive dashes/separators
    text = re.sub(r'-{3,}', '---', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove empty lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    text = '\n'.join(lines)
    
    return text


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text
    
    Args:
        text: Text to normalize
        
    Returns:
        Normalized text
    """
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    # Replace multiple newlines with double newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

