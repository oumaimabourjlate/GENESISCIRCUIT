import os
import base64
import google.generativeai as genai
from PIL import Image
import io
import key

# Configure the Gemini client
try:
    genai.configure(api_key= key )
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    exit()

def genesiscircuit_analysis(image_bytes):
    """
    Analyzes a PCB image using the Gemini API and returns a structured response.
    """
    try:
        print("Loading image for Gemini analysis")
        img = Image.open(io.BytesIO(image_bytes))
        print(f"Image format: {img.format}, size: {img.size}")
        
        # Validate image size and format
        if img.size[0] * img.size[1] > 5000 * 5000:
            return "<h3>Error</h3><p>Image is too large. Please use an image smaller than 5000x5000 pixels.</p>"
        if img.format not in ['JPEG', 'PNG']:
            return "<h3>Error</h3><p>Unsupported image format. Please use JPEG or PNG.</p>"

        # Initialize the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")  # Updated to a more commonly available model
        prompt = """
        Act as an expert PCB Quality Assurance inspector. Analyze the provided image of a Printed Circuit Board.

        Your task is to identify all manufacturing defects with high precision.
        Structure your response in the following format:

        *Status:* [Defective or Production-Ready]
        *Defect Description:*
        - [List each defect as a bullet point. Describe the type of defect (e.g., "Poor Solder Joint", "Missing Component", "Solder Bridge", "Discoloration/Corrosion", "Cracked Trace") and specify its location using component designators (like U3, R1) or a general area.]
        *Severity:* [High, Medium, or Low]
        *Suggested Fixes:*
        - [Provide a bulleted list of actionable steps to repair the identified defects.]

        If no defects are found, the Status should be "Production-Ready" and the other fields should state "N/A".
        """

        print("Sending request to Gemini API")
        response = model.generate_content([prompt, img])
        print("Gemini API response received")
        return response.text.replace('\n', '<br>')
    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        return f"<h3>Error</h3><p>Could not analyze the image. The API call failed.</p><p><b>Details:</b> {str(e)}</p>"