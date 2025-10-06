#!/usr/bin/env python3
"""
YouTube Video Downloader GUI
A simple PyQt6 application to download YouTube videos using pytube
"""

import sys
import os
import threading
import re
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QLabel, QLineEdit, QPushButton, QFileDialog, 
                            QProgressBar, QMessageBox, QTextEdit, QFrame, QComboBox)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont, QIcon
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError, PytubeError
import urllib.request
import ssl


class DownloadThread(QThread):
    """Thread for downloading YouTube videos to prevent GUI freezing"""
    
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    status_update = pyqtSignal(str)
    
    def __init__(self, url, save_path, quality_choice="highest"):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.quality_choice = quality_choice
        
    def progress_callback(self, stream, chunk, bytes_remaining):
        """Callback function to track download progress"""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = int((bytes_downloaded / total_size) * 100)
        self.progress.emit(percentage)
        
    def get_video_info(self, yt):
        """Get video information and available streams"""
        try:
            # Try to get video info
            title = yt.title
            length = yt.length
            views = yt.views
            
            self.status_update.emit(f"Video: {title}")
            self.status_update.emit(f"Duration: {length//60}:{length%60:02d}")
            self.status_update.emit(f"Views: {views:,}")
            
            return True
        except Exception as e:
            self.status_update.emit(f"Warning: Could not get video info: {str(e)}")
            return True  # Continue anyway
            
    def fix_ssl_context(self):
        """Fix SSL context for pytube compatibility"""
        try:
            # Create an SSL context that doesn't verify certificates
            ssl._create_default_https_context = ssl._create_unverified_context
        except:
            pass
            
    def sanitize_url(self, url):
        """Clean and validate YouTube URL"""
        # Remove any extra parameters that might cause issues
        if 'youtube.com' in url or 'youtu.be' in url:
            # Extract video ID
            video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
            if video_id_match:
                video_id = video_id_match.group(1)
                return f"https://www.youtube.com/watch?v={video_id}"
        return url
        
    def run(self):
        """Main download process with multiple fallback strategies"""
        try:
            # Fix SSL issues
            self.fix_ssl_context()
            
            # Sanitize URL
            clean_url = self.sanitize_url(self.url)
            self.status_update.emit(f"Processing URL: {clean_url}")
            
            # Strategy 1: Try with default settings
            self.status_update.emit("Attempting connection to YouTube...")
            
            try:
                yt = YouTube(clean_url, on_progress_callback=self.progress_callback)
                self.get_video_info(yt)
                
                # Get available streams
                self.status_update.emit("Fetching available video streams...")
                
                # Try different stream selection strategies
                stream = None
                
                if self.quality_choice == "highest":
                    # Try progressive streams first (video + audio)
                    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                    
                    if not stream:
                        # Try adaptive streams (video only, highest quality)
                        stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
                        
                    if not stream:
                        # Fallback to any available stream
                        stream = yt.streams.filter(file_extension='mp4').first()
                        
                elif self.quality_choice == "audio_only":
                    stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
                    
                else:  # medium quality
                    stream = yt.streams.filter(progressive=True, file_extension='mp4', res='720p').first()
                    if not stream:
                        stream = yt.streams.filter(progressive=True, file_extension='mp4', res='480p').first()
                    if not stream:
                        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                
                if stream is None:
                    available_streams = yt.streams.all()
                    if available_streams:
                        stream = available_streams[0]  # Use first available stream
                        self.status_update.emit(f"Using fallback stream: {stream.mime_type} - {getattr(stream, 'resolution', 'audio only')}")
                    else:
                        self.error.emit("No downloadable streams found for this video.")
                        return
                else:
                    self.status_update.emit(f"Selected stream: {stream.mime_type} - {getattr(stream, 'resolution', 'audio only')}")
                
                # Download the video
                self.status_update.emit("Starting download...")
                filename = stream.download(output_path=self.save_path)
                self.finished.emit(f"Video downloaded successfully!\nSaved as: {filename}")
                
            except Exception as e:
                # Strategy 2: Try with different approach
                self.status_update.emit(f"First attempt failed: {str(e)}")
                self.status_update.emit("Trying alternative method...")
                
                try:
                    # Try creating YouTube object without progress callback
                    yt = YouTube(clean_url)
                    
                    # Get the first available stream
                    streams = yt.streams.all()
                    if not streams:
                        self.error.emit("No streams available for this video.")
                        return
                        
                    # Select a good quality stream
                    progressive_streams = [s for s in streams if hasattr(s, 'resolution') and s.resolution]
                    if progressive_streams:
                        # Sort by resolution and pick the best one
                        progressive_streams.sort(key=lambda x: int(x.resolution.replace('p', '')), reverse=True)
                        stream = progressive_streams[0]
                    else:
                        stream = streams[0]
                    
                    self.status_update.emit(f"Using stream: {stream}")
                    
                    # Download without progress tracking
                    filename = stream.download(output_path=self.save_path)
                    self.finished.emit(f"Video downloaded successfully!\nSaved as: {filename}")
                    
                except Exception as e2:
                    self.error.emit(f"Download failed with multiple attempts:\n1. {str(e)}\n2. {str(e2)}\n\nTry using a different video URL or check your internet connection.")
                
        except VideoUnavailable:
            self.error.emit("Video is unavailable, private, or has been removed.")
        except RegexMatchError:
            self.error.emit("Invalid YouTube URL. Please check the URL format.")
        except PytubeError as e:
            self.error.emit(f"Pytube error: {str(e)}\nTry updating pytube or using a different video.")
        except Exception as e:
            self.error.emit(f"Unexpected error: {str(e)}")


