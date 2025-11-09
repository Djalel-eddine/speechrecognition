import speech_recognition as sr
import streamlit as st
import os
from datetime import datetime

st.title("🎙️ Enhanced Speech Recognition App (by Djalel)")

# --- Select API
api_option = st.selectbox(
    "Choose the Speech Recognition API:",
    ["Google Speech Recognition", "Sphinx (Offline)", "Deepgram (coming soon)"]
)

# --- Select Language
language = st.selectbox(
    "Select the language:",
    [
        ("English (US)", "en-US"),
        ("French (FR)", "fr-FR"),
        ("Arabic (DZ)", "ar-DZ"),
        ("Spanish (ES)", "es-ES")
    ],
    format_func=lambda x: x[0]
)[1]

# --- Buttons for control
col1, col2, col3 = st.columns(3)
start_button = col1.button("🎤 Start Recording")
pause_button = col2.button("⏸ Pause")
resume_button = col3.button("▶ Resume")

r = sr.Recognizer()
mic = sr.Microphone()
pause_flag = False

# --- Transcription logic
def transcribe_speech(api_choice, lang):
    global pause_flag
    try:
        with mic as source:
            st.info("Listening... Speak now 🎧")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
            st.success("Audio captured, transcribing...")

        if pause_flag:
            st.warning("Recognition paused.")
            return ""

        if api_choice == "Google Speech Recognition":
            text = r.recognize_google(audio, language=lang)
        elif api_choice == "Sphinx (Offline)":
            text = r.recognize_sphinx(audio, language=lang)
        else:
            text = "[API not yet implemented]"
        return text

    except sr.UnknownValueError:
        st.error("🤔 Sorry, I couldn’t understand what you said.")
    except sr.RequestError as e:
        st.error(f"⚠️ API Error: {e}")
    except sr.WaitTimeoutError:
        st.error("⏱ No speech detected within the time limit.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

    return ""

# --- Pause / Resume Logic
if pause_button:
    pause_flag = True
    st.warning("Recognition paused.")

if resume_button:
    pause_flag = False
    st.success("Recognition resumed.")

# --- Start Transcription
if start_button:
    transcript = transcribe_speech(api_option, language)
    if transcript:
        st.subheader("📝 Transcribed Text:")
        st.write(transcript)

        # --- Save to File
        if st.button("💾 Save to File"):
            if not os.path.exists("transcriptions"):
                os.makedirs("transcriptions")
            filename = f"transcriptions/transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(transcript)
            st.success(f"✅ Transcription saved to {filename}")
