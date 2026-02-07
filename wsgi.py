"""
WSGI entry point for production deployment
"""
import os
from app.main import create_app

# Create the Flask application instance
app = create_app()

# This is required for gunicorn
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

