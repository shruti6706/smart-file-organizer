"""
Flask API for Smart File Organizer.
"""
from flask import Flask, jsonify, request
from pathlib import Path
from organizer import FileOrganizer

app = Flask(__name__)

# Default target folder - uses user's home directory
TARGET_FOLDER = str(Path.home() / "Desktop")


@app.route('/organize', methods=['POST'])
def organize_endpoint():
    """
    Organize files in the target folder.
    
    Returns:
        JSON response with file counts per category
    """
    try:
        # Allow custom folder path from request body
        data = request.get_json() or {}
        folder = data.get('target_folder', TARGET_FOLDER)
        
        # Create organizer and run
        organizer = FileOrganizer(folder)
        results = organizer.organize()
        
        # Calculate total
        total = sum(results.values())
        
        return jsonify({
            'success': True,
            'results': results,
            'total': total,
            'message': f'Successfully organized {total} files'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal error: {str(e)}'
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    print(f"Starting Smart File Organizer API...")
    print(f"Target folder: {TARGET_FOLDER}")
    print(f"API available at: http://localhost:8000")
    print(f"Endpoint: POST /organize")
    app.run(debug=False, host='0.0.0.0', port=8000)
