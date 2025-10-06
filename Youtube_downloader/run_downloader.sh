#!/bin/bash
# YouTube Downloader Launcher Script

# Activate virtual environment and run the application
cd "$(dirname "$0")"
source .venv/bin/activate
python youtube_downloader.py