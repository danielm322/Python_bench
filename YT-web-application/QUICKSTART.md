# YouTube Downloader - Quick Start Guide

Get up and running in 5 minutes! 🚀

## Prerequisites

- Python 3.9+ installed
- FFmpeg installed (for video/audio processing)

## Installation Steps

### 1. Navigate to Project Directory

```bash
cd YT-web-application
```

### 2. Run Setup Script (Recommended)

```bash
bash setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Generate secure configuration
- Set up required directories

### 3. Start the Application

```bash
bash start.sh
```

Or manually:

```bash
source venv/bin/activate
python run.py
```

### 4. Open Your Browser

Navigate to: **http://localhost:5000**

## Using the Application

### Download a Video

1. Paste YouTube URL
2. Select "Video" format
3. Choose quality (e.g., 720p)
4. Click "Download"

### Download Audio (MP3)

1. Paste YouTube URL
2. Select "Audio (MP3)" format
3. Choose quality (e.g., 192 kbps)
4. Click "Download"

### Get Video Information

Click "Get Video Info" to preview:
- Title
- Thumbnail
- Duration
- View count
- Uploader

## Troubleshooting

### FFmpeg Not Found

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### Port Already in Use

Edit `run.py` and change:
```python
app.run(port=5001)  # Change from 5000 to 5001
```

### Permission Denied

```bash
chmod +x setup.sh start.sh
```

### Module Not Found

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [DEVELOPMENT.md](DEVELOPMENT.md) for developer guide
- Explore the code in the `app/` directory
- Run tests: `python -m pytest tests/`

## Need Help?

- Check the logs in `logs/yt_downloader.log`
- Review error messages in the browser console
- Open an issue in the repository

---

**Enjoy downloading! 🎬**
