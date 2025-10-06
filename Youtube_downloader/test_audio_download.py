#!/usr/bin/env python3
"""
Test script to verify MP3 audio download functionality
"""

import sys
import os
import tempfile
import subprocess
from pathlib import Path

def test_audio_download():
    """Test audio-only download with MP3 conversion"""
    print("Testing audio-only download (MP3 format)...")
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"Downloading audio to: {temp_dir}")
            
            # Test with a short video
            test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # Short test video
            
            result = subprocess.run([
                sys.executable, '-m', 'yt_dlp', 
                '--no-playlist',
                '-f', 'bestaudio',
                '--extract-audio',
                '--audio-format', 'mp3',
                '-o', f'{temp_dir}/%(title)s.%(ext)s',
                test_url
            ], capture_output=True, text=True, timeout=120)
            
            print("yt-dlp output:")
            print(result.stdout)
            
            if result.returncode == 0:
                files = list(Path(temp_dir).glob('*.mp3'))
                if files:
                    mp3_file = files[0]
                    print(f"✓ MP3 download successful: {mp3_file.name}")
                    print(f"✓ File size: {mp3_file.stat().st_size / 1024:.1f} KB")
                    return True
                else:
                    print("✗ No MP3 files found after download")
                    all_files = list(Path(temp_dir).glob('*'))
                    print(f"Files found: {[f.name for f in all_files]}")
                    return False
            else:
                print(f"✗ Download failed: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"✗ Audio download test failed: {e}")
        return False

def check_ffmpeg():
    """Check if ffmpeg is available for audio conversion"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=10)
        if result.returncode == 0:
            print("✓ FFmpeg is available for audio conversion")
            return True
        else:
            print("⚠ FFmpeg not found - audio conversion may be limited")
            return False
    except:
        print("⚠ FFmpeg not found - will use basic file extension change")
        return False

def main():
    """Run audio download tests"""
    print("Audio Download Test Suite")
    print("=" * 40)
    
    ffmpeg_available = check_ffmpeg()
    audio_works = test_audio_download()
    
    print("\n" + "=" * 40)
    print("Test Results:")
    print(f"FFmpeg Available: {'✓ YES' if ffmpeg_available else '⚠ NO'}")
    print(f"MP3 Download: {'✓ PASS' if audio_works else '✗ FAIL'}")
    
    if audio_works:
        print("\n✓ Audio download with MP3 format is working!")
        if not ffmpeg_available:
            print("Note: Install ffmpeg for better audio conversion quality:")
            print("  sudo apt install ffmpeg  # On Ubuntu/Debian")
    else:
        print("\n✗ Audio download test failed.")

if __name__ == "__main__":
    main()