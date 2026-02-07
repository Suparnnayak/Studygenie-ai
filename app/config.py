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
        "llama-3.3-70b-versatile"  # Default: latest 70B model (replaces deprecated llama-3.1-70b-versatile)
    )

    SUPPORTED_GROQ_MODELS = {
        "llama-3.3-70b-versatile",  # Latest 70B model
        "llama-3.1-8b-instant",      # Fast 8B model
        "llama-3.1-70b-versatile",   # Deprecated but kept for reference
        "mixtral-8x7b-32768",        # Mixtral model
        "gemma2-9b-it"               # Gemma 2 model
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

        # Note: Model validation is lenient - Groq may support models not in our list
        # We log a warning but don't fail, allowing flexibility for new models
        if cls.GROQ_MODEL not in cls.SUPPORTED_GROQ_MODELS:
            import warnings
            warnings.warn(
                f"GROQ_MODEL '{cls.GROQ_MODEL}' not in known supported models. "
                f"Known models: {cls.SUPPORTED_GROQ_MODELS}. "
                f"Proceeding anyway - Groq may support this model."
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
