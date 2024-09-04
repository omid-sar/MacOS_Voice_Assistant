import openai
import speech_recognition as sr
import pyperclip
from pynput import keyboard
import time
import os
import keyring
import threading

os.system('afplay /System/Library/Sounds/Ping.aiff')

def get_api_key():
    api_key = keyring.get_password("OpenAI_API_Key", "omidsardari")
    if not api_key:
        raise ValueError("OpenAI API key not found in keychain")
    return api_key

openai.api_key = get_api_key()

class AudioRecorder:
    def __init__(self):
        self.recording = False
        self.audio = None

    def record(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Recording started. Press 'F13' to stop recording.")
            self.recording = True
            self.audio = r.listen(source, phrase_time_limit=None)
        self.recording = False

def on_press(key, recorder):
    if key == keyboard.Key.f13:
        recorder.recording = False
        return False
    return True

def transcribe_audio(audio):
    temp_file = "temp_audio.wav"
    with open(temp_file, "wb") as f:
        f.write(audio.get_wav_data())
    
    with open(temp_file, "rb") as audio_file:
        client = openai.OpenAI(api_key=openai.api_key)
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    
    os.remove(temp_file)
    return transcript.text

def notify_user(message, title="Voice to Text"):
    os.system(f'osascript -e \'display notification "{message}" with title "{title}"\'')

def main():
    recorder = AudioRecorder()
    recording_thread = threading.Thread(target=recorder.record)
    recording_thread.start()

    with keyboard.Listener(on_press=lambda key: on_press(key, recorder)) as listener:
        listener.join()
    
    while recorder.recording:
        time.sleep(0.1)
    
    recording_thread.join()

    if not recorder.audio:
        notify_user("Recording failed.", "Voice to Text")
        return

    transcript = transcribe_audio(recorder.audio)
    
    if transcript:
        pyperclip.copy(transcript)
        notify_user("Transcription complete.")
    else:
        notify_user("Transcription failed.", "Voice to Text")

if __name__ == "__main__":
    main()