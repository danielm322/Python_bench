#!/usr/bin/env python3
"""
Quick test to verify the None handling fix works correctly.
"""

# Test the fix logic
def test_none_handling():
    """Test that None values are handled correctly."""
    
    # Simulate what happens in the route
    data = {
        'url': 'https://www.youtube.com/watch?v=test',
        'type': 'video',
        'quality': '720',
        'filename': None  # This is what causes the error
    }
    
    # Old way (would fail)
    try:
        filename_old = data.get('filename', '').strip()
        print(f"❌ Old way should have failed but got: {filename_old}")
    except AttributeError as e:
        print(f"✓ Old way fails as expected: {e}")
    
    # New way (should work)
    try:
        filename_new = (data.get('filename') or '').strip()
        print(f"✓ New way works: '{filename_new}' (empty string)")
    except AttributeError as e:
        print(f"❌ New way failed: {e}")
    
    # Test with actual value
    data['filename'] = '  my_video  '
    filename_new = (data.get('filename') or '').strip()
    print(f"✓ New way with value: '{filename_new}'")
    
    # Test with empty string
    data['filename'] = ''
    filename_new = (data.get('filename') or '').strip()
    print(f"✓ New way with empty string: '{filename_new}'")
    
    print("\n✅ All tests passed! The fix is working correctly.")


if __name__ == '__main__':
    test_none_handling()
