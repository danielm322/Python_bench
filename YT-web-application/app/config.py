"""
Configuration module for the application.

This module contains configuration settings and constants used throughout the application.
"""

import os
from typing import Dict, List


class Config:
    """Base configuration class."""
    
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'downloads')
    MAX_CONTENT_LENGTH = 524288000  # 500 MB
    
    # yt-dlp settings
    AUDIO_QUALITIES: List[Dict[str, str]] = [
        {'value': '64', 'label': '64 kbps'},
        {'value': '128', 'label': '128 kbps'},
        {'value': '192', 'label': '192 kbps'},
        {'value': '256', 'label': '256 kbps'},
        {'value': '320', 'label': '320 kbps (Best)'},
    ]
    
    VIDEO_QUALITIES: List[Dict[str, str]] = [
        {'value': '144', 'label': '144p'},
        {'value': '240', 'label': '240p'},
        {'value': '360', 'label': '360p'},
        {'value': '480', 'label': '480p'},
        {'value': '720', 'label': '720p (HD)'},
        {'value': '1080', 'label': '1080p (Full HD)'},
        {'value': 'best', 'label': 'Best Available'},
    ]
    
    # Progress tracking
    PROGRESS_UPDATE_INTERVAL = 1  # seconds


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
