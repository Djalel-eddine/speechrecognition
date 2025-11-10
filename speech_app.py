import streamlit as st
import speech_recognition as sr
from io import BytesIO
from datetime import datetime
import os

# --- APP TITLE ---
st.title("🎤 Speech Recognition App (By Djalel)")
st.write("Upload an audio file (.wav or .flac), and the app will transcribe it for you.")

# --- CREATE SPEECH RECOGNIZER ---
recognizer = sr.Recognizer()

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader(
    "Upload an audio file (.wav or .flac)",
    type=["wav", "flac"]
)

if uploaded_file:
    st.info("Processing your audio file...")
    try:
        # Convert uploaded file to BytesIO for SpeechRecognition
        audio_data = BytesIO(uploaded_file.read())

        with sr.AudioFile(audio_data) as source:
            audio = recognizer.record(source)

        # Recognize the audio
        transcription = recognizer.recognize_google(audio, language="en-US")

        st.success("✅ Transcription completed!")
        st.subheader("Transcribed Text:")
        st.write(transcription)

        # Optional: Save the transcription
        save_option = st.checkbox("Save transcription as text file")
        if save_option:
            filename = f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(transcription)
            st.download_button("Download Transcription", filename, file_name=filename)

    except sr.UnknownValueError:
        st.error("⚠️ Could not understand the audio.")
    except sr.RequestError as e:
        st.error(f"API error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# --- FOOTER ---
st.markdown("---")
st.write("Built using Streamlit and SpeechRecognition")
