# YouTube Downloader Web Application

A modern, professional web application for downloading YouTube videos and audio content. Built with Flask, yt-dlp, and vanilla JavaScript.

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/flask-3.0.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ Features

- **Video Downloads**: Download YouTube videos in multiple quality settings (144p to 1080p, or best available)
- **Audio Extraction**: Extract and convert audio to MP3 format with customizable bitrates (64-320 kbps)
- **Real-time Progress**: Live progress tracking with download speed, ETA, and completion percentage
- **Video Information**: Preview video details (title, thumbnail, duration, views) before downloading
- **Custom Filenames**: Optionally specify custom filenames for downloads
- **Modern UI**: Responsive, professional interface with dark theme
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Modular Architecture**: Clean, maintainable code following Python best practices

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- ffmpeg (required by yt-dlp for video/audio processing)

### Installing FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

## 🚀 Installation

### 1. Clone or Download the Project

```bash
cd YT-web-application
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file and update the values:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secure-secret-key-here
DOWNLOAD_FOLDER=downloads
MAX_CONTENT_LENGTH=524288000
```

## 🎮 Usage

### Starting the Application

```bash
python run.py
```

The application will start on `http://localhost:5000`

### Using the Application

1. **Open your browser** and navigate to `http://localhost:5000`

2. **Enter YouTube URL** in the input field

3. **Select format**:
   - Video: Choose video quality (144p - 1080p)
   - Audio: Choose audio bitrate (64 - 320 kbps)

4. **(Optional) Get Video Info**: Click "Get Video Info" to preview video details

5. **(Optional) Custom Filename**: Enter a custom filename (without extension)

6. **Click Download**: The download will start and you can track progress in real-time

7. **File Download**: Once complete, the file will automatically download to your computer

### API Endpoints

The application provides the following REST API endpoints:

- `GET /` - Main application page
- `GET /about` - About page
- `POST /api/video-info` - Get video information
- `POST /api/download` - Initiate download
- `GET /api/progress` - Get download progress
- `GET /api/download-file/<filename>` - Download completed file

## 📁 Project Structure

```
YT-web-application/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration settings
│   ├── downloader.py        # YouTube download service
│   ├── routes.py            # Flask routes/endpoints
│   ├── utils.py             # Utility functions
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css   # Application styles
│   │   └── js/
│   │       └── main.js      # Frontend JavaScript
│   └── templates/
│       ├── index.html       # Main page template
│       └── about.html       # About page template
├── downloads/               # Download directory
├── tests/
│   ├── __init__.py
│   ├── test_downloader.py   # Downloader tests
│   └── test_utils.py        # Utility tests
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md                # This file
```

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_downloader.py

# Run with coverage
python -m pytest --cov=app tests/
```

## 🔧 Development

### Setting Up Development Environment

1. Follow installation steps above
2. Set `FLASK_ENV=development` in `.env`
3. Install development dependencies:
   ```bash
   pip install pytest pytest-cov black flake8
   ```

### Code Formatting

```bash
# Format code with Black
black app/ tests/

# Check code style with Flake8
flake8 app/ tests/
```

### Project Guidelines

- Follow **PEP 8** style guide
- Use **type hints** for function signatures
- Write **docstrings** for all functions and classes
- Add **unit tests** for new features
- Use **logging** instead of print statements
- Handle exceptions gracefully
- Keep functions small and focused

## 🐛 Troubleshooting

### Common Issues

**1. ModuleNotFoundError: No module named 'flask'**
- Solution: Ensure virtual environment is activated and dependencies are installed

**2. FFmpeg not found**
- Solution: Install FFmpeg and ensure it's in your system PATH

**3. Download fails with "ERROR: unable to download video data"**
- Solution: Check that the YouTube URL is valid and accessible

**4. Port 5000 already in use**
- Solution: Change the port in `run.py` or kill the process using port 5000

**5. Permission denied when downloading**
- Solution: Check that the `downloads` folder has proper write permissions

## 🔒 Security Considerations

- Never commit `.env` file to version control
- Change the default `SECRET_KEY` in production
- Implement rate limiting for production use
- Validate and sanitize all user inputs
- Keep dependencies updated regularly
- Use HTTPS in production

## 📝 License

This project is provided for educational purposes. Users are responsible for ensuring their use complies with YouTube's Terms of Service and all applicable copyright laws.

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Support

For issues, questions, or suggestions, please open an issue in the project repository.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Powerful YouTube download library
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [FFmpeg](https://ffmpeg.org/) - Multimedia processing

## 📊 Version History

- **1.0.0** (October 2025)
  - Initial release
  - Video and audio download functionality
  - Real-time progress tracking
  - Modern responsive UI
  - Comprehensive error handling

---

**Made with ❤️ by the development team**
