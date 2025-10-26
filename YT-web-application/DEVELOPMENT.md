# YouTube Downloader - Development Guide

This guide provides detailed information for developers who want to contribute to or extend the YouTube Downloader application.

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Technology Stack](#technology-stack)
3. [Code Structure](#code-structure)
4. [Development Setup](#development-setup)
5. [API Documentation](#api-documentation)
6. [Frontend Architecture](#frontend-architecture)
7. [Backend Architecture](#backend-architecture)
8. [Testing](#testing)
9. [Deployment](#deployment)
10. [Best Practices](#best-practices)

## 🏗️ Architecture Overview

The application follows a modern three-tier architecture:

```
┌─────────────────────────────────────────────┐
│           Frontend (Browser)                │
│   HTML5 + CSS3 + Vanilla JavaScript        │
└─────────────────┬───────────────────────────┘
                  │ REST API
                  │ (JSON over HTTP)
┌─────────────────▼───────────────────────────┐
│           Backend (Flask)                   │
│   - Routes (API endpoints)                  │
│   - Business Logic                          │
│   - Input Validation                        │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│        Service Layer (yt-dlp)               │
│   - Video Information Extraction            │
│   - Download Management                     │
│   - Format Conversion (FFmpeg)              │
└─────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0**: Lightweight WSGI web application framework
- **yt-dlp**: YouTube download library (fork of youtube-dl)
- **python-dotenv**: Environment variable management

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **Vanilla JavaScript**: No framework dependencies for simplicity

### Development Tools
- **pytest**: Testing framework
- **black**: Code formatter
- **flake8**: Linting tool

## 📁 Code Structure

```
app/
├── __init__.py          # Application factory pattern
├── config.py            # Configuration management
├── downloader.py        # Core download service
├── routes.py            # Flask route handlers
├── utils.py             # Utility functions
├── static/
│   ├── css/
│   │   └── styles.css   # All styling
│   └── js/
│       └── main.js      # All frontend logic
└── templates/
    ├── index.html       # Main application page
    └── about.html       # About page
```

## 🚀 Development Setup

### 1. Initial Setup

```bash
# Run the automated setup script
bash setup.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# Create .env file
cp .env.example .env
```

### 2. Development Mode

Set in `.env`:
```
FLASK_ENV=development
FLASK_DEBUG=1
```

### 3. Running the Application

```bash
# Option 1: Use the start script
bash start.sh

# Option 2: Run directly
source venv/bin/activate
python run.py
```

## 📡 API Documentation

### GET /
Returns the main application page.

### GET /about
Returns the about page.

### POST /api/video-info

Get video information without downloading.

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=..."
}
```

**Response:**
```json
{
  "success": true,
  "info": {
    "title": "Video Title",
    "duration": 180,
    "thumbnail": "https://...",
    "uploader": "Channel Name",
    "view_count": 1000000,
    "upload_date": "20250101",
    "description": "..."
  }
}
```

### POST /api/download

Initiate a video or audio download.

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=...",
  "type": "video",
  "quality": "720",
  "filename": "my_video"
}
```

**Response:**
```json
{
  "success": true,
  "filename": "my_video.mp4",
  "path": "/path/to/file",
  "title": "Video Title"
}
```

### GET /api/progress

Get current download progress.

**Response:**
```json
{
  "status": "downloading",
  "percentage": 45.5,
  "speed": "2.5 MB/s",
  "eta": "30s",
  "downloaded": "50.2 MB",
  "total": "110.5 MB",
  "filename": "video.mp4"
}
```

### GET /api/download-file/<filename>

Download a completed file from the server.

## 🎨 Frontend Architecture

### Design Principles

1. **Mobile-First**: Responsive design starting from mobile
2. **Progressive Enhancement**: Works without JavaScript (for basic functionality)
3. **Semantic HTML**: Proper use of HTML5 elements
4. **CSS Variables**: Consistent theming with custom properties
5. **No Dependencies**: Pure vanilla JavaScript for simplicity

### Key Components

#### Form Handler
- Validates user input
- Manages form state
- Handles format switching (video/audio)

#### Progress Tracker
- Polls backend every second
- Updates progress bar and statistics
- Handles completion and errors

#### Video Info Display
- Fetches and displays video metadata
- Shows thumbnail and details
- Helps user verify correct video

### Styling System

The application uses a cohesive dark theme with:
- CSS custom properties for theming
- BEM-inspired class naming
- Mobile-first responsive breakpoints
- Smooth transitions and animations

## 🔧 Backend Architecture

### Application Factory Pattern

The application uses Flask's application factory pattern for better testability and configuration management:

```python
from app import create_app

app = create_app()
```

### Service Layer

The `YouTubeDownloader` class encapsulates all download logic:

```python
class YouTubeDownloader:
    def __init__(self, download_folder: str)
    def get_video_info(self, url: str) -> Dict
    def download_video(self, url: str, quality: str) -> Dict
    def download_audio(self, url: str, quality: str) -> Dict
    def get_progress(self) -> Dict
```

### Progress Tracking

Progress is tracked through a shared `DownloadProgress` object that gets updated by yt-dlp's progress hooks:

```python
def _progress_hook(self, data: Dict) -> None:
    self.progress.update(data)
```

Frontend polls `/api/progress` endpoint to get real-time updates.

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=app tests/

# Run specific test
python -m pytest tests/test_downloader.py::TestYouTubeDownloader::test_initialization
```

### Writing Tests

Follow these guidelines:

1. **Use descriptive test names**: `test_download_video_with_valid_url`
2. **Test one thing**: Each test should verify one behavior
3. **Use fixtures**: Set up common test data with pytest fixtures
4. **Mock external calls**: Don't make actual YouTube API calls in tests
5. **Test edge cases**: Invalid inputs, network errors, etc.

Example test:

```python
def test_sanitize_filename():
    """Test filename sanitization removes invalid characters."""
    result = sanitize_filename('file<>:"/\\|?*.mp4')
    assert result == 'file.mp4'
```

## 🚀 Deployment

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure proper logging
- [ ] Set up HTTPS
- [ ] Implement rate limiting
- [ ] Configure firewall rules
- [ ] Set up monitoring
- [ ] Regular backups of download folder
- [ ] Update dependencies regularly

### Using Gunicorn (Recommended)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## 📝 Best Practices

### Python Code

1. **Type Hints**: Use type hints for all function signatures
   ```python
   def download_video(url: str, quality: str = 'best') -> Dict:
   ```

2. **Docstrings**: Document all functions and classes
   ```python
   def get_video_info(self, url: str) -> Dict:
       """
       Retrieve video information without downloading.
       
       Args:
           url: YouTube video URL.
           
       Returns:
           Dictionary containing video metadata.
       """
   ```

3. **Error Handling**: Always handle exceptions gracefully
   ```python
   try:
       result = download_video(url)
   except Exception as e:
       logger.error(f"Download failed: {str(e)}")
       raise
   ```

4. **Logging**: Use logging instead of print
   ```python
   logger.info(f"Starting download for {url}")
   ```

5. **Constants**: Define constants at module level
   ```python
   MAX_FILENAME_LENGTH = 200
   PROGRESS_POLL_INTERVAL = 1000  # milliseconds
   ```

### Frontend Code

1. **Error Handling**: Always handle fetch errors
   ```javascript
   try {
       const response = await fetch('/api/download');
       const data = await response.json();
   } catch (error) {
       showMessage('Network error: ' + error.message, 'error');
   }
   ```

2. **DOM Manipulation**: Cache DOM queries
   ```javascript
   const downloadBtn = document.getElementById('downloadBtn');
   ```

3. **Event Listeners**: Remove listeners when not needed
   ```javascript
   element.removeEventListener('click', handler);
   ```

### Git Workflow

1. **Branching**: Create feature branches
   ```bash
   git checkout -b feature/add-playlist-support
   ```

2. **Commits**: Write clear commit messages
   ```
   feat: Add playlist download support
   
   - Add playlist parsing logic
   - Update UI for playlist selection
   - Add tests for playlist functionality
   ```

3. **Pull Requests**: Include description and testing notes

## 🔄 Common Development Tasks

### Adding a New API Endpoint

1. Define route in `app/routes.py`:
   ```python
   @main_bp.route('/api/new-endpoint', methods=['POST'])
   def new_endpoint():
       # Implementation
       return jsonify(result), 200
   ```

2. Add frontend handler in `app/static/js/main.js`:
   ```javascript
   async function callNewEndpoint() {
       const response = await fetch('/api/new-endpoint', {
           method: 'POST',
           headers: {'Content-Type': 'application/json'},
           body: JSON.stringify(data)
       });
   }
   ```

3. Add tests in `tests/test_routes.py`

### Adding a New Quality Option

1. Update `app/config.py`:
   ```python
   VIDEO_QUALITIES = [
       # ... existing qualities
       {'value': '4k', 'label': '4K (2160p)'},
   ]
   ```

2. Update validation in `app/utils.py`

3. No frontend changes needed (uses dynamic rendering)

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [JavaScript Best Practices](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

---

**Happy Coding! 🎉**
