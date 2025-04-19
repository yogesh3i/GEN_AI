import streamlit as st
import os
import io
from dotenv import load_dotenv
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google API Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the Gemini Model Once (Reuse it)
model = genai.GenerativeModel('gemini-1.5-flash')

## Function to load OpenAI model and get response
def get_gemini_response(input_text, image):
    """Generates a response from the Gemini model based on input text and image."""
    # Convert image to bytes if provided
    image_data = None
    if image:
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")  # Convert image to PNG format
        image_data = {
            "mime_type": "image/png",  # Correct key instead of "type"
            "data": image_bytes.getvalue()  # Get image bytes
        }

    # Prepare input list
    request_data = []
    if input_text:
        request_data.append({"text": input_text})  # Pass input text properly
    if image_data:
        request_data.append({"inline_data": image_data})  # Correct image format

    # Ensure request data is not empty
    if not request_data:
        return "Please provide an input prompt or an image."

    # Get response from model
    response = model.generate_content(request_data)
    return response.text

## Initialize Streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")

# User input field
input_text = st.text_input("Input Prompt:", key="input")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None  # Initialize image as None

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button
if st.button("Tell me about the image"):
    response = get_gemini_response(input_text, image)
    st.subheader("The Response is")
    st.write(response)
