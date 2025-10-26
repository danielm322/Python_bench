#!/bin/bash

# Project Structure Verification Script
# Verifies that all required files and directories exist

echo "🔍 YouTube Downloader - Project Structure Verification"
echo "======================================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1 (MISSING)"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        return 0
    else
        echo -e "${RED}✗${NC} $1/ (MISSING)"
        return 1
    fi
}

missing=0

echo "📁 Project Structure:"
echo ""

# Root files
check_file "run.py" || ((missing++))
check_file "requirements.txt" || ((missing++))
check_file "README.md" || ((missing++))
check_file "DEVELOPMENT.md" || ((missing++))
check_file "QUICKSTART.md" || ((missing++))
check_file "PROJECT_SUMMARY.md" || ((missing++))
check_file ".env.example" || ((missing++))
check_file ".gitignore" || ((missing++))
check_file "setup.sh" || ((missing++))
check_file "start.sh" || ((missing++))
echo ""

# Directories
check_dir "app" || ((missing++))
check_dir "app/static" || ((missing++))
check_dir "app/static/css" || ((missing++))
check_dir "app/static/js" || ((missing++))
check_dir "app/templates" || ((missing++))
check_dir "tests" || ((missing++))
check_dir "downloads" || ((missing++))
echo ""

# App files
echo "📄 Application Files:"
echo ""
check_file "app/__init__.py" || ((missing++))
check_file "app/config.py" || ((missing++))
check_file "app/downloader.py" || ((missing++))
check_file "app/routes.py" || ((missing++))
check_file "app/utils.py" || ((missing++))
echo ""

# Static files
echo "🎨 Static Files:"
echo ""
check_file "app/static/css/styles.css" || ((missing++))
check_file "app/static/js/main.js" || ((missing++))
echo ""

# Templates
echo "📝 Templates:"
echo ""
check_file "app/templates/index.html" || ((missing++))
check_file "app/templates/about.html" || ((missing++))
echo ""

# Tests
echo "🧪 Test Files:"
echo ""
check_file "tests/__init__.py" || ((missing++))
check_file "tests/test_downloader.py" || ((missing++))
check_file "tests/test_utils.py" || ((missing++))
echo ""

# Summary
echo "======================================================"
if [ $missing -eq 0 ]; then
    echo -e "${GREEN}✓ All files present! Project structure is complete.${NC}"
    echo ""
    echo "🚀 Ready to run:"
    echo "   bash setup.sh"
    echo "   bash start.sh"
else
    echo -e "${RED}✗ $missing file(s) or directory(ies) missing!${NC}"
    echo ""
    echo "Please ensure all files are present before running the application."
fi
echo "======================================================"
