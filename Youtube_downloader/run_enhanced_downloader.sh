#!/bin/bash
# YouTube Downloader Enhanced Launcher Script

echo "YouTube Video Downloader - Enhanced Version"
echo "==========================================="

# Activate virtual environment and run the enhanced application
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

echo "Starting YouTube Downloader with yt-dlp fallback support..."
source .venv/bin/activate
python youtube_downloader_fixed.py