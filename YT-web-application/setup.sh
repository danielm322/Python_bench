#!/bin/bash

# YouTube Downloader - Setup Script
# This script automates the setup process for the application

echo "🎬 YouTube Downloader - Setup Script"
echo "===================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.9"

if [ -z "$python_version" ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✓ Found Python $python_version"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ Pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Check for FFmpeg
echo "Checking for FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    ffmpeg_version=$(ffmpeg -version 2>&1 | head -n 1)
    echo "✓ FFmpeg is installed: $ffmpeg_version"
else
    echo "⚠️  FFmpeg is not installed"
    echo "   FFmpeg is required for video/audio processing"
    echo "   Install it using:"
    echo "   - Ubuntu/Debian: sudo apt install ffmpeg"
    echo "   - macOS: brew install ffmpeg"
fi
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    
    # Generate a random secret key
    secret_key=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    
    # Update the .env file with the generated secret key
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your-secret-key-here/$secret_key/" .env
    else
        # Linux
        sed -i "s/your-secret-key-here/$secret_key/" .env
    fi
    
    echo "✓ .env file created with random secret key"
else
    echo "✓ .env file already exists"
fi
echo ""

# Create downloads directory
if [ ! -d "downloads" ]; then
    mkdir -p downloads
    echo "✓ Downloads directory created"
else
    echo "✓ Downloads directory already exists"
fi
echo ""

# Create logs directory
if [ ! -d "logs" ]; then
    mkdir -p logs
    echo "✓ Logs directory created"
else
    echo "✓ Logs directory already exists"
fi
echo ""

echo "===================================="
echo "✓ Setup complete!"
echo ""
echo "To start the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the application: python run.py"
echo "3. Open your browser: http://localhost:5000"
echo ""
echo "For more information, see README.md"
echo "===================================="
