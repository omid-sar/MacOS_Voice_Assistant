import openai
import speech_recognition as sr
import pyperclip
from pynput import keyboard
import time
import os
import keyring
import logging
import sys
import threading
import traceback

os.system('afplay /System/Library/Sounds/Ping.aiff')

# Set up logging

script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, "voice_to_text_verbose.log")
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler(sys.stdout)
    ]
)

def log_environment():
    logging.debug(f"Python version: {sys.version}")
    logging.debug(f"Python executable: {sys.executable}")
    logging.debug(f"Current working directory: {os.getcwd()}")
    logging.debug(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")
    logging.debug(f"Environment variables: {dict(os.environ)}")

log_environment()

def get_api_key():
    logging.debug("Attempting to retrieve API key from keychain...")
    try:
        api_key = keyring.get_password("OpenAI_API_Key", "omidsardari")
        if not api_key:
            raise ValueError("OpenAI API key not found in keychain")
        return api_key
    except Exception as e:
        logging.error(f"Error retrieving API key: {e}")
        raise

try:
    api_key = get_api_key()
    logging.info("API key retrieved successfully.")
    openai.api_key = api_key
except Exception as e:
    logging.error(f"Failed to retrieve OpenAI API key: {e}")
    sys.exit(1)

class AudioRecorder:
    def __init__(self):
        self.recording = False
        self.audio = None

    def record(self):
        logging.debug("Starting audio recording...")
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                logging.info("Recording started. Press 'F13' to stop recording.")
                self.recording = True
                audio = r.listen(source, phrase_time_limit=None)
                self.audio = audio
                logging.debug("Audio recording completed.")
        except Exception as e:
            logging.error(f"Error during audio recording: {e}")
            logging.error(traceback.format_exc())
        finally:
            self.recording = False

def on_press(key, recorder):
    logging.debug(f"Key {key} pressed")
    if key == keyboard.Key.f13:
        logging.info("F13 key pressed. Stopping recording.")
        recorder.recording = False
        return False
    return True

def transcribe_audio(audio):
    logging.info("Starting audio transcription...")
    temp_file = "temp_audio.wav"
    try:
        wav_data = audio.get_wav_data()
        with open(temp_file, "wb") as f:
            f.write(wav_data)
        logging.debug(f"Temporary audio file created: {temp_file}")
        
        with open(temp_file, "rb") as audio_file:
            logging.debug("Sending request to OpenAI API...")
            client = openai.OpenAI(api_key=openai.api_key)
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        transcribed_text = transcript.text
        logging.info(f"Transcription successful. Text: {transcribed_text}")
        return transcribed_text
    
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        logging.error(traceback.format_exc())
        return None
    finally:
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
                logging.debug(f"Temporary audio file removed: {temp_file}")
        except Exception as e:
            logging.error(f"Error removing temporary file: {e}")

def notify_user(message, title="Voice to Text"):
    try:
        os.system(f'osascript -e \'display notification "{message}" with title "{title}"\'')
        logging.debug(f"User notification sent: {message}")
    except Exception as e:
        logging.error(f"Error sending notification: {e}")

def main():
    logging.info("Starting main function...")
    recorder = AudioRecorder()

    recording_thread = threading.Thread(target=recorder.record)
    recording_thread.start()
    logging.debug("Recording thread started.")

    with keyboard.Listener(on_press=lambda key: on_press(key, recorder)) as listener:
        listener.join()
    
    # Wait for the recording to actually stop
    while recorder.recording:
        time.sleep(1)
    
    recording_thread.join()
    logging.debug("Recording thread joined.")

    if not recorder.audio:
        logging.error("Recording failed. No audio data.")
        notify_user("Recording failed.", "Voice to Text")
        return

    logging.info("Recording stopped. Starting transcription...")
    
    transcript = transcribe_audio(recorder.audio)
    
    if transcript:
        pyperclip.copy(transcript)
        logging.info(f"Transcribed text copied to clipboard: {transcript}")
        notify_user("Transcription complete.")
    else:
        logging.error("Transcription failed.")
        notify_user("Transcription failed.", "Voice to Text")

    logging.info("Main function completed.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.critical(f"Unhandled exception in main: {e}")
        logging.critical(traceback.format_exc())
        notify_user("An error occurred. Check the log file.", "Voice to Text Error")