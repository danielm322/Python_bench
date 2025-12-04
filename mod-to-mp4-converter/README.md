# 🎬 MOD to MP4 Converter

A modern, premium web application for converting .mod video files (MPEG-2 format from camcorders) to .mp4 format with customizable quality settings.

## ✨ Features

- **Premium UI Design**: Dark theme with glassmorphism effects and smooth animations
- **Drag & Drop Upload**: Intuitive file upload with drag-and-drop support
- **Quality Presets**: Choose from High (1080p), Medium (720p), or Low (480p) quality
- **Real-time Progress**: Visual feedback during conversion process
- **Automatic Cleanup**: Temporary files are automatically removed
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## 🚀 Prerequisites

Before running this application, ensure you have the following installed:

1. **Python 3.9 or higher**
   ```bash
   python3 --version
   ```

2. **FFmpeg** (required for video conversion)
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```
   
   **macOS (using Homebrew):**
   ```bash
   brew install ffmpeg
   ```
   
   **Verify installation:**
   ```bash
   ffmpeg -version
   ```

## 📦 Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /home/monlef/VSProjects/Python_bench/mod-to-mp4-converter
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   
   **Linux/macOS:**
   ```bash
   source venv/bin/activate
   ```
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Convert your videos:**
   - Drag and drop a .mod file or click to browse
   - Select your desired quality preset
   - Click "Convert to MP4"
   - Download the converted file when ready

## ⚙️ Configuration

### File Size Limit

The default maximum upload size is 500MB. To change this, edit `app.py`:

```python
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # Change to desired size in bytes
```

### Quality Presets

Quality presets are defined in `converter.py`. You can modify or add new presets:

```python
QUALITY_PRESETS = {
    'high': {
        'resolution': '1920x1080',
        'video_bitrate': '8M',
        'audio_bitrate': '192k',
        'description': 'High Quality (1080p, 8 Mbps)'
    },
    # Add more presets here
}
```

### Cleanup Schedule

Files are automatically cleaned up after 24 hours. To change this, modify the `cleanup_old_files()` call in `app.py`:

```python
cleanup_old_files(max_age_hours=24)  # Change to desired hours
```

## 📁 Project Structure

```
mod-to-mp4-converter/
├── app.py                  # Flask application
├── converter.py            # Video conversion logic
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── static/
│   ├── css/
│   │   └── style.css      # Premium design system
│   └── js/
│       └── app.js         # Frontend logic
├── templates/
│   └── index.html         # Main HTML template
├── uploads/               # Temporary upload storage (auto-created)
└── outputs/               # Converted files storage (auto-created)
```

## 🔧 Troubleshooting

### FFmpeg Not Found

If you see an error about FFmpeg not being installed:

1. Install FFmpeg using the instructions in the Prerequisites section
2. Verify installation: `ffmpeg -version`
3. Restart the application

### File Upload Fails

- Ensure the file is a valid .mod file
- Check that the file size is under 500MB (or your configured limit)
- Verify that the `uploads/` directory exists and is writable

### Conversion Fails

- Check FFmpeg installation: `ffmpeg -version`
- Verify the .mod file is not corrupted
- Check server logs for detailed error messages

### Port Already in Use

If port 5000 is already in use, you can change it in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port number
```

## 🛡️ Security Considerations

**For Production Deployment:**

1. **Disable Debug Mode**: Set `debug=False` in `app.run()`
2. **Use a Production Server**: Deploy with Gunicorn or uWSGI instead of Flask's development server
3. **Add Authentication**: Implement user authentication if needed
4. **Set Up HTTPS**: Use SSL/TLS certificates for secure connections
5. **Configure Firewall**: Restrict access to necessary ports only
6. **Implement Rate Limiting**: Prevent abuse with rate limiting middleware
7. **Validate File Content**: Add additional file validation beyond extension checking

## 📝 API Endpoints

- `GET /` - Main application page
- `POST /upload` - Upload and convert video file
- `GET /download/<filename>` - Download converted file
- `POST /cleanup` - Manually trigger file cleanup
- `GET /health` - Check server and FFmpeg status

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is open source and available for personal and commercial use.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Video conversion powered by [FFmpeg](https://ffmpeg.org/)
- Design inspired by modern web aesthetics

---

**Enjoy converting your videos! 🎥✨**
