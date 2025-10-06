#!/usr/bin/env python3
"""
Test script to verify YouTube downloader functionality
"""

import sys
import os
import tempfile
import subprocess
from pathlib import Path

# Add the project directory to the path
sys.path.insert(0, '/home/monlef/VSProjects/Python_bench')

def test_pytube():
    """Test pytube functionality"""
    print("Testing pytube...")
    try:
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context
        
        from pytube import YouTube
        
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        yt = YouTube(test_url)
        
        print(f"✓ Video title: {yt.title}")
        print(f"✓ Video length: {yt.length} seconds")
        
        streams = yt.streams.all()
        print(f"✓ Available streams: {len(streams)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Pytube failed: {e}")
        return False

def test_ytdlp():
    """Test yt-dlp functionality"""
    print("\nTesting yt-dlp...")
    try:
        result = subprocess.run([
            sys.executable, '-m', 'yt_dlp', 
            '--no-download', 
            '--print', 'title',
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            title = result.stdout.strip()
            print(f"✓ Video title: {title}")
            return True
        else:
            print(f"✗ yt-dlp failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ yt-dlp failed: {e}")
        return False

def test_download():
    """Test actual download with yt-dlp"""
    print("\nTesting actual download...")
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"Downloading to: {temp_dir}")
            
            result = subprocess.run([
                sys.executable, '-m', 'yt_dlp', 
                '--no-playlist',
                '-f', 'worst',  # Use worst quality for faster test
                '-o', f'{temp_dir}/%(title)s.%(ext)s',
                'https://www.youtube.com/watch?v=jNQXAC9IVRw'  # Short test video
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                files = list(Path(temp_dir).glob('*'))
                if files:
                    print(f"✓ Download successful: {files[0].name}")
                    return True
                else:
                    print("✗ No files found after download")
                    return False
            else:
                print(f"✗ Download failed: {result.stderr}")
                return False
                
    except Exception as e:
        print(f"✗ Download test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("YouTube Downloader Test Suite")
    print("=" * 40)
    
    pytube_works = test_pytube()
    ytdlp_works = test_ytdlp()
    download_works = test_download()
    
    print("\n" + "=" * 40)
    print("Test Results:")
    print(f"Pytube: {'✓ PASS' if pytube_works else '✗ FAIL'}")
    print(f"yt-dlp: {'✓ PASS' if ytdlp_works else '✗ FAIL'}")
    print(f"Download: {'✓ PASS' if download_works else '✗ FAIL'}")
    
    if ytdlp_works:
        print("\n✓ YouTube downloader should work with yt-dlp fallback!")
        print("You can run the GUI application with:")
        print("  python youtube_downloader_fixed.py")
    else:
        print("\n✗ Issues detected. Check your internet connection and dependencies.")

if __name__ == "__main__":
    main()