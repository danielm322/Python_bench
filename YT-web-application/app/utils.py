"""
Utility module for input validation and sanitization.

This module provides functions to validate and sanitize user inputs.
"""

import re
from typing import Optional
from urllib.parse import urlparse, parse_qs


def is_valid_youtube_url(url: str) -> bool:
    """
    Validate if the provided URL is a valid YouTube URL.
    
    Args:
        url: URL string to validate.
        
    Returns:
        True if valid YouTube URL, False otherwise.
    """
    if not url:
        return False
    
    # YouTube URL patterns
    youtube_patterns = [
        r'^https?://(www\.)?youtube\.com/watch\?v=[\w-]+',
        r'^https?://(www\.)?youtube\.com/embed/[\w-]+',
        r'^https?://youtu\.be/[\w-]+',
    ]
    
    return any(re.match(pattern, url) for pattern in youtube_patterns)


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove invalid characters.
    
    Args:
        filename: Original filename.
        
    Returns:
        Sanitized filename safe for file systems.
    """
    if not filename:
        return ''
    
    # Remove invalid characters for file systems
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '', filename)
    
    # Trim whitespace
    sanitized = sanitized.strip()
    
    # Limit length
    max_length = 200
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def extract_video_id(url: str) -> Optional[str]:
    """
    Extract video ID from YouTube URL.
    
    Args:
        url: YouTube URL.
        
    Returns:
        Video ID if found, None otherwise.
    """
    parsed = urlparse(url)
    
    # Handle different YouTube URL formats
    if parsed.hostname in ['www.youtube.com', 'youtube.com']:
        if parsed.path == '/watch':
            query_params = parse_qs(parsed.query)
            return query_params.get('v', [None])[0]
        elif parsed.path.startswith('/embed/'):
            return parsed.path.split('/')[2]
    elif parsed.hostname == 'youtu.be':
        return parsed.path[1:]
    
    return None


def validate_quality(quality: str, download_type: str) -> bool:
    """
    Validate quality parameter.
    
    Args:
        quality: Quality value to validate.
        download_type: Type of download ('video' or 'audio').
        
    Returns:
        True if valid, False otherwise.
    """
    if download_type == 'video':
        valid_qualities = ['144', '240', '360', '480', '720', '1080', 'best']
        return quality in valid_qualities
    elif download_type == 'audio':
        valid_qualities = ['64', '128', '192', '256', '320']
        return quality in valid_qualities
    
    return False
