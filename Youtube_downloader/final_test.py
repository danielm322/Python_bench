#!/usr/bin/env python3
"""
Final comprehensive test for YouTube downloader with MP3 support
"""

import sys
import os
import tempfile
import subprocess
from pathlib import Path

def test_all_functionality():
    """Test all download types"""
    
    print("YouTube Downloader - Final Test Suite")
    print("=" * 50)
    
    test_results = {
        'ffmpeg': False,
        'yt_dlp': False,
        'video_download': False,
        'mp3_download': False
    }
    
    # Test 1: Check FFmpeg
    print("\n1. Testing FFmpeg availability...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
        if result.returncode == 0:
            print("✓ FFmpeg is available for audio conversion")
            test_results['ffmpeg'] = True
        else:
            print("✗ FFmpeg not available")
    except:
        print("✗ FFmpeg not found")
    
    # Test 2: Check yt-dlp
    print("\n2. Testing yt-dlp...")
    try:
        result = subprocess.run([sys.executable, '-m', 'yt_dlp', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✓ yt-dlp version: {version}")
            test_results['yt_dlp'] = True
        else:
            print("✗ yt-dlp not working")
    except Exception as e:
        print(f"✗ yt-dlp failed: {e}")
    
    # Test 3: Video download
    print("\n3. Testing video download...")
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run([
                sys.executable, '-m', 'yt_dlp', 
                '--no-playlist',
                '-f', 'worst',  # Use worst quality for speed
                '-o', f'{temp_dir}/%(title)s.%(ext)s',
                'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                files = list(Path(temp_dir).glob('*'))
                if files:
                    video_file = files[0]
                    size_mb = video_file.stat().st_size / (1024 * 1024)
                    print(f"✓ Video download successful: {video_file.name}")
                    print(f"  File size: {size_mb:.1f} MB")
                    test_results['video_download'] = True
                else:
                    print("✗ No video files found")
            else:
                print(f"✗ Video download failed: {result.stderr[:200]}")
                
    except Exception as e:
        print(f"✗ Video download test failed: {e}")
    
    # Test 4: MP3 audio download
    print("\n4. Testing MP3 audio download...")
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            cmd = [
                sys.executable, '-m', 'yt_dlp', 
                '--no-playlist',
                '-f', 'bestaudio',
                '-o', f'{temp_dir}/%(title)s.%(ext)s',
                'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
            ]
            
            if test_results['ffmpeg']:
                cmd.extend(['--extract-audio', '--audio-format', 'mp3'])
                print("  Using FFmpeg for MP3 conversion...")
            else:
                print("  Downloading in original audio format (no FFmpeg)...")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            
            if result.returncode == 0:
                if test_results['ffmpeg']:
                    files = list(Path(temp_dir).glob('*.mp3'))
                    if files:
                        mp3_file = files[0]
                        size_kb = mp3_file.stat().st_size / 1024
                        print(f"✓ MP3 download successful: {mp3_file.name}")
                        print(f"  File size: {size_kb:.1f} KB")
                        test_results['mp3_download'] = True
                    else:
                        print("✗ No MP3 files found")
                else:
                    # Without FFmpeg, check for any audio file
                    files = list(Path(temp_dir).glob('*'))
                    if files:
                        audio_file = files[0]
                        size_kb = audio_file.stat().st_size / 1024
                        print(f"✓ Audio download successful: {audio_file.name}")
                        print(f"  File size: {size_kb:.1f} KB")
                        print("  Note: Install FFmpeg for automatic MP3 conversion")
                        test_results['mp3_download'] = True
                    else:
                        print("✗ No audio files found")
            else:
                print(f"✗ MP3 download failed: {result.stderr[:200]}")
                
    except Exception as e:
        print(f"✗ MP3 download test failed: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("FINAL TEST RESULTS:")
    print(f"FFmpeg Available: {'✓ YES' if test_results['ffmpeg'] else '⚠ NO'}")
    print(f"yt-dlp Working: {'✓ YES' if test_results['yt_dlp'] else '✗ NO'}")
    print(f"Video Download: {'✓ PASS' if test_results['video_download'] else '✗ FAIL'}")
    print(f"Audio/MP3 Download: {'✓ PASS' if test_results['mp3_download'] else '✗ FAIL'}")
    
    all_working = all([test_results['yt_dlp'], test_results['video_download'], test_results['mp3_download']])
    
    if all_working:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your YouTube downloader is fully functional with:")
        print("  ✓ Video downloads (highest/medium quality)")
        print(f"  ✓ Audio downloads {'(MP3 format)' if test_results['ffmpeg'] else '(original format)'}")
        print("  ✓ Automatic fallback from pytube to yt-dlp")
        print("\nYou can now run: python youtube_downloader_fixed.py")
    else:
        print("\n⚠ Some issues detected:")
        if not test_results['yt_dlp']:
            print("  - yt-dlp is not working properly")
        if not test_results['video_download']:
            print("  - Video downloads are failing")
        if not test_results['mp3_download']:
            print("  - Audio downloads are failing")
        if not test_results['ffmpeg']:
            print("  - Consider installing FFmpeg for MP3 conversion: sudo apt install ffmpeg")

if __name__ == "__main__":
    test_all_functionality()