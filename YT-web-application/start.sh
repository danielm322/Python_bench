#!/bin/bash

# YouTube Downloader - Run Script
# Quick start script for running the application

echo "🎬 Starting YouTube Downloader..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup.sh first:"
    echo "  bash setup.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
fi

# Server configuration
SERVER_URL="http://localhost:5000"
SERVER_PID=""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down YouTube Downloader..."
    
    # Kill the Flask server if it's running
    if [ ! -z "$SERVER_PID" ] && kill -0 $SERVER_PID 2>/dev/null; then
        kill $SERVER_PID 2>/dev/null
        wait $SERVER_PID 2>/dev/null
    fi
    
    # Also kill any remaining Python processes running run.py
    pkill -f "python.*run.py" 2>/dev/null
    
    echo "✓ Server stopped successfully"
    exit 0
}

# Set up trap to catch Ctrl+C and other termination signals
trap cleanup SIGINT SIGTERM EXIT

# Function to open browser
open_browser() {
    # Wait a moment for server to start
    sleep 2
    
    echo "🌐 Opening browser..."
    
    # Detect OS and open browser accordingly
    if command -v xdg-open > /dev/null; then
        # Linux
        xdg-open "$SERVER_URL" 2>/dev/null &
    elif command -v gnome-open > /dev/null; then
        # Older Linux systems
        gnome-open "$SERVER_URL" 2>/dev/null &
    elif command -v open > /dev/null; then
        # macOS
        open "$SERVER_URL" 2>/dev/null &
    elif command -v start > /dev/null; then
        # Windows (Git Bash)
        start "$SERVER_URL" 2>/dev/null &
    else
        echo "⚠️  Could not detect browser command. Please open manually:"
        echo "   $SERVER_URL"
    fi
}

# Function to wait for server to be ready
wait_for_server() {
    echo "⏳ Waiting for server to start..."
    
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if curl -s "$SERVER_URL" > /dev/null 2>&1; then
            echo "✓ Server is ready!"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 0.5
    done
    
    echo "⚠️  Server took too long to start"
    return 1
}

# Start the Flask application in the background
echo "🚀 Starting Flask application on $SERVER_URL"
echo "📝 Press Ctrl+C to stop the server"
echo ""

python run.py &
SERVER_PID=$!

# Wait for server to be ready
if wait_for_server; then
    # Open browser once server is ready
    open_browser
    echo ""
    echo "✓ Application is running!"
    echo "  URL: $SERVER_URL"
    echo "  PID: $SERVER_PID"
    echo ""
    echo "Press Ctrl+C to stop..."
fi

# Wait for the server process to finish (or be killed by Ctrl+C)
wait $SERVER_PID 