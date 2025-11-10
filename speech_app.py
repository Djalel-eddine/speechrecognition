import streamlit as st
from datetime import datetime
import whisper
import os

st.title("Audio Transcription App (Whisper)")

# Upload audio file
uploaded_file = st.file_uploader("Upload audio file (mp3, wav, mp4, etc.)", type=["mp3", "wav", "mp4", "m4a", "ogg"])

# Language selection
language = st.selectbox(
    "Select the language of the audio:",
    ["auto", "en", "fr", "es", "ar", "de", "it"]  # add more languages as needed
)

# Save transcription option
save_file = st.checkbox("Save transcription to a text file")

# Whisper model selection
model_size = st.selectbox(
    "Select Whisper model size:",
    ["tiny", "base", "small", "medium", "large"]
)

# Pause/resume controls
pause = st.button("Pause")
resume = st.button("Resume")

# Global state for pause/resume
if "paused" not in st.session_state:
    st.session_state.paused = False

if pause:
    st.session_state.paused = True
if resume:
    st.session_state.paused = False


def transcribe_audio(file_path, model_name="small", lang="auto"):
    try:
        model = whisper.load_model(model_name)
        st.info("Transcribing audio... This may take a while depending on the file size and model.")

        # Split long files into segments if needed
        result = model.transcribe(file_path, language=lang)
        return result["text"]
    except Exception as e:
        st.error(f"Error during transcription: {str(e)}")
        return None


if uploaded_file:
    # Save uploaded file temporarily
    temp_dir = "temp_audio"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if not st.session_state.paused:
        transcription = transcribe_audio(temp_file_path, model_size, language)
        if transcription:
            st.subheader("Transcribed Text:")
            st.text_area("Your transcription:", transcription, height=300)

            if save_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"transcription_{timestamp}.txt"
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write(transcription)
                st.success(f"Transcription saved as {file_name}")
