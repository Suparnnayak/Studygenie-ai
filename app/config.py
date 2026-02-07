"""
Configuration settings for StudyGenie AI Backend
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Groq AI settings
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    # Available models: llama-3.1-70b-versatile, llama-3.1-8b-instant, mixtral-8x7b-32768
    GROQ_MODEL = 'llama-3.1-70b-versatile'  # High-performance model for complex tasks
    
    # Text processing settings
    CHUNK_SIZE = 1500
    CHUNK_OVERLAP = 200
    
    # CORS settings
    _cors_origins = os.getenv('CORS_ORIGINS', '*')
    CORS_ORIGINS = '*' if _cors_origins == '*' else [origin.strip() for origin in _cors_origins.split(',')]
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        # Ensure upload directory exists
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

