#!/bin/bash

# Desktop Shortcut Installation Script
# Installs YouTube Downloader desktop shortcut for the current user

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 YouTube Downloader - Desktop Shortcut Installer${NC}"
echo ""

# Get the absolute path of the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DESKTOP_FILE="$SCRIPT_DIR/youtube-downloader.desktop"

# Check if desktop file exists
if [ ! -f "$DESKTOP_FILE" ]; then
    echo -e "${YELLOW}⚠️  Error: youtube-downloader.desktop not found${NC}"
    exit 1
fi

# Create local applications directory if it doesn't exist
mkdir -p ~/.local/share/applications

# Copy desktop file
echo -e "${BLUE}📋 Copying desktop file...${NC}"
cp "$DESKTOP_FILE" ~/.local/share/applications/

# Make executable
echo -e "${BLUE}🔐 Setting permissions...${NC}"
chmod +x ~/.local/share/applications/youtube-downloader.desktop

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    echo -e "${BLUE}🔄 Updating desktop database...${NC}"
    update-desktop-database ~/.local/share/applications/ 2>/dev/null || true
fi

echo ""
echo -e "${GREEN}✓ Desktop shortcut installed successfully!${NC}"
echo ""
echo -e "You can now launch YouTube Downloader from:"
echo -e "  • Application menu (Network or Audio & Video category)"
echo -e "  • Search for '${BLUE}YouTube Downloader${NC}'"
echo ""
echo -e "${YELLOW}Optional:${NC} Install to desktop for quick access:"
echo -e "  cp $DESKTOP_FILE ~/Desktop/"
echo -e "  chmod +x ~/Desktop/youtube-downloader.desktop"
echo ""
