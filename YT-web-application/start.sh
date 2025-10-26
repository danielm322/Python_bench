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

# Run the application
echo "Starting Flask application on http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python run.py
