#!/usr/bin/env python3
"""
Test script to verify yt-dlp can access YouTube with the new configuration.
"""

import sys
import yt_dlp

def test_youtube_access():
    """Test YouTube access with proper headers."""
    
    test_url = "https://www.youtube.com/watch?v=YqeW9_5kURI"
    
    print("🔍 Testing YouTube access with updated configuration...")
    print(f"   URL: {test_url}")
    print("")
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        },
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("📥 Fetching video information...")
            info = ydl.extract_info(test_url, download=False)
            
            print("✅ SUCCESS! Video information retrieved:")
            print(f"   Title: {info.get('title', 'Unknown')}")
            print(f"   Duration: {info.get('duration', 0)} seconds")
            print(f"   Uploader: {info.get('uploader', 'Unknown')}")
            print(f"   View count: {info.get('view_count', 0):,}")
            print("")
            print("✅ YouTube access is working correctly!")
            print("   The 403 Forbidden error should now be resolved.")
            return True
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print("")
        print("Troubleshooting:")
        print("1. Make sure you have the latest yt-dlp version:")
        print("   pip install --upgrade yt-dlp")
        print("2. Check your internet connection")
        print("3. Try the video URL in a browser to ensure it's accessible")
        return False

if __name__ == '__main__':
    success = test_youtube_access()
    sys.exit(0 if success else 1)
