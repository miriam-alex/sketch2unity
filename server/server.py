#!/usr/bin/env python3
"""
Local Model to Unity Bridge Server

Phase 1: Basic Flask server with health check endpoint
This server will eventually handle communication between laptop and Unity
for model selection and generation.
"""

import os
import glob
from pathlib import Path
from flask import Flask, jsonify, request, send_file, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for Unity communication

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify server is running.
    Returns a simple JSON status message.
    """
    return jsonify({
        "status": "ok",
        "message": "Local Model to Unity Bridge Server is running",
        "version": "1.0.0"
    })

@app.route('/api/list', methods=['GET'])
def list_models():
    """
    List all model files in the models directory.
    Scans ~/models/ for supported 3D model file formats.
    """
    try:
        models_dir = Path.home() / "models"
        
        # Supported model file extensions
        supported_extensions = ['*.fbx', '*.obj', '*.dae', '*.3ds', '*.blend', '*.ply', '*.stl']
        
        found_models = []
        
        if models_dir.exists():
            for extension in supported_extensions:
                # Find files with this extension
                pattern = str(models_dir / extension)
                files = glob.glob(pattern)
                
                for file_path in files:
                    file_info = {
                        "name": os.path.basename(file_path),
                        "path": file_path,
                        "size": os.path.getsize(file_path),
                        "extension": os.path.splitext(file_path)[1].lower(),
                        "modified": os.path.getmtime(file_path)
                    }
                    found_models.append(file_info)
        
        # Sort by name
        found_models.sort(key=lambda x: x["name"])
        
        return jsonify({
            "status": "success",
            "models_directory": str(models_dir),
            "count": len(found_models),
            "models": found_models
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error scanning models directory: {str(e)}"
        }), 500

@app.route('/api/search', methods=['POST'])
def search_models():
    """
    Search for models based on a query string.
    Filters models by name containing the search query.
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'query' parameter in request body"
            }), 400
        
        query = data['query'].lower().strip()
        if not query:
            return jsonify({
                "status": "error",
                "message": "Query cannot be empty"
            }), 400
        
        models_dir = Path.home() / "models"
        supported_extensions = ['*.fbx', '*.obj', '*.dae', '*.3ds', '*.blend', '*.ply', '*.stl']
        
        found_models = []
        
        if models_dir.exists():
            for extension in supported_extensions:
                pattern = str(models_dir / extension)
                files = glob.glob(pattern)
                
                for file_path in files:
                    filename = os.path.basename(file_path)
                    # Check if query matches filename (case-insensitive)
                    if query in filename.lower():
                        file_info = {
                            "name": filename,
                            "path": file_path,
                            "size": os.path.getsize(file_path),
                            "extension": os.path.splitext(file_path)[1].lower(),
                            "modified": os.path.getmtime(file_path)
                        }
                        found_models.append(file_info)
        
        # Sort by name
        found_models.sort(key=lambda x: x["name"])
        
        return jsonify({
            "status": "success",
            "query": query,
            "models_directory": str(models_dir),
            "count": len(found_models),
            "models": found_models
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error searching models: {str(e)}"
        }), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_model(filename):
    """
    Download a specific model file.
    Streams the file directly to the client.
    """
    try:
        models_dir = Path.home() / "models"
        file_path = models_dir / filename
        
        # Security check - ensure file is within models directory
        if not file_path.is_file() or not str(file_path).startswith(str(models_dir)):
            return jsonify({
                "status": "error",
                "message": f"File '{filename}' not found"
            }), 404
        
        # Check if it's a supported model file
        supported_extensions = ['.fbx', '.obj', '.dae', '.3ds', '.blend', '.ply', '.stl']
        file_extension = file_path.suffix.lower()
        
        if file_extension not in supported_extensions:
            return jsonify({
                "status": "error",
                "message": f"Unsupported file type: {file_extension}"
            }), 400
        
        # Send the file
        return send_file(
            str(file_path),
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error downloading file: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("Starting Local Model to Unity Bridge Server...")
    print("Health check available at: http://localhost:5002/health")
    print("Model listing available at: http://localhost:5002/api/list")
    print("Model search available at: http://localhost:5002/api/search")
    print("Model download available at: http://localhost:5002/api/download/<filename>")
    app.run(host='0.0.0.0', port=5002, debug=True)