"""
Configuration settings for StudyGenie AI Backend
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()


class Config:
    """
    Base application configuration
    """

    # -----------------------
    # Project paths
    # -----------------------
    BASE_DIR = Path(__file__).resolve().parent.parent
    UPLOAD_FOLDER = BASE_DIR / "uploads"

    # -----------------------
    # Flask settings
    # -----------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # -----------------------
    # File upload settings
    # -----------------------
    ALLOWED_EXTENSIONS = {"pdf"}

    # -----------------------
    # Groq AI settings
    # -----------------------
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Supported Groq models
    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "llama-3.1-70b-versatile"  # Default: best reasoning
    )

    SUPPORTED_GROQ_MODELS = {
        "llama-3.1-8b-instant"
    }

    # -----------------------
    # Text processing
    # -----------------------
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1500))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))

    # Hard cap to protect LLM & memory
    MAX_SYLLABUS_CHARS = int(os.getenv("MAX_SYLLABUS_CHARS", 8000))

    # -----------------------
    # CORS
    # -----------------------
    _cors_origins = os.getenv("CORS_ORIGINS", "*")
    CORS_ORIGINS = (
        "*"
        if _cors_origins == "*"
        else [origin.strip() for origin in _cors_origins.split(",")]
    )

    # -----------------------
    # Validation hooks
    # -----------------------
    @classmethod
    def validate(cls) -> None:
        """Validate critical configuration at startup"""

        if not cls.GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY is not set")

        if cls.GROQ_MODEL not in cls.SUPPORTED_GROQ_MODELS:
            raise RuntimeError(
                f"Unsupported GROQ_MODEL: {cls.GROQ_MODEL}. "
                f"Supported models: {cls.SUPPORTED_GROQ_MODELS}"
            )

    @classmethod
    def init_app(cls, app) -> None:
        """
        Initialize application with configuration
        """
        # Ensure upload directory exists
        cls.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

        # Validate config once at startup
        cls.validate()
