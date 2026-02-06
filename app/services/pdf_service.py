"""
PDF extraction service using pdfplumber
"""
import pdfplumber
from typing import Optional
from app.utils.cleaner import clean_text


class PDFService:
    """Service for extracting text from PDF files"""
    
    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """
        Extract text from PDF file
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted and cleaned text string
            
        Raises:
            ValueError: If PDF is empty or cannot be read
            FileNotFoundError: If PDF file doesn't exist
        """
        try:
            text_content = []
            
            with pdfplumber.open(pdf_path) as pdf:
                if len(pdf.pages) == 0:
                    raise ValueError("PDF file is empty or corrupted")
                
                # Extract text from each page
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
                
                # Combine all pages
                full_text = '\n\n'.join(text_content)
                
                if not full_text or len(full_text.strip()) < 10:
                    raise ValueError("PDF appears to be scanned or contains no extractable text")
                
                # Clean the extracted text
                cleaned_text = clean_text(full_text)
                
                if not cleaned_text or len(cleaned_text.strip()) < 10:
                    raise ValueError("PDF text extraction resulted in empty or invalid content")
                
                return cleaned_text
                
        except FileNotFoundError:
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        except Exception as e:
            if isinstance(e, (ValueError, FileNotFoundError)):
                raise
            raise ValueError(f"Error extracting text from PDF: {str(e)}")

