import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import os
from datetime import datetime

# ----------------------
# App Title
# ----------------------
st.title("Speech Recognition App")
st.write("Upload an audio file and transcribe it into text. Supported formats: mp3, wav, mp4, m4a, etc.")

# ----------------------
# File uploader
# ----------------------
uploaded_file = st.file_uploader("Upload your audio file", type=["mp3", "wav", "mp4", "m4a"])

# ----------------------
# Select language
# ----------------------
language = st.selectbox(
    "Choose the language of the audio file",
    options=["en-US", "fr-FR", "es-ES", "ar-SA"]  # add more as needed
)

# ----------------------
# Select API
# ----------------------
api_choice = st.selectbox(
    "Select Speech Recognition API",
    options=["Google Speech Recognition", "Sphinx (offline)"]
)

# ----------------------
# Initialize Recognizer
# ----------------------
recognizer = sr.Recognizer()

# ----------------------
# Transcribe function
# ----------------------
def transcribe_speech(audio_file, language="en-US", api="Google Speech Recognition"):
    try:
        # Convert non-wav to wav
        if not audio_file.name.endswith(".wav"):
            audio = AudioSegment.from_file(audio_file)
            wav_path = f"temp_{datetime.now().strftime('%Y%m%d%H%M%S')}.wav"
            audio.export(wav_path, format="wav")
        else:
            wav_path = audio_file.name
            with open(wav_path, "wb") as f:
                f.write(audio_file.read())

        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)

        if api == "Google Speech Recognition":
            text = recognizer.recognize_google(audio_data, language=language)
        elif api == "Sphinx (offline)":
            text = recognizer.recognize_sphinx(audio_data, language=language)
        else:
            text = "Selected API is not supported."

        # Clean up temporary file
        if wav_path.startswith("temp_"):
            os.remove(wav_path)

        return text

    except sr.UnknownValueError:
        return "Speech Recognition could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results from the API; {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# ----------------------
# Pause/Resume simulation
# ----------------------
if uploaded_file:
    st.session_state["paused"] = False

    if "paused" not in st.session_state:
        st.session_state.paused = False

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Pause"):
            st.session_state.paused = True
    with col2:
        if st.button("Resume"):
            st.session_state.paused = False

    if st.session_state.paused:
        st.warning("Transcription is paused.")
    else:
        st.info("Transcription in progress...")
        transcription = transcribe_speech(uploaded_file, language=language, api=api_choice)
        st.text_area("Transcribed Text", transcription, height=200)

        # Option to save transcription
        if st.button("Save Transcription"):
            save_path = f"transcription_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(transcription)
            st.success(f"Transcription saved as {save_path}")
            st.download_button("Download Transcription", data=transcription, file_name=save_path)
