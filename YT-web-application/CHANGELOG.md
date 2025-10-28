# Changelog

All notable changes to the YouTube Downloader project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.4] - 2025-10-28

### Added

- **Linux Desktop Shortcut**: Created `.desktop` file for easy application launching
  - Installs to application menu (Network/Audio & Video categories)
  - Can be placed on desktop for quick access
  - Automated installation script (`install-desktop-shortcut.sh`)
  - Comprehensive documentation in `DESKTOP_SHORTCUT.md`
  - Follows freedesktop.org Desktop Entry Specification
  - Includes proper icon, categories, and keywords for searchability

### Changed

- **UI Theme Overhaul**: Converted from dark theme to modern professional light theme
  - Updated color scheme: Light blue primary (#2563eb), clean white surfaces (#ffffff), subtle gray backgrounds (#f8fafc)
  - Enhanced readability with improved contrast ratios
  - Modern gradient accents on navigation, buttons, and progress bars
  - Professional shadow system for depth and visual hierarchy
  - Improved hover states and interactive feedback
  - Added shimmer animation to progress bars
  - Better visual consistency across all components
  - Responsive design maintained with enhanced mobile/tablet experience
  - Footer kept with subtle dark gradient for visual grounding

### Improved

- Enhanced button styling with gradient effects and better shadows
- Better form input feedback with focus rings
- Improved card hover effects with smooth transitions
- More professional message boxes (success/error states)
- Enhanced feature cards with modern styling

### Documentation

- Added `DESKTOP_SHORTCUT.md` with installation guide and troubleshooting
- Added `THEME_UPDATE_v1.0.4.md` with detailed theme conversion documentation
- Updated `README.md` with desktop shortcut installation instructions

## [1.0.3] - 2025-10-26

### Added

- **Auto Browser Launch**: `start.sh` now automatically opens the application in the default web browser
  - Supports Linux (xdg-open, gnome-open), macOS (open), and Windows Git Bash (start)
  - Falls back to manual URL display if no browser command is detected
- **Server Readiness Check**: Script waits for Flask server to be fully ready before opening browser
  - Uses curl to test server availability
  - 15-second timeout with retry logic
- **Graceful Shutdown**: Proper signal handling for clean server shutdown
  - Captures SIGINT (Ctrl+C), SIGTERM, and EXIT signals
  - Kills server process and cleans up orphaned processes
  - Displays shutdown confirmation message
- **Process Management**: Tracks server PID and displays runtime information
  - Shows server URL and Process ID when running
  - Background execution with proper wait handling

### Changed

- Enhanced `start.sh` script with better user experience
- Server now runs in background to allow browser launching
- Improved error messages and status indicators

### Documentation

- Added `START_SCRIPT_DOCS.md` with comprehensive documentation
  - Script flow diagrams
  - Troubleshooting guide
  - Technical details on signal handling
  - Browser detection logic

## [1.0.2] - 2025-10-26

### Fixed

- **Critical Bug:** Fixed `HTTP Error 403: Forbidden` that prevented all YouTube downloads
  - Updated yt-dlp from 2024.10.22 to 2025.10.22 (latest version)
  - Added proper HTTP headers to mimic real browser requests
  - Configured YouTube player clients ('android', 'web') for better compatibility
  - Added `noplaylist` option to download only single videos, not entire playlists
  - Skips problematic HLS and DASH formats that cause empty downloads

### Added

- `_get_base_ydl_opts()` method for centralized yt-dlp configuration
- Comprehensive HTTP headers (User-Agent, Accept, Accept-Language, Sec-Fetch-Mode)
- YouTube extractor arguments with multiple player client fallbacks
- Playlist URL handling to extract single videos

### Changed

- Centralized yt-dlp options across all download methods (info, video, audio)
- Updated requirements.txt to use `yt-dlp>=2025.10.22`
- Improved error handling for YouTube API changes

### Documentation

- Added `BUGFIX_403_FORBIDDEN.md` with comprehensive explanation and solutions
- Added `test_youtube_access.py` for testing YouTube connectivity

## [1.0.1] - 2025-10-26

### Fixed

- **Critical Bug:** Fixed `'NoneType' object has no attribute 'strip'` error that prevented downloads
  - Issue occurred when custom filename field was left empty (frontend sends `null`)
  - Fixed by using `(data.get('key') or '').strip()` pattern instead of `data.get('key', '').strip()`
  - Applied fix to both `/api/video-info` and `/api/download` endpoints
  - All download functionality now works correctly with or without custom filenames

### Changed

- Improved null value handling in API routes for better robustness
- Added defensive programming pattern for handling optional string parameters

### Documentation

- Added `BUGFIX_NONETYPE.md` documenting the issue and solution
- Added `test_fix.py` to verify the fix works correctly

## [1.0.0] - 2025-10-26

### Added

#### Core Features
- YouTube video download functionality with multiple quality options (144p - 1080p)
- Audio extraction and MP3 conversion with customizable bitrates (64-320 kbps)
- Real-time download progress tracking with speed, ETA, and percentage
- Video information preview (title, thumbnail, duration, views, uploader)
- Custom filename support for downloads
- Automatic file download to user's browser

#### Backend
- Flask application with modular architecture
- Application factory pattern for better testability
- RESTful API with JSON request/response format
- `YouTubeDownloader` service class for download management
- `DownloadProgress` class for progress tracking
- Comprehensive error handling and logging
- Input validation and sanitization utilities
- Type hints throughout codebase
- Detailed docstrings for all functions and classes

#### Frontend
- Modern dark-themed responsive UI
- Real-time progress visualization with progress bar
- Format selection (video/audio)
- Quality selection for both formats
- Video information display with thumbnail
- User-friendly error messages
- About page with project information
- Mobile-friendly responsive design

#### API Endpoints
- `GET /` - Main application page
- `GET /about` - About page
- `POST /api/video-info` - Get video metadata
- `POST /api/download` - Initiate download
- `GET /api/progress` - Get download progress
- `GET /api/download-file/<filename>` - Download completed file

#### Testing
- Unit tests for downloader service
- Unit tests for utility functions
- Test fixtures and setup/teardown
- pytest configuration

#### Documentation
- Comprehensive README.md with installation and usage instructions
- DEVELOPMENT.md developer guide with architecture details
- QUICKSTART.md for quick setup
- PROJECT_SUMMARY.md with project overview
- Inline code documentation with docstrings
- API documentation

#### Scripts & Configuration
- `setup.sh` - Automated setup script for Linux/macOS
- `start.sh` - Quick start script
- `verify_structure.sh` - Project structure verification
- `.env.example` - Environment variables template
- `.gitignore` - Git ignore configuration
- `requirements.txt` - Python dependencies

#### Project Structure
- Clean, modular directory structure
- Separation of concerns (routes, services, utilities)
- Static files organization (CSS, JavaScript)
- Template organization
- Test directory structure

### Technical Details

#### Dependencies
- Flask 3.0.0 - Web framework
- yt-dlp 2024.10.22 - YouTube download library
- python-dotenv 1.0.0 - Environment variable management
- Werkzeug 3.0.1 - WSGI utilities

#### Code Quality
- PEP 8 compliant code style
- Type hints for function signatures
- Comprehensive docstrings
- Logging instead of print statements
- Try-catch exception handling
- Input validation and sanitization

#### Security
- Environment variable configuration
- Secret key management
- Input validation and sanitization
- Path sanitization for filenames
- Error message sanitization

#### Performance
- Progress polling mechanism (1 second interval)
- Efficient file serving
- Streaming download support
- Automatic cleanup

### Architecture

- **Backend**: Flask with Blueprint-based routing
- **Service Layer**: YouTubeDownloader class with yt-dlp integration
- **Progress Tracking**: Hook-based progress updates with polling
- **Frontend**: Vanilla JavaScript with fetch API
- **Styling**: Modern CSS with custom properties and responsive design

### Browser Support

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Opera 76+

---

## Future Enhancements (Planned)

### [1.1.0] - TBD
- [ ] Playlist download support
- [ ] Batch download capability
- [ ] Download queue management

### [1.2.0] - TBD
- [ ] User authentication system
- [ ] Download history tracking
- [ ] User preferences and settings

### [1.3.0] - TBD
- [ ] WebSocket for real-time progress (replacing polling)
- [ ] Background task queue (Celery)
- [ ] Database integration (SQLite/PostgreSQL)

### [2.0.0] - TBD
- [ ] Multiple language support (i18n)
- [ ] Theme customization
- [ ] Advanced video filtering
- [ ] Subtitle download support
- [ ] Video thumbnail generation

---

## Version History

- **1.0.0** (2025-10-26) - Initial release with core functionality

---

[1.0.0]: https://github.com/yourusername/yt-web-application/releases/tag/v1.0.0
