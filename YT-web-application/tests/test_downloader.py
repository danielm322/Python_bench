"""
Unit tests for the YouTube downloader service.

This module contains test cases for the downloader functionality.
"""

import unittest
import os
from pathlib import Path
from app.downloader import YouTubeDownloader, DownloadProgress


class TestDownloadProgress(unittest.TestCase):
    """Test cases for DownloadProgress class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.progress = DownloadProgress()
    
    def test_initial_state(self):
        """Test initial progress state."""
        self.assertEqual(self.progress.status, 'idle')
        self.assertEqual(self.progress.percentage, 0.0)
        self.assertEqual(self.progress.speed, 'N/A')
        self.assertEqual(self.progress.eta, 'N/A')
    
    def test_update_downloading(self):
        """Test progress update during download."""
        data = {
            'status': 'downloading',
            'total_bytes': 1000000,
            'downloaded_bytes': 500000,
            'speed': 102400,
            'eta': 5,
            'filename': 'test_video.mp4'
        }
        self.progress.update(data)
        
        self.assertEqual(self.progress.status, 'downloading')
        self.assertEqual(self.progress.percentage, 50.0)
        self.assertIn('MB/s', self.progress.speed)
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        result = self.progress.to_dict()
        
        self.assertIsInstance(result, dict)
        self.assertIn('status', result)
        self.assertIn('percentage', result)
        self.assertIn('speed', result)


class TestYouTubeDownloader(unittest.TestCase):
    """Test cases for YouTubeDownloader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_folder = Path('test_downloads')
        self.test_folder.mkdir(exist_ok=True)
        self.downloader = YouTubeDownloader(str(self.test_folder))
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up downloaded files
        if self.test_folder.exists():
            for file in self.test_folder.glob('*'):
                file.unlink()
            self.test_folder.rmdir()
    
    def test_initialization(self):
        """Test downloader initialization."""
        self.assertTrue(self.test_folder.exists())
        self.assertIsInstance(self.downloader.progress, DownloadProgress)
    
    def test_get_progress(self):
        """Test get progress method."""
        progress = self.downloader.get_progress()
        
        self.assertIsInstance(progress, dict)
        self.assertIn('status', progress)
        self.assertIn('percentage', progress)


if __name__ == '__main__':
    unittest.main()
