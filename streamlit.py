# -*- coding: utf-8 -*-
"""Streamlit.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1e_goiA1a0JXi97KzA1ZfB2NP2aLk-XWW
"""

import streamlit as st
import google.generativeai as genai
import anthropic  # For Claude AI
import openai  # For ChatGPT
import base64
from PIL import Image
import io

# Set up Google AI Studio API Key
Gemini_API_KEY = "AIzaSyCtuCi_7qoxwNC-Em5WG7iKdMXp48oqkNY"  # 🔹 Replace with your Google AI API Key
CLAUDE_API_KEY = ""
GPT_API_KEY = ""

genai.configure(api_key=Gemini_API_KEY)

# Streamlit UI Title
st.title("🩺 AI-Powered Radiology Report Generator")
st.write("📷 Upload a medical image, and AI will generate a detailed radiology report.")

# Upload Image
uploaded_file = st.file_uploader("📂 Choose a medical image...", type=["png", "jpg", "jpeg"])

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini.

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# Function to encode image to base64 for AI processing
def encode_image(image):
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    return base64.b64encode(image_bytes.getvalue()).decode("utf-8")

def gemini_analysis(file_path):
    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
    )

    files = [
        upload_to_gemini(file_path, mime_type="image/png"),
    ]

    chat_session = model.start_chat(
        history=[
            {
            "role": "user",
            "parts": [
                files[0],
            ],
            },
        ]
        )

    response = chat_session.send_message("please help me analysis the xray")

    # return {"message": f"Gemini processed {file_path}",
    #         "report": response.text}
    return response

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Uploaded Medical Image", use_column_width=True)

    # # Convert image to base64
    # image_base64 = encode_image(image)

    # Button to generate AI report
    if st.button("📝 Generate Radiology Report"):
        st.write("⏳ Processing... Please wait.")
    
    # AI Model Selection Buttons
    st.write("### 🔍 Select an AI Model:")
    col1, col2, col3 = st.columns(3)

    if col1.button("🤖 Use Gemini AI"):
        st.write("⏳ Processing with Gemini AI...")
        report = generate_gemini_report(image_base64)
        st.subheader("📑 AI-Generated Radiology Report:")
        st.write(report)

    if col2.button("🧠 Use Claude AI"):
        st.write("⏳ Processing with Claude AI...")
        report = generate_claude_report(image_base64)
        st.subheader("📑 AI-Generated Radiology Report:")
        st.write(report)

    if col3.button("💡 Use GPT AI"):
        st.write("⏳ Processing with GPT AI...")
        report = generate_gpt_report(image_base64)
        st.subheader("📑 AI-Generated Radiology Report:")
        st.write(report)


        try:
            # Save file temporarily
            temp_path = os.path.join("temp_uploaded_file.png")  # Change extension accordingly
        
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            response = gemini_analysis(temp_path)
            
            # # Send request to Google Gemini AI
            # model = genai.GenerativeModel("gemini-pro-vision")
            # response = model.generate_content(
            #     ["Analyze this medical image and generate a detailed radiology report."],
            #     [image_base64]
            # )

            # Extract AI-generated report
            ai_report = response.text if response else "⚠️ No report generated."

            # Display the AI Report
            st.subheader("📑 AI-Generated Radiology Report:")
            st.write(ai_report)

        except Exception as e:
            st.error(f"❌ Error: {e}")

