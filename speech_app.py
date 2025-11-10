import streamlit as st
from pydub import AudioSegment
import whisper
import os
from datetime import datetime

# --- App Title ---
st.title("Speech-to-Text App (By Djalel)")
st.write("Upload an audio file, select options, and get transcription.")

# --- Sidebar Options ---
st.sidebar.header("Settings")

# Model selection
model_options = ["tiny", "base", "small", "medium", "large"]
selected_model = st.sidebar.selectbox("Select Whisper Model", model_options, index=2)

# Language selection
language_options = ["auto", "en", "fr", "ar", "es", "de"]
selected_language = st.sidebar.selectbox("Select Audio Language", language_options, index=0)

# Upload audio file
uploaded_file = st.file_uploader("Upload Audio File (mp3, wav, mp4)", type=["mp3", "wav", "mp4"])

# Pause/Resume controls
if 'paused' not in st.session_state:
    st.session_state.paused = False


def toggle_pause():
    st.session_state.paused = not st.session_state.paused


st.sidebar.button("Pause/Resume Transcription", on_click=toggle_pause)


# --- Helper Functions ---
def save_transcription(text, filename="transcription.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    st.success(f"Transcription saved to {filename}")


def transcribe_audio(file_path, model_name, language):
    try:
        model = whisper.load_model(model_name)
        st.info("Transcribing audio... This may take a few moments.")
        result = model.transcribe(file_path, language=language)
        return result["text"]
    except Exception as e:
        st.error(f"Error during transcription: {str(e)}")
        return None


# --- Main ---
if uploaded_file:
    try:
        # Convert uploaded file to wav (if needed)
        file_extension = uploaded_file.name.split('.')[-1]
        temp_file_path = f"temp_uploaded.{file_extension}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if file_extension != "wav":
            audio = AudioSegment.from_file(temp_file_path)
            temp_wav_path = "temp_uploaded.wav"
            audio.export(temp_wav_path, format="wav")
            file_path = temp_wav_path
        else:
            file_path = temp_file_path

        # Transcription
        if not st.session_state.paused:
            transcription = transcribe_audio(file_path, selected_model, selected_language)
            if transcription:
                st.text_area("Transcribed Text", transcription, height=300)
                st.download_button("Download Transcription", transcription, file_name="transcription.txt")

    except Exception as e:
        st.error(f"Failed to process audio file: {str(e)}")
