"""
Flask web application for converting .mod video files to .mp4 format.
"""
import os
import uuid
from datetime import datetime, timedelta
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
import converter


# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['ALLOWED_EXTENSIONS'] = {'mod'}

# Ensure upload and output directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


def allowed_file(filename: str) -> bool:
    """
    Check if the uploaded file has an allowed extension.
    
    Args:
        filename: Name of the file to check
    
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def cleanup_old_files(max_age_hours: int = 24):
    """
    Remove files older than specified hours from upload and output directories.
    
    Args:
        max_age_hours: Maximum age of files in hours before deletion
    """
    current_time = datetime.now()
    cutoff_time = current_time - timedelta(hours=max_age_hours)
    
    for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                file_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_modified_time < cutoff_time:
                    try:
                        os.remove(file_path)
                        print(f"Cleaned up old file: {file_path}")
                    except Exception as e:
                        print(f"Error cleaning up {file_path}: {e}")


@app.route('/')
def index():
    """Serve the main application page."""
    # Clean up old files on page load
    cleanup_old_files()
    
    # Get available quality presets
    quality_presets = converter.get_quality_presets()
    
    return render_template('index.html', quality_presets=quality_presets)


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and conversion.
    
    Returns:
        JSON response with conversion status and download link
    """
    # Check if file is present in request
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Check if file was selected
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    # Check if quality preset is provided
    quality = request.form.get('quality', 'medium')
    if quality not in converter.QUALITY_PRESETS:
        return jsonify({'success': False, 'error': 'Invalid quality preset'}), 400
    
    # Validate file extension
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': 'Invalid file type. Only .mod files are allowed.'
        }), 400
    
    try:
        # Generate unique filename to avoid conflicts
        unique_id = str(uuid.uuid4())
        original_filename = secure_filename(file.filename)
        input_filename = f"{unique_id}_{original_filename}"
        output_filename = f"{unique_id}_{os.path.splitext(original_filename)[0]}.mp4"
        
        # Save uploaded file
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        file.save(input_path)
        
        # Convert the file
        print(f"Starting conversion: {input_path} -> {output_path} (quality: {quality})")
        success, message = converter.convert_mod_to_mp4(input_path, output_path, quality)
        print(f"Conversion result: success={success}, message={message}")
        
        if success:
            # Clean up input file after successful conversion
            try:
                os.remove(input_path)
            except Exception as e:
                print(f"Error removing input file: {e}")
            
            return jsonify({
                'success': True,
                'message': message,
                'download_url': f'/download/{output_filename}',
                'filename': output_filename
            })
        else:
            # Clean up input file on failure
            try:
                os.remove(input_path)
            except Exception as e:
                print(f"Error removing input file: {e}")
            
            return jsonify({
                'success': False,
                'error': message
            }), 500
            
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"ERROR in upload_file: {error_details}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/download/<filename>')
def download_file(filename):
    """
    Serve converted file for download.
    
    Args:
        filename: Name of the file to download
    
    Returns:
        File download response
    """
    try:
        # Secure the filename to prevent directory traversal
        safe_filename = secure_filename(filename)
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], safe_filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Send file and schedule cleanup after download
        response = send_file(
            file_path,
            as_attachment=True,
            download_name=safe_filename,
            mimetype='video/mp4'
        )
        
        # Note: In production, you might want to implement a more sophisticated
        # cleanup mechanism, such as a background task that removes files after
        # a certain period or after confirming download completion
        
        return response
        
    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500


@app.route('/cleanup', methods=['POST'])
def cleanup():
    """
    Manually trigger cleanup of old files.
    
    Returns:
        JSON response with cleanup status
    """
    try:
        cleanup_old_files()
        return jsonify({'success': True, 'message': 'Cleanup completed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/health')
def health_check():
    """
    Health check endpoint to verify FFmpeg availability.
    
    Returns:
        JSON response with health status
    """
    ffmpeg_available = converter.check_ffmpeg_installed()
    
    return jsonify({
        'status': 'healthy' if ffmpeg_available else 'degraded',
        'ffmpeg_available': ffmpeg_available,
        'message': 'FFmpeg is available' if ffmpeg_available else 'FFmpeg is not installed'
    })


if __name__ == '__main__':
    # Check FFmpeg availability on startup
    if not converter.check_ffmpeg_installed():
        print("WARNING: FFmpeg is not installed!")
        print("Please install FFmpeg to use this application.")
        print("Visit: https://ffmpeg.org/download.html")
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)
