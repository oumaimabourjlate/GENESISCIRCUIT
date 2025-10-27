import google.generativeai as genai
from PIL import Image
import io

# Configure the Generative AI API (Make sure you have your API key set as an environment variable)
genai.configure(api_key="AIzaSyCwEqNelbtwi7y6_SWz2_QrZ6EqU4rDTvw")

def get_gen_analysis(image_bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes))

        # Basic image validation
        if img.width > 5000 or img.height > 5000:
            return "<h3>Error</h3><p>Image is too large. Please use an image smaller than 5000x5000 pixels.</p>"
        if img.format not in ['JPEG', 'PNG']:
            return "<h3>Error</h3><p>Unsupported image format. Please use JPEG or PNG.</p>"

        # Initialize the Gemini model for vision tasks
        model = genai.GenerativeModel("gemini-1.5-flash")
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

        print("Sending request to Gemini API for image analysis")
        response = model.generate_content([prompt, img])
        print("Gemini API image analysis response received")
        return response.text.replace('\n', '<br>')
    except Exception as e:
        print(f"Gemini API error (image analysis): {str(e)}")
        return f"<h3>Error</h3><p>Could not analyze the image. The API call failed.</p><p><b>Details:</b> {str(e)}</p>"

def get_gen_chat_response(message, history=None):
    try:
        # Initialize the Gemini model for text-only tasks
        chat_model = genai.GenerativeModel("gemini-1.5-flash")
        
        # We can give the chatbot some context about its role
        system_instruction = "You are a helpful assistant specialized in Printed Circuit Boards (PCBs) and quality assurance. Answer questions related to PCB manufacturing, common defects, repair techniques, and electronic components. Be concise and informative."
        
        full_prompt = f"{system_instruction}\n\nUser: {message}"
        
        print(f"Sending request to Gemini API for chat: {message}")
        response = chat_model.generate_content(full_prompt)
        print("Gemini API chat response received")
        return response.text
    except Exception as e:
        print(f"Gemini API error (chat): {str(e)}")
        return f"Sorry, I'm having trouble connecting right now: {str(e)}"
