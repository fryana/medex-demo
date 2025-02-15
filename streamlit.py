# -*- coding: utf-8 -*-
"""Streamlit.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1e_goiA1a0JXi97KzA1ZfB2NP2aLk-XWW
"""

import streamlit as st
import google.generativeai as genai
import base64
from PIL import Image
import io
import os

# Set up Google AI Studio API Key
API_KEY = "AIzaSyCtuCi_7qoxwNC-Em5WG7iKdMXp48oqkNY"  # 🔹 Replace with your Google AI API Key
genai.configure(api_key=API_KEY)

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
    return response, chat_session

def chat_with_gemini(chat_session, prompt):
    response = chat_session.send_message(prompt)
    return response, chat_session

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Uploaded Medical Image", use_column_width=True)

    # Initialize the conversation history list (will be used across different interactions)
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    # Button to generate AI report
    if st.button("📝 Generate Radiology Report"):
        st.write("⏳ Processing... Please wait.")
        
        try:
            # Save file temporarily
            temp_path = os.path.join("temp_uploaded_file.png")  # Change extension accordingly
        
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Initial report generation
            response, gemini_session = gemini_analysis(temp_path)

            # Extract AI-generated report
            ai_report = response.text if response else "⚠️ No report generated."

            # Display the AI Report
            st.subheader("📑 AI-Generated Radiology Report (Gemini-2.0-Flash):")
            st.write(ai_report)

            # Begin the chat interface with Gemini
            st.subheader("💬 Chat with Gemini")
            user_prompt = st.text_input("Ask Gemini anything about the report or image:")

            if user_prompt:
                # Get chat response and update conversation history
                chat_response, gemini_session = chat_with_gemini(
                    gemini_session, user_prompt
                )

                # Show the chat history
                st.write(chat_response)

        except Exception as e:
            st.error(f"❌ Error: {e}. Please start over again")