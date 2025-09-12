import os
from flask import Flask, request, render_template_string, jsonify
from flask_cors import CORS
from template import HTML_TEMPLATE
from model import get_gemini_analysis, get_gemini_chat_response

app = Flask(__name__)
CORS(app)

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
        analysis_result = get_gemini_analysis(image_bytes)
        print("Analysis result received from Gemini")
        return jsonify({'analysis': analysis_result})
    except Exception as e:
        print(f"Error in analyze route: {str(e)}")
        return jsonify({'error': f'File processing error: {str(e)}'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Handles chatbot messages and returns Gemini responses."""
    print("Received request at /chat")
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    print(f"Chatbot received message: {user_message}")
    bot_response = get_gemini_chat_response(user_message)
    print(f"Chatbot sending response: {bot_response[:50]}...")
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    print("--- Gemini PCB Defect Detection & Chatbot App ---")
    print("Starting Flask server...")
    print("Open your browser and navigate to http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)