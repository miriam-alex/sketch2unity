#!/usr/bin/env python3
"""
Local Model to Unity Bridge Server

Phase 1: Basic Flask server with health check endpoint
This server will eventually handle communication between laptop and Unity
for model selection and generation.
"""

import os
import glob
import json
import threading
import sys
from pathlib import Path
from flask import Flask, jsonify, request, send_file, abort
from flask_cors import CORS

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from layout_prompt import process_sketch, visualize_output, choose_sketch_path

app = Flask(__name__)
CORS(app)  # Enable CORS for Unity communication

SUPPORTED_EXTENSIONS = ['.obj', '.glb']
SUPPORTED_REGEX_EXTENSIONS = ['*.obj', '*.glb']
LAYOUT_OUTPUT_PATH = PROJECT_ROOT / "sample_output.json"
DEFAULT_LOT_BOUNDARY = [[0, 0], [0, 1000], [1000, 0], [1000, 1000]]
DEFAULT_SITE_WIDTH_FT = 1000
DEFAULT_SITE_HEIGHT_FT = 1000

layout_generation_lock = threading.Lock()


def get_models_dir() -> Path:
    """Return the project's models directory path."""
    return Path(__file__).resolve().parent.parent / "models"

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
        models_dir = get_models_dir()
        
        # Supported model file extensions        
        found_models = []
        
        if models_dir.exists():
            for extension in SUPPORTED_REGEX_EXTENSIONS:
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
        
        models_dir = get_models_dir()
        found_models = []
        
        if models_dir.exists():
            for extension in SUPPORTED_REGEX_EXTENSIONS:
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
        models_dir = get_models_dir()
        file_path = models_dir / filename
        
        # Security check - ensure file is within models directory
        if not file_path.is_file() or not str(file_path).startswith(str(models_dir)):
            return jsonify({
                "status": "error",
                "message": f"File '{filename}' not found"
            }), 404
        
        # Check if it's a supported model file
        file_extension = file_path.suffix.lower()
        
        if file_extension not in SUPPORTED_EXTENSIONS:
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

@app.route('/api/layout/generate', methods=['POST'])
def generate_layout_from_sketch():
    """
    Trigger sketch selection on the local machine, run prompting, and return layout JSON.
    This endpoint intentionally accepts no request payload for local-only workflows.
    """
    if not layout_generation_lock.acquire(blocking=False):
        return jsonify({
            "status": "error",
            "message": "Layout generation is already in progress."
        }), 409

    try:
        selected_sketch_path = choose_sketch_path()
        if selected_sketch_path is None:
            return jsonify({
                "status": "error",
                "message": "Sketch selection canceled."
            }), 400

        output = process_sketch(
            output_path=LAYOUT_OUTPUT_PATH,
            sketch_path=selected_sketch_path,
            lot_boundary=DEFAULT_LOT_BOUNDARY,
            site_width_ft=DEFAULT_SITE_WIDTH_FT,
            site_height_ft=DEFAULT_SITE_HEIGHT_FT,
        )

        if output is None:
            return jsonify({
                "status": "error",
                "message": "Layout generation failed. Check server logs for details."
            }), 502

        if not LAYOUT_OUTPUT_PATH.exists():
            return jsonify({
                "status": "error",
                "message": f"Expected output file was not created: {LAYOUT_OUTPUT_PATH}"
            }), 500

        try:
            site_data = json.loads(LAYOUT_OUTPUT_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return jsonify({
                "status": "error",
                "message": f"Generated output is not valid JSON: {exc.msg}"
            }), 500

        visualization_warning = None
        try:
            visualize_output(site_data)
        except Exception as exc:
            visualization_warning = str(exc)

        response = {
            "status": "success",
            "message": "Layout generated successfully.",
            "layout": site_data,
            "output_path": str(LAYOUT_OUTPUT_PATH),
            "selected_sketch": str(selected_sketch_path),
        }
        if visualization_warning:
            response["visualization_warning"] = visualization_warning

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Unexpected error during layout generation: {str(e)}"
        }), 500
    finally:
        layout_generation_lock.release()

if __name__ == '__main__':
    print("Starting Local Model to Unity Bridge Server...")
    print("Health check available at: http://localhost:5002/health")
    print("Model listing available at: http://localhost:5002/api/list")
    print("Model search available at: http://localhost:5002/api/search")
    print("Model download available at: http://localhost:5002/api/download/<filename>")
    print("Layout generation available at: http://localhost:5002/api/layout/generate")
    app.run(host='0.0.0.0', port=5002, debug=True)