"""
StudyGenie AI Backend - Main Flask Application
"""
import os
from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.api.routes import api_bp


def create_app(config_class=Config):
    """
    Create and configure Flask application
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize config
    config_class.init_app(app)
    
    # Enable CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return {'status': 'healthy', 'service': 'StudyGenie AI Backend'}, 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    # Get port from environment variable (for Render) or default to 5000
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)