class YouTubeDownloader(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.download_thread = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("YouTube Video Downloader")
        self.setGeometry(100, 100, 600, 400)
        
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
        url_frame = QFrame()
        url_layout = QVBoxLayout(url_frame)
        
        url_label = QLabel("YouTube Video URL:")
        url_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        url_layout.addWidget(url_label)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste YouTube video URL here...")
        self.url_input.setMinimumHeight(35)
        url_layout.addWidget(self.url_input)
        
        main_layout.addWidget(url_frame)
        
        # Save path section
        path_frame = QFrame()
        path_layout = QVBoxLayout(path_frame)
        
        path_label = QLabel("Download Location:")
        path_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        path_layout.addWidget(path_label)
        
        path_input_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select download folder...")
        self.path_input.setMinimumHeight(35)
        self.path_input.setText(str(Path.home() / "Downloads"))  # Default to Downloads folder
        
        self.browse_button = QPushButton("Browse")
        self.browse_button.setMinimumHeight(35)
        self.browse_button.setMinimumWidth(80)
        self.browse_button.clicked.connect(self.browse_folder)
        
        path_input_layout.addWidget(self.path_input)
        path_input_layout.addWidget(self.browse_button)
        path_layout.addLayout(path_input_layout)
        
        main_layout.addWidget(path_frame)
        
        # Quality selection section
        quality_frame = QFrame()
        quality_layout = QVBoxLayout(quality_frame)
        
        quality_label = QLabel("Download Quality:")
        quality_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        quality_layout.addWidget(quality_label)
        
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([
            "Highest Quality (Recommended)",
            "Medium Quality (720p/480p)",
            "Audio Only"
        ])
        self.quality_combo.setMinimumHeight(35)
        quality_layout.addWidget(self.quality_combo)
        
        main_layout.addWidget(quality_frame)
        
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
        self.status_text.setMaximumHeight(100)
        self.status_text.setReadOnly(True)
        self.status_text.setPlaceholderText("Status messages will appear here...")
        main_layout.addWidget(self.status_text)
        
        # Add some stretch to center content
        main_layout.addStretch()
        
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
        """Validate user inputs before download"""
        url = self.url_input.text().strip()
        save_path = self.path_input.text().strip()
        
        if not url:
            QMessageBox.warning(self, "Invalid Input", "Please enter a YouTube URL.")
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
            
        # Disable UI elements during download
        self.download_button.setEnabled(False)
        self.url_input.setEnabled(False)
        self.path_input.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.quality_combo.setEnabled(False)
        
        # Show progress bar and reset it
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Update status
        self.status_text.clear()
        self.status_text.append("Initializing download...")
        
        # Get quality choice
        quality_map = {
            0: "highest",
            1: "medium", 
            2: "audio_only"
        }
        quality_choice = quality_map.get(self.quality_combo.currentIndex(), "highest")
        
        # Create and start download thread
        url = self.url_input.text().strip()
        save_path = self.path_input.text().strip()
        
        self.download_thread = DownloadThread(url, save_path, quality_choice)
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
        # Auto-scroll to bottom
        cursor = self.status_text.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.status_text.setTextCursor(cursor)
        
    def download_finished(self, message):
        """Handle successful download completion"""
        self.progress_bar.setValue(100)
        self.status_text.append(message)
        
        # Show success message
        QMessageBox.information(self, "Download Complete", message)
        
        # Reset UI
        self.reset_ui()
        
    def download_error(self, error_message):
        """Handle download errors"""
        self.status_text.append(f"Error: {error_message}")
        
        # Show error message
        QMessageBox.critical(self, "Download Error", error_message)
        
        # Reset UI
        self.reset_ui()
        
    def reset_ui(self):
        """Reset UI elements after download completion or error"""
        self.download_button.setEnabled(True)
        self.url_input.setEnabled(True)
        self.path_input.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.quality_combo.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        
    def closeEvent(self, event):
        """Handle application closing"""
        if self.download_thread and self.download_thread.isRunning():
            reply = QMessageBox.question(
                self, 
                "Download in Progress", 
                "A download is currently in progress. Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.download_thread.terminate()
                self.download_thread.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("YouTube Downloader")
    app.setApplicationVersion("1.0")
    
    # Create and show main window
    window = YouTubeDownloader()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()