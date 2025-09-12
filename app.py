from flask import Flask, request, render_template_string, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

from model import genesiscircuit_analysis
from templates import HTML_TEMPLATE

@app.route('/')
def home():
    """Renders the main HTML page."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handles the image upload and returns the Gemini analysis."""
    print("Received request at /analyze")
    if 'file' not in request.files:
        print("No file part in request")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        print("No file selected")
        return jsonify({'error': 'No selected file'}), 400

    print(f"Processing file: {file.filename}")
    try:
        image_bytes = file.read()
        print(f"Image bytes read: {len(image_bytes)} bytes")
        analysis_result = genesiscircuit_analysis(image_bytes)
        print("Analysis result received from Gemini")
        return jsonify({'analysis': analysis_result})
    except Exception as e:
        print(f"Error in analyze route: {str(e)}")
        return jsonify({'error': f'File processing error: {str(e)}'}), 500

if __name__ == '__main__':
    print("--- Gemini PCB Defect Detection App ---")
    print("Starting Flask server...")
    print("Open your browser and navigate to http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)