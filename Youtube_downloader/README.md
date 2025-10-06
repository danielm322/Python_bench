# YouTube Video Downloader

A robust GUI application for downloading YouTube videos using PyQt6 with multiple download strategies (pytube + yt-dlp fallback).

## Features

- Clean and intuitive GUI interface
- **Dual download strategy**: pytube primary, yt-dlp fallback
- URL validation and error handling
- Real-time progress tracking
- Customizable download location and quality
- Highest quality video download
- Audio-only download option
- Comprehensive error handling and troubleshooting

## Current Status

Due to recent YouTube API changes, **pytube may encounter HTTP 400 errors**. This application automatically falls back to **yt-dlp** which works reliably. The enhanced version (`youtube_downloader_fixed.py`) is recommended.

## Requirements

- Python 3.7+
- PyQt6
- pytube (with yt-dlp fallback)
- yt-dlp
- FFmpeg (for MP3 audio conversion - install with `sudo apt install ffmpeg`)

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Recommended: Enhanced version with fallback
```bash
python youtube_downloader_fixed.py
```

### Original version (may have issues with some videos)
```bash
python youtube_downloader.py
```

### Using the launcher script
```bash
./run_downloader.sh
```

### Test functionality
```bash
python test_downloader.py
```

## How to Use

1. **Enter YouTube URL**: Paste the YouTube video URL in the text field
2. **Select Download Location**: Choose where you want to save the video (defaults to Downloads folder)
3. **Choose Quality**: Select video quality (Highest, Medium, or Audio Only in MP3 format)
4. **Enable Fallback**: Keep "Use yt-dlp" checked for maximum compatibility
5. **Click Download**: Press the "Download Video" button to start the process
6. **Monitor Progress**: Watch the progress bar and status messages
7. **Success**: A success message will appear when the download is complete

## Features Explanation

- **URL Input**: Accepts standard YouTube URLs (youtube.com or youtu.be)
- **Path Selection**: Browse button opens a folder selection dialog
- **Quality Selection**: Choose between highest quality video, medium quality (720p/480p) video, or audio only (MP3 format)
- **Fallback Option**: Automatically uses yt-dlp if pytube fails
- **Progress Tracking**: Real-time download progress with detailed status messages
- **Error Handling**: Comprehensive error messages with troubleshooting suggestions

## Troubleshooting

### Common Issues

- **HTTP Error 400**: This is a known issue with pytube. Enable "Use yt-dlp" option
- **Invalid URL**: Make sure you're using a valid YouTube URL
- **Video Unavailable**: Some videos may be private, region-restricted, or removed
- **Permission Error**: Ensure you have write permissions to the selected folder
- **Network Issues**: Check your internet connection

### Solutions

1. **Always enable "Use yt-dlp" option** for maximum compatibility
2. **Test with the test script**: Run `python test_downloader.py` to verify functionality
3. **Check dependencies**: Ensure all required packages are installed
4. **Try different URLs**: Some videos may have restrictions

## Technical Details

- **Primary**: pytube library for YouTube video extraction
- **Fallback**: yt-dlp for reliable downloads when pytube fails
- **GUI**: PyQt6 for the graphical user interface
- **Threading**: Prevents GUI freezing during downloads
- **Quality**: Downloads highest available resolution by default
- **Progress**: Real-time progress tracking with detailed status updates

## File Structure

- `youtube_downloader.py` - Original version (may have HTTP 400 issues)
- `youtube_downloader_fixed.py` - **Enhanced version with yt-dlp fallback (RECOMMENDED)**
- `test_downloader.py` - Test suite to verify functionality
- `run_downloader.sh` - Launcher script
- `requirements.txt` - Python dependencies

## License

This project is for educational purposes. Please respect YouTube's Terms of Service and copyright laws when downloading videos.