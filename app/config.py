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
    
    # Gemini AI settings
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    # Available models: gemini-2.5-flash, gemini-flash-latest, gemini-2.0-flash-001
    GEMINI_MODEL = 'gemini-2.5-flash'  # Stable, fast, and supports up to 1M tokens
    
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

