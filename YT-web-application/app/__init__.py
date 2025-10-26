"""
Flask application factory module.

This module initializes and configures the Flask application with all necessary
settings, extensions, and blueprints.
"""

import os
import logging
from flask import Flask
from logging.handlers import RotatingFileHandler


def create_app() -> Flask:
    """
    Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DOWNLOAD_FOLDER'] = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        'downloads'
    )
    app.config['MAX_CONTENT_LENGTH'] = int(
        os.environ.get('MAX_CONTENT_LENGTH', 524288000)
    )
    
    # Ensure download folder exists
    os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)
    
    # Configure logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/yt_downloader.log', 
            maxBytes=10240000, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('YouTube Downloader startup')
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
