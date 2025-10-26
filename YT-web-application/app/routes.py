"""
Flask routes module.

This module defines all the API endpoints and routes for the application.
"""

import os
import logging
from flask import (
    Blueprint, 
    render_template, 
    request, 
    jsonify, 
    send_file,
    current_app
)
from typing import Dict, Tuple
from app.downloader import YouTubeDownloader
from app.config import Config


logger = logging.getLogger(__name__)
main_bp = Blueprint('main', __name__)

# Global downloader instance
downloader: YouTubeDownloader = None


def get_downloader() -> YouTubeDownloader:
    """
    Get or create the downloader instance.
    
    Returns:
        YouTubeDownloader instance.
    """
    global downloader
    if downloader is None:
        downloader = YouTubeDownloader(current_app.config['DOWNLOAD_FOLDER'])
    return downloader


@main_bp.route('/')
def index() -> str:
    """
    Render the main application page.
    
    Returns:
        Rendered HTML template.
    """
    return render_template(
        'index.html',
        audio_qualities=Config.AUDIO_QUALITIES,
        video_qualities=Config.VIDEO_QUALITIES
    )


@main_bp.route('/about')
def about() -> str:
    """
    Render the about page.
    
    Returns:
        Rendered HTML template.
    """
    return render_template('about.html')


@main_bp.route('/api/video-info', methods=['POST'])
def get_video_info() -> Tuple[Dict, int]:
    """
    Get video information without downloading.
    
    Returns:
        JSON response with video metadata or error.
    """
    try:
        data = request.get_json()
        url = (data.get('url') or '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        dl = get_downloader()
        info = dl.get_video_info(url)
        
        return jsonify({'success': True, 'info': info}), 200
    
    except Exception as e:
        logger.error(f"Error in get_video_info: {str(e)}")
        return jsonify({'error': str(e)}), 400


@main_bp.route('/api/download', methods=['POST'])
def download() -> Tuple[Dict, int]:
    """
    Initiate video or audio download.
    
    Returns:
        JSON response with download result or error.
    """
    try:
        data = request.get_json()
        url = (data.get('url') or '').strip()
        download_type = data.get('type', 'video')
        quality = data.get('quality', 'best')
        filename = (data.get('filename') or '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        dl = get_downloader()
        
        if download_type == 'audio':
            result = dl.download_audio(
                url, 
                quality=quality,
                filename=filename if filename else None
            )
        else:
            result = dl.download_video(
                url, 
                quality=quality,
                filename=filename if filename else None
            )
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in download: {str(e)}")
        return jsonify({'error': str(e)}), 400


@main_bp.route('/api/progress', methods=['GET'])
def get_progress() -> Tuple[Dict, int]:
    """
    Get current download progress.
    
    Returns:
        JSON response with progress information.
    """
    try:
        dl = get_downloader()
        progress = dl.get_progress()
        return jsonify(progress), 200
    
    except Exception as e:
        logger.error(f"Error in get_progress: {str(e)}")
        return jsonify({'error': str(e)}), 500


@main_bp.route('/api/download-file/<filename>', methods=['GET'])
def download_file(filename: str) -> send_file:
    """
    Download a file from the server.
    
    Args:
        filename: Name of the file to download.
        
    Returns:
        File download response.
    """
    try:
        file_path = os.path.join(current_app.config['DOWNLOAD_FOLDER'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        logger.error(f"Error in download_file: {str(e)}")
        return jsonify({'error': str(e)}), 500


@main_bp.errorhandler(404)
def not_found(error) -> Tuple[Dict, int]:
    """Handle 404 errors."""
    return jsonify({'error': 'Resource not found'}), 404


@main_bp.errorhandler(500)
def internal_error(error) -> Tuple[Dict, int]:
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500
