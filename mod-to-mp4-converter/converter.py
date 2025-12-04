"""
Video conversion module for MOD to MP4 conversion using FFmpeg.
"""
import subprocess
import os
from typing import Dict, Tuple


# Quality presets with resolution and bitrate settings
QUALITY_PRESETS = {
    'high': {
        'resolution': '1920x1080',
        'video_bitrate': '8M',
        'audio_bitrate': '192k',
        'description': 'High Quality (1080p, 8 Mbps)'
    },
    'medium': {
        'resolution': '1280x720',
        'video_bitrate': '4M',
        'audio_bitrate': '128k',
        'description': 'Medium Quality (720p, 4 Mbps)'
    },
    'low': {
        'resolution': '854x480',
        'video_bitrate': '2M',
        'audio_bitrate': '96k',
        'description': 'Low Quality (480p, 2 Mbps)'
    }
}


def check_ffmpeg_installed() -> bool:
    """
    Check if FFmpeg is installed and accessible.
    
    Returns:
        bool: True if FFmpeg is available, False otherwise
    """
    try:
        subprocess.run(
            ['ffmpeg', '-version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def convert_mod_to_mp4(
    input_path: str,
    output_path: str,
    quality: str = 'medium'
) -> Tuple[bool, str]:
    """
    Convert a .mod file to .mp4 format using FFmpeg.
    
    Args:
        input_path: Path to the input .mod file
        output_path: Path where the output .mp4 file should be saved
        quality: Quality preset ('high', 'medium', or 'low')
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    # Validate input file exists
    if not os.path.exists(input_path):
        return False, f"Input file not found: {input_path}"
    
    # Validate quality preset
    if quality not in QUALITY_PRESETS:
        return False, f"Invalid quality preset: {quality}. Must be one of {list(QUALITY_PRESETS.keys())}"
    
    # Check if FFmpeg is installed
    if not check_ffmpeg_installed():
        return False, "FFmpeg is not installed. Please install FFmpeg to use this application."
    
    # Get quality settings
    preset = QUALITY_PRESETS[quality]
    
    # Parse resolution into width and height
    width, height = preset['resolution'].split('x')
    
    # Build FFmpeg command
    # -i: input file
    # -vf scale: resize video to target resolution
    # -c:v libx264: use H.264 codec for video
    # -b:v: video bitrate
    # -c:a aac: use AAC codec for audio
    # -b:a: audio bitrate
    # -movflags +faststart: optimize for web streaming
    # -y: overwrite output file if it exists
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_path,
        '-vf', f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2",
        '-c:v', 'libx264',
        '-b:v', preset['video_bitrate'],
        '-c:a', 'aac',
        '-b:a', preset['audio_bitrate'],
        '-movflags', '+faststart',
        '-y',
        output_path
    ]
    
    try:
        # Run FFmpeg conversion
        result = subprocess.run(
            ffmpeg_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        
        # Verify output file was created
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            if file_size > 0:
                return True, f"Conversion successful! Output file size: {file_size / (1024*1024):.2f} MB"
            else:
                return False, "Conversion failed: Output file is empty"
        else:
            return False, "Conversion failed: Output file was not created"
            
    except subprocess.CalledProcessError as e:
        error_message = e.stderr if e.stderr else str(e)
        return False, f"FFmpeg conversion failed: {error_message}"
    except Exception as e:
        return False, f"Unexpected error during conversion: {str(e)}"


def get_quality_presets() -> Dict[str, Dict[str, str]]:
    """
    Get available quality presets.
    
    Returns:
        Dictionary of quality presets
    """
    return QUALITY_PRESETS
