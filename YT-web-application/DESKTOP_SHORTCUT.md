# Desktop Shortcut Installation Guide

## Overview

A `.desktop` file has been created to launch the YouTube Downloader application directly from your Linux desktop environment.

## Installation Options

### Option 1: Local User Installation (Recommended)

Install the shortcut for the current user only:

```bash
# Copy to local applications directory
mkdir -p ~/.local/share/applications
cp youtube-downloader.desktop ~/.local/share/applications/

# Make executable
chmod +x ~/.local/share/applications/youtube-downloader.desktop

# Update desktop database
update-desktop-database ~/.local/share/applications/
```

The application will appear in your application menu under "Network" or "Audio & Video" categories.

### Option 2: Desktop Shortcut

Place the shortcut directly on your desktop:

```bash
# Copy to desktop
cp youtube-downloader.desktop ~/Desktop/

# Make executable
chmod +x ~/Desktop/youtube-downloader.desktop

# Allow launching (if prompted by file manager)
gio set ~/Desktop/youtube-downloader.desktop metadata::trusted true
```

### Option 3: System-Wide Installation (Requires sudo)

Install for all users on the system:

```bash
# Copy to system applications directory
sudo cp youtube-downloader.desktop /usr/share/applications/

# Make executable
sudo chmod +x /usr/share/applications/youtube-downloader.desktop

# Update desktop database
sudo update-desktop-database /usr/share/applications/
```

## Desktop File Details

**File**: `youtube-downloader.desktop`

**Properties**:
- **Name**: YouTube Downloader
- **Type**: Application launcher
- **Terminal**: Opens in terminal (required for Flask server output)
- **Categories**: Network, Audio & Video, Utility
- **Exec Command**: Runs `start.sh` script in the correct directory

## Usage

Once installed, you can:

1. **Launch from Application Menu**: 
   - Search for "YouTube Downloader" in your application launcher
   - Or browse to Network/Audio & Video categories

2. **Launch from Desktop**: 
   - Double-click the desktop icon (if installed to desktop)
   - May need to confirm "Trust and Launch" on first run

3. **What Happens**:
   - Terminal window opens
   - Flask server starts
   - Browser automatically opens to `http://localhost:5000`
   - Server shows startup messages and logs

4. **To Stop**:
   - Press `Ctrl+C` in the terminal window
   - Server shuts down gracefully
   - Terminal window closes

## Customization

You can edit the `.desktop` file to customize:

- **Icon**: Change the `Icon=` path to use a different image
- **Terminal**: Set `Terminal=false` to hide terminal window (not recommended for development)
- **Name**: Change the display name
- **Comment**: Modify the description

## Troubleshooting

### Icon Not Showing
If the icon doesn't display:
```bash
# Use a system icon instead
Icon=video-x-generic
# or
Icon=internet-web-browser
```

### Desktop File Not Executable
```bash
chmod +x youtube-downloader.desktop
gio set youtube-downloader.desktop metadata::trusted true
```

### Permission Denied
Ensure the start.sh script is executable:
```bash
chmod +x /home/monlef/VSProjects/Python_bench/YT-web-application/start.sh
```

### Application Doesn't Launch
Check that all paths in the `.desktop` file are correct:
- Exec path should point to the correct directory
- Icon path should exist
- start.sh script should be executable

### Desktop Environment Specific

**GNOME**:
- Desktop shortcuts may need to be trusted: `gio set ~/Desktop/youtube-downloader.desktop metadata::trusted true`

**KDE**:
- Right-click desktop icon → Properties → Permissions → Check "Is executable"

**XFCE**:
- Right-click desktop icon → Allow launching

## Verification

Test the desktop file before installing:

```bash
# Test launch from command line
gtk-launch youtube-downloader
# or
dex /path/to/youtube-downloader.desktop
```

## Uninstallation

To remove the shortcut:

```bash
# From local applications
rm ~/.local/share/applications/youtube-downloader.desktop
update-desktop-database ~/.local/share/applications/

# From desktop
rm ~/Desktop/youtube-downloader.desktop

# From system (requires sudo)
sudo rm /usr/share/applications/youtube-downloader.desktop
sudo update-desktop-database /usr/share/applications/
```

## Desktop File Specification

The `.desktop` file follows the [freedesktop.org Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/latest/).

**Fields Used**:
- `Version`: Desktop Entry Specification version
- `Type`: Application launcher
- `Name`: Display name
- `Comment`: Description tooltip
- `Exec`: Command to execute
- `Icon`: Icon file or name
- `Terminal`: Whether to run in terminal
- `Categories`: Menu categories
- `Keywords`: Search keywords
- `StartupNotify`: Show startup notification

## Quick Install Script

For convenience, run this one-liner:

```bash
mkdir -p ~/.local/share/applications && \
cp youtube-downloader.desktop ~/.local/share/applications/ && \
chmod +x ~/.local/share/applications/youtube-downloader.desktop && \
update-desktop-database ~/.local/share/applications/ && \
echo "✓ Desktop shortcut installed successfully!"
```

---

**Note**: The desktop shortcut will launch the application using the virtual environment configured during setup. Ensure you've run `setup.sh` at least once before using the shortcut.
