"""
Text chunking service for processing large documents
"""
from typing import List


class ChunkService:
    """Service for chunking text into manageable pieces"""
    
    def __init__(self, chunk_size: int = 1500, chunk_overlap: int = 200):
        """
        Initialize chunking service
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            # Calculate end position
            end = start + self.chunk_size
            
            # If this is not the last chunk, try to break at word boundary
            if end < text_length:
                # Look for sentence boundary near the end
                last_period = text.rfind('.', start, end)
                last_newline = text.rfind('\n', start, end)
                
                # Prefer sentence boundary, then paragraph boundary
                if last_period > start + self.chunk_size * 0.7:
                    end = last_period + 1
                elif last_newline > start + self.chunk_size * 0.7:
                    end = last_newline + 1
            
            # Extract chunk
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            if start >= text_length:
                break
        
        return chunks if chunks else [text]

