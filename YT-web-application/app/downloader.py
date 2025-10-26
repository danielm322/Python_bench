"""
YouTube downloader service module.

This module provides the core functionality for downloading YouTube videos and audio
using yt-dlp with progress tracking and error handling.
"""

import os
import logging
from typing import Dict, Optional, Callable
from pathlib import Path
import yt_dlp


logger = logging.getLogger(__name__)


class DownloadProgress:
    """Track download progress for real-time updates."""
    
    def __init__(self):
        """Initialize progress tracker."""
        self.status: str = 'idle'
        self.percentage: float = 0.0
        self.speed: str = 'N/A'
        self.eta: str = 'N/A'
        self.downloaded: str = '0 MB'
        self.total: str = '0 MB'
        self.filename: str = ''
        self.error: Optional[str] = None
    
    def update(self, data: Dict) -> None:
        """
        Update progress data from yt-dlp hook.
        
        Args:
            data: Progress data dictionary from yt-dlp.
        """
        self.status = data.get('status', 'unknown')
        
        if self.status == 'downloading':
            total = data.get('total_bytes') or data.get('total_bytes_estimate', 0)
            downloaded = data.get('downloaded_bytes', 0)
            
            if total > 0:
                self.percentage = (downloaded / total) * 100
            else:
                self.percentage = 0
            
            # Format speed
            speed = data.get('speed')
            if speed:
                self.speed = f"{speed / 1024 / 1024:.2f} MB/s"
            
            # Format ETA
            eta = data.get('eta')
            if eta:
                self.eta = f"{eta}s"
            
            # Format sizes
            self.downloaded = f"{downloaded / 1024 / 1024:.2f} MB"
            if total > 0:
                self.total = f"{total / 1024 / 1024:.2f} MB"
            
            self.filename = data.get('filename', '')
        
        elif self.status == 'finished':
            self.percentage = 100.0
            self.filename = data.get('filename', '')
    
    def to_dict(self) -> Dict:
        """
        Convert progress to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of progress.
        """
        return {
            'status': self.status,
            'percentage': round(self.percentage, 2),
            'speed': self.speed,
            'eta': self.eta,
            'downloaded': self.downloaded,
            'total': self.total,
            'filename': os.path.basename(self.filename) if self.filename else '',
            'error': self.error
        }


class YouTubeDownloader:
    """Service class for downloading YouTube videos and audio."""
    
    def __init__(self, download_folder: str):
        """
        Initialize the YouTube downloader service.
        
        Args:
            download_folder: Path to the folder where downloads will be saved.
        """
        self.download_folder = Path(download_folder)
        self.download_folder.mkdir(parents=True, exist_ok=True)
        self.progress = DownloadProgress()
    
    def _progress_hook(self, data: Dict) -> None:
        """
        Hook function called by yt-dlp during download.
        
        Args:
            data: Progress data from yt-dlp.
        """
        self.progress.update(data)
        logger.info(f"Download progress: {self.progress.percentage:.2f}%")
    
    def _get_base_ydl_opts(self) -> Dict:
        """
        Get base yt-dlp options with proper headers and configurations.
        
        Returns:
            Dictionary with base yt-dlp options.
        """
        return {
            'noplaylist': True,  # Don't download playlists, only single videos
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'skip': ['hls', 'dash'],  # Skip problematic formats
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
        }
    
    def get_video_info(self, url: str) -> Dict:
        """
        Retrieve video information without downloading.
        
        Args:
            url: YouTube video URL.
            
        Returns:
            Dictionary containing video metadata.
            
        Raises:
            Exception: If video info cannot be retrieved.
        """
        ydl_opts = {
            **self._get_base_ydl_opts(),
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'upload_date': info.get('upload_date', ''),
                    'description': info.get('description', '')[:200] + '...',
                }
        except Exception as e:
            logger.error(f"Error retrieving video info: {str(e)}")
            raise Exception(f"Failed to retrieve video information: {str(e)}")
    
    def download_video(
        self, 
        url: str, 
        quality: str = 'best',
        filename: Optional[str] = None
    ) -> Dict:
        """
        Download video from YouTube.
        
        Args:
            url: YouTube video URL.
            quality: Video quality (e.g., '720', '1080', 'best').
            filename: Optional custom filename (without extension).
            
        Returns:
            Dictionary with download result information.
            
        Raises:
            Exception: If download fails.
        """
        self.progress = DownloadProgress()
        
        # Determine format string
        if quality == 'best':
            format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        else:
            format_str = f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]/best'
        
        output_template = str(self.download_folder / (filename or '%(title)s.%(ext)s'))
        
        ydl_opts = {
            **self._get_base_ydl_opts(),
            'format': format_str,
            'outtmpl': output_template,
            'progress_hooks': [self._progress_hook],
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                final_filename = ydl.prepare_filename(info)
                
                return {
                    'success': True,
                    'filename': os.path.basename(final_filename),
                    'path': final_filename,
                    'title': info.get('title', 'Unknown'),
                }
        except Exception as e:
            logger.error(f"Error downloading video: {str(e)}")
            self.progress.error = str(e)
            raise Exception(f"Failed to download video: {str(e)}")
    
    def download_audio(
        self, 
        url: str, 
        quality: str = '192',
        filename: Optional[str] = None
    ) -> Dict:
        """
        Download audio from YouTube and convert to MP3.
        
        Args:
            url: YouTube video URL.
            quality: Audio bitrate in kbps (e.g., '128', '192', '320').
            filename: Optional custom filename (without extension).
            
        Returns:
            Dictionary with download result information.
            
        Raises:
            Exception: If download fails.
        """
        self.progress = DownloadProgress()
        
        output_template = str(self.download_folder / (filename or '%(title)s.%(ext)s'))
        
        ydl_opts = {
            **self._get_base_ydl_opts(),
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'progress_hooks': [self._progress_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': quality,
            }],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Get the final filename after post-processing
                base_filename = ydl.prepare_filename(info)
                final_filename = os.path.splitext(base_filename)[0] + '.mp3'
                
                return {
                    'success': True,
                    'filename': os.path.basename(final_filename),
                    'path': final_filename,
                    'title': info.get('title', 'Unknown'),
                }
        except Exception as e:
            logger.error(f"Error downloading audio: {str(e)}")
            self.progress.error = str(e)
            raise Exception(f"Failed to download audio: {str(e)}")
    
    def get_progress(self) -> Dict:
        """
        Get current download progress.
        
        Returns:
            Dictionary with current progress information.
        """
        return self.progress.to_dict()
