#!/usr/bin/env python3
"""
YouTube Video Downloader GUI - Fixed Version
A robust PyQt6 application to download YouTube videos with multiple fallback strategies
"""

import sys
import os
import threading
import re
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, 
                            QProgressBar, QMessageBox, QTextEdit, QFrame, QComboBox,
                            QCheckBox, QGroupBox)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont, QIcon
import urllib.request
import ssl
import json


class DownloadThread(QThread):
    """Thread for downloading YouTube videos with multiple strategies"""
    
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    status_update = pyqtSignal(str)
    
    def __init__(self, url, save_path, quality_choice="highest", use_ytdlp=False):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.quality_choice = quality_choice
        self.use_ytdlp = use_ytdlp
        
    def sanitize_url(self, url):
        """Clean and validate YouTube URL"""
        if 'youtube.com' in url or 'youtu.be' in url:
            video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
            if video_id_match:
                video_id = video_id_match.group(1)
                return f"https://www.youtube.com/watch?v={video_id}"
        return url
        
    def download_with_pytube(self):
        """Try downloading with pytube library"""
        try:
            # Import pytube here to avoid import issues
            from pytube import YouTube
            from pytube.exceptions import VideoUnavailable, RegexMatchError, PytubeError
            
            # Fix SSL context
            ssl._create_default_https_context = ssl._create_unverified_context
            
            clean_url = self.sanitize_url(self.url)
            self.status_update.emit(f"Using pytube for: {clean_url}")
            
            # Try multiple approaches
            strategies = [
                lambda: YouTube(clean_url, on_progress_callback=self.progress_callback),
                lambda: YouTube(clean_url),
                lambda: YouTube(clean_url, use_oauth=False, allow_oauth_cache=False)
            ]
            
            yt = None
            for i, strategy in enumerate(strategies):
                try:
                    self.status_update.emit(f"Trying connection strategy {i+1}/3...")
                    yt = strategy()
                    # Test if we can get basic info
                    title = yt.title
                    self.status_update.emit(f"Connected! Video: {title}")
                    break
                except Exception as e:
                    self.status_update.emit(f"Strategy {i+1} failed: {str(e)}")
                    if i == len(strategies) - 1:
                        raise e
                        
            if not yt:
                raise Exception("All connection strategies failed")
                
            # Get streams
            self.status_update.emit("Fetching available streams...")
            streams = yt.streams.all()
            
            if not streams:
                raise Exception("No streams available")
                
            # Select stream based on quality choice
            stream = None
            if self.quality_choice == "highest":
                # Try progressive first, then adaptive
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                if not stream:
                    stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
            elif self.quality_choice == "audio_only":
                # Get best audio stream
                stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
                if not stream:
                    # Fallback to any audio stream
                    stream = yt.streams.filter(only_audio=True).first()
            else:  # medium
                stream = yt.streams.filter(progressive=True, res='720p').first()
                if not stream:
                    stream = yt.streams.filter(progressive=True, res='480p').first()
                    
            if not stream:
                stream = streams[0]
                
            self.status_update.emit(f"Selected: {stream}")
            self.status_update.emit("Starting download...")
            
            filename = stream.download(output_path=self.save_path)
            
            # Convert audio to MP3 if needed
            if self.quality_choice == "audio_only" and not filename.endswith('.mp3'):
                self.status_update.emit("Converting audio to MP3...")
                try:
                    import subprocess
                    from pathlib import Path
                    
                    # Generate MP3 filename
                    original_path = Path(filename)
                    mp3_path = original_path.with_suffix('.mp3')
                    
                    # Try to convert using ffmpeg if available
                    try:
                        result = subprocess.run([
                            'ffmpeg', '-i', str(original_path), 
                            '-acodec', 'mp3', '-y', str(mp3_path)
                        ], capture_output=True, timeout=300)
                        
                        if result.returncode == 0:
                            # Remove original file and use MP3
                            original_path.unlink()
                            filename = str(mp3_path)
                            self.status_update.emit("Audio converted to MP3 successfully")
                        else:
                            self.status_update.emit("FFmpeg conversion failed, keeping original format")
                    except (FileNotFoundError, subprocess.TimeoutExpired):
                        # Rename file to .mp3 extension (basic conversion)
                        mp3_path = original_path.rename(original_path.with_suffix('.mp3'))
                        filename = str(mp3_path)
                        self.status_update.emit("Audio file renamed to .mp3 format")
                        
                except Exception as conv_error:
                    self.status_update.emit(f"Audio conversion warning: {conv_error}")
                    # Continue with original file
            
            return filename
            
        except Exception as e:
            raise Exception(f"Pytube failed: {str(e)}")
            
    def progress_callback(self, stream, chunk, bytes_remaining):
        """Progress callback for pytube"""
        try:
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentage = int((bytes_downloaded / total_size) * 100)
            self.progress.emit(percentage)
        except:
            pass
            
    def download_with_ytdlp(self):
        """Try downloading with yt-dlp as fallback"""
        try:
            # Check if yt-dlp is available
            result = subprocess.run([sys.executable, '-m', 'yt_dlp', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                raise Exception("yt-dlp not found")
                
            self.status_update.emit(f"Using yt-dlp version: {result.stdout.strip()}")
            
            # Check if ffmpeg is available for audio conversion
            ffmpeg_available = False
            try:
                ffmpeg_result = subprocess.run(['ffmpeg', '-version'], 
                                            capture_output=True, timeout=5)
                ffmpeg_available = ffmpeg_result.returncode == 0
            except:
                pass
                
            if self.quality_choice == "audio_only" and not ffmpeg_available:
                self.status_update.emit("Warning: ffmpeg not found - downloading best audio format available")
            
            # Build yt-dlp command
            cmd = [sys.executable, '-m', 'yt_dlp', '--no-playlist']
            
            # Quality selection
            if self.quality_choice == "audio_only":
                cmd.extend(['-f', 'bestaudio'])
                if ffmpeg_available:
                    cmd.extend(['--extract-audio', '--audio-format', 'mp3'])
                    self.status_update.emit("Will convert audio to MP3 format")
                else:
                    self.status_update.emit("Will download in original audio format (ffmpeg not available)")
                cmd.extend(['-o', f'{self.save_path}/%(title)s.%(ext)s'])
            elif self.quality_choice == "highest":
                cmd.extend(['-f', 'best'])
                cmd.extend(['-o', f'{self.save_path}/%(title)s.%(ext)s'])
            else:  # medium
                cmd.extend(['-f', 'best[height<=720]'])
                cmd.extend(['-o', f'{self.save_path}/%(title)s.%(ext)s'])
            cmd.extend(['--newline'])  # For better progress tracking
            cmd.append(self.url)
            
            self.status_update.emit("Starting yt-dlp download...")
            
            # Run yt-dlp
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT, text=True)
            
            filename = None
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    line = output.strip()
                    self.status_update.emit(line)
                    
                    # Try to extract progress
                    if '%' in line and 'ETA' in line:
                        try:
                            progress_match = re.search(r'(\d+(?:\.\d+)?)%', line)
                            if progress_match:
                                percentage = int(float(progress_match.group(1)))
                                self.progress.emit(min(percentage, 99))  # Keep 100% for completion
                        except:
                            pass
                            
                    # Extract filename
                    if 'Destination:' in line:
                        filename_match = re.search(r'Destination: (.+)', line)
                        if filename_match:
                            filename = filename_match.group(1)
                    elif 'has already been downloaded' in line:
                        filename = "File already exists (downloaded previously)"
            
            if process.returncode == 0:
                if not filename:
                    # Look for the most recent file in the directory
                    files = list(Path(self.save_path).glob('*'))
                    if files:
                        latest_file = max(files, key=os.path.getctime)
                        filename = str(latest_file)
                    else:
                        filename = "Downloaded successfully (filename unknown)"
                        
                return filename
            else:
                raise Exception("yt-dlp download failed")
                
        except FileNotFoundError:
            raise Exception("yt-dlp not installed. Install with: pip install yt-dlp")
        except Exception as e:
            raise Exception(f"yt-dlp failed: {str(e)}")
            
    def run(self):
        """Main download process with fallback strategies"""
        try:
            filename = None
            
            if not self.use_ytdlp:
                # Try pytube first
                try:
                    filename = self.download_with_pytube()
                except Exception as e:
                    self.status_update.emit(f"Pytube failed: {str(e)}")
                    self.status_update.emit("Trying yt-dlp fallback...")
                    filename = self.download_with_ytdlp()
            else:
                # Use yt-dlp directly
                filename = self.download_with_ytdlp()
                
            self.progress.emit(100)
            self.finished.emit(f"Download completed successfully!\nSaved as: {filename}")
            
        except Exception as e:
            self.error.emit(str(e))


class YouTubeDownloader(QMainWindow):
    """Enhanced YouTube Downloader GUI"""
    
    def __init__(self):
        super().__init__()
        self.download_thread = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("YouTube Video Downloader - Enhanced")
        self.setGeometry(100, 100, 700, 500)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("YouTube Video Downloader")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # URL input section
        url_group = QGroupBox("Video URL")
        url_layout = QVBoxLayout(url_group)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste YouTube video URL here...")
        self.url_input.setMinimumHeight(35)
        url_layout.addWidget(self.url_input)
        
        main_layout.addWidget(url_group)
        
        # Save path section
        path_group = QGroupBox("Download Location")
        path_layout = QVBoxLayout(path_group)
        
        path_input_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select download folder...")
        self.path_input.setMinimumHeight(35)
        self.path_input.setText(str(Path.home() / "Downloads"))
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.setMinimumHeight(35)
        self.browse_button.setMinimumWidth(80)
        self.browse_button.clicked.connect(self.browse_folder)
        
        path_input_layout.addWidget(self.path_input)
        path_input_layout.addWidget(self.browse_button)
        path_layout.addLayout(path_input_layout)
        
        main_layout.addWidget(path_group)
        
        # Settings section
        settings_group = QGroupBox("Download Settings")
        settings_layout = QVBoxLayout(settings_group)
        
        # Quality selection
        quality_layout = QHBoxLayout()
        quality_label = QLabel("Quality:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([
            "Highest Quality (Video)",
            "Medium Quality (720p/480p Video)",
            "Audio Only (MP3)"
        ])
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_combo)
        quality_layout.addStretch()
        
        # Use yt-dlp option
        self.use_ytdlp_check = QCheckBox("Use yt-dlp (if pytube fails)")
        self.use_ytdlp_check.setChecked(True)
        
        settings_layout.addLayout(quality_layout)
        settings_layout.addWidget(self.use_ytdlp_check)
        
        main_layout.addWidget(settings_group)
        
        # Download button
        self.download_button = QPushButton("Download Video")
        self.download_button.setMinimumHeight(45)
        self.download_button.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.download_button.clicked.connect(self.start_download)
        main_layout.addWidget(self.download_button)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(25)
        main_layout.addWidget(self.progress_bar)
        
        # Status text area
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(120)
        self.status_text.setReadOnly(True)
        self.status_text.setPlaceholderText("Status messages will appear here...")
        main_layout.addWidget(self.status_text)
        
    def browse_folder(self):
        """Open folder selection dialog"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Select Download Folder",
            self.path_input.text() or str(Path.home())
        )
        if folder:
            self.path_input.setText(folder)
            
    def validate_inputs(self):
        """Validate user inputs"""
        url = self.url_input.text().strip()
        save_path = self.path_input.text().strip()
        
        if not url:
            QMessageBox.warning(self, "Invalid Input", "Please enter a YouTube URL.")
            return False
            
        if 'youtube.com' not in url and 'youtu.be' not in url:
            QMessageBox.warning(self, "Invalid URL", "Please enter a valid YouTube URL.")
            return False
            
        if not save_path:
            QMessageBox.warning(self, "Invalid Input", "Please select a download folder.")
            return False
            
        if not os.path.exists(save_path):
            QMessageBox.warning(self, "Invalid Path", "The selected download folder does not exist.")
            return False
            
        if not os.access(save_path, os.W_OK):
            QMessageBox.warning(self, "Permission Error", "You don't have write permission to the selected folder.")
            return False
            
        return True
        
    def start_download(self):
        """Start the download process"""
        if not self.validate_inputs():
            return
            
        # Disable UI elements
        self.download_button.setEnabled(False)
        self.url_input.setEnabled(False)
        self.path_input.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.quality_combo.setEnabled(False)
        self.use_ytdlp_check.setEnabled(False)
        
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Clear status
        self.status_text.clear()
        self.status_text.append("Initializing download...")
        
        # Get settings
        quality_map = {0: "highest", 1: "medium", 2: "audio_only"}
        quality_choice = quality_map.get(self.quality_combo.currentIndex(), "highest")
        use_ytdlp = self.use_ytdlp_check.isChecked()
        
        # Start download thread
        url = self.url_input.text().strip()
        save_path = self.path_input.text().strip()
        
        self.download_thread = DownloadThread(url, save_path, quality_choice, use_ytdlp)
        self.download_thread.progress.connect(self.update_progress)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.error.connect(self.download_error)
        self.download_thread.status_update.connect(self.update_status)
        self.download_thread.start()
        
    def update_progress(self, percentage):
        """Update progress bar"""
        self.progress_bar.setValue(percentage)
        
    def update_status(self, message):
        """Update status text"""
        self.status_text.append(message)
        cursor = self.status_text.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.status_text.setTextCursor(cursor)
        
    def download_finished(self, message):
        """Handle successful download"""
        self.progress_bar.setValue(100)
        self.status_text.append("✓ " + message)
        QMessageBox.information(self, "Download Complete", message)
        self.reset_ui()
        
    def download_error(self, error_message):
        """Handle download errors"""
        self.status_text.append("✗ Error: " + error_message)
        
        # Show detailed error with suggestions
        detailed_msg = f"{error_message}\n\nTroubleshooting suggestions:\n"
        detailed_msg += "• Check your internet connection\n"
        detailed_msg += "• Verify the YouTube URL is correct\n"
        detailed_msg += "• Try enabling 'Use yt-dlp' option\n"
        detailed_msg += "• Some videos may be region-restricted or private"
        
        QMessageBox.critical(self, "Download Error", detailed_msg)
        self.reset_ui()
        
    def reset_ui(self):
        """Reset UI elements"""
        self.download_button.setEnabled(True)
        self.url_input.setEnabled(True)
        self.path_input.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.quality_combo.setEnabled(True)
        self.use_ytdlp_check.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("YouTube Downloader - Enhanced")
    app.setApplicationVersion("2.0")
    
    # Create and show main window
    window = YouTubeDownloader()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()