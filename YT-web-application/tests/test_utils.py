"""
Unit tests for utility functions.

This module contains test cases for input validation and sanitization.
"""

import unittest
from app.utils import (
    is_valid_youtube_url,
    sanitize_filename,
    extract_video_id,
    validate_quality
)


class TestValidation(unittest.TestCase):
    """Test cases for validation functions."""
    
    def test_valid_youtube_urls(self):
        """Test valid YouTube URLs."""
        valid_urls = [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'http://youtube.com/watch?v=dQw4w9WgXcQ',
            'https://youtu.be/dQw4w9WgXcQ',
            'https://www.youtube.com/embed/dQw4w9WgXcQ',
        ]
        
        for url in valid_urls:
            with self.subTest(url=url):
                self.assertTrue(is_valid_youtube_url(url))
    
    def test_invalid_youtube_urls(self):
        """Test invalid YouTube URLs."""
        invalid_urls = [
            '',
            'not a url',
            'https://www.google.com',
            'https://vimeo.com/123456',
        ]
        
        for url in invalid_urls:
            with self.subTest(url=url):
                self.assertFalse(is_valid_youtube_url(url))
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        test_cases = [
            ('normal_file.mp4', 'normal_file.mp4'),
            ('file<>:"/\\|?*.mp4', 'file.mp4'),
            ('  spaces  ', 'spaces'),
            ('', ''),
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input=input_name):
                result = sanitize_filename(input_name)
                self.assertEqual(result, expected)
    
    def test_extract_video_id(self):
        """Test video ID extraction."""
        test_cases = [
            ('https://www.youtube.com/watch?v=dQw4w9WgXcQ', 'dQw4w9WgXcQ'),
            ('https://youtu.be/dQw4w9WgXcQ', 'dQw4w9WgXcQ'),
            ('https://www.youtube.com/embed/dQw4w9WgXcQ', 'dQw4w9WgXcQ'),
            ('https://www.google.com', None),
        ]
        
        for url, expected_id in test_cases:
            with self.subTest(url=url):
                result = extract_video_id(url)
                self.assertEqual(result, expected_id)
    
    def test_validate_quality(self):
        """Test quality validation."""
        # Valid video qualities
        for quality in ['144', '240', '360', '480', '720', '1080', 'best']:
            self.assertTrue(validate_quality(quality, 'video'))
        
        # Valid audio qualities
        for quality in ['64', '128', '192', '256', '320']:
            self.assertTrue(validate_quality(quality, 'audio'))
        
        # Invalid qualities
        self.assertFalse(validate_quality('999', 'video'))
        self.assertFalse(validate_quality('invalid', 'audio'))


if __name__ == '__main__':
    unittest.main()
