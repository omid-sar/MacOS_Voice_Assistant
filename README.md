
# Voice-to-Text Transcription Tool

## Overview

This tool allows users to transcribe voice input into text using OpenAI's Whisper model. The process is triggered by a keyboard shortcut set up in macOS Automator, which starts and stops the recording based on user-defined keys.

## Features

- **Automated Transcription**: Converts voice input to text using OpenAI's Whisper model.
- **Keyboard Shortcuts**: Initiates and stops recording through user-defined keyboard shortcuts.
- **Clipboard Integration**: Automatically copies the transcribed text to the clipboard.
- **Verbose Logging**: Provides detailed logs for debugging if the script encounters any issues.

## Project Summary

1. **Start Recording**: The recording starts when a specific key (e.g., `F14`) is pressed.
2. **Stop Recording**: Recording stops when another key (e.g., `F13`) is pressed.
3. **Transcription**: The recorded audio is sent to OpenAI's Whisper API for transcription.
4. **Clipboard Integration**: The transcribed text is copied to the clipboard automatically.
5. **Verbose Mode**: If debugging is needed, the script can run in a verbose mode, generating detailed logs.

## Installation and Setup

### 1. Prerequisites

- **macOS**: Required for Automator functionality.
- **Python 3.7+**: Ensure Python is installed.
- **OpenAI API Key**: Sign up at [OpenAI](https://beta.openai.com/signup/) and generate an API key.

### 2. Install Required Python Libraries

Install the necessary libraries using the following command:

```bash
pip install openai speech_recognition pyperclip pynput keyring
```

### 3. Store Your OpenAI API Key Securely

Store your OpenAI API key securely in macOS's Keychain:

```bash
security add-generic-password -a "your-username" -s "OpenAI_API_Key" -w "your-actual-api-key"
```

Replace `"your-username"` with your macOS username and `"your-actual-api-key"` with your actual API key from OpenAI.

### 4. Python Script Setup

Ensure your Python script (`voice_to_text.py`) is configured correctly to:

- Start recording when `F14` is pressed.
- Stop recording when `F13` is pressed.
- Transcribe the recorded audio using OpenAI's Whisper API.
- Copy the transcribed text to the clipboard.
- Notify the user upon transcription completion.

### 5. Setting Up macOS Automator

To automate the process, set up a Quick Action in Automator:

1. Open **Automator** on your Mac.
2. Create a new "Quick Action".
3. Configure the Quick Action:
   - Set "Workflow receives" to "no input".
   - Select "any application" for "in".
   - Add a "Run Shell Script" action:
     - Set "Shell" to `/bin/zsh`.
     - Set "Pass input" to `stdin`.
     - Enter the following script:

     ```zsh
     #!/bin/zsh
     /path/to/your/python /path/to/your/voice_to_text.py
     ```

   Replace `/path/to/your/python` with the path to your Python executable and `/path/to/your/voice_to_text.py` with the actual path where you have placed your Python script from the repository.

### 6. Permissions Configuration

To ensure the application runs smoothly, grant the following permissions:

- **Microphone Access**: Allow the Terminal or Python application to access the microphone. Go to **System Preferences** > **Security & Privacy** > **Privacy** > **Microphone**.
- **Accessibility Access**: Go to **System Preferences** > **Security & Privacy** > **Privacy** > **Accessibility** and add Automator and Terminal (or your preferred shell application).

### 7. Running the Application

1. Press `F14` (or your configured shortcut) to start recording.
2. Speak clearly into your microphone.
3. Press `F13` (or your configured shortcut) to stop recording.
4. The transcribed text will be copied to your clipboard, and a notification will appear.

### 8. Debugging with Verbose Logging

If the script does not work as expected, switch to the verbose mode for detailed logs:

1. In Automator, modify the script path from `voice_to_text.py` to `voice_to_text_verbose.py`.
2. The verbose script will create a log file (`voice_to_text_verbose.log`) in the same directory where you placed your Python script, providing detailed information on any issues encountered.

## Notes

- The OpenAI API key storage in Keychain uses placeholder values. Replace "your-username" with your actual macOS username.
- The project assumes basic familiarity with macOS and Python scripting.
- The provided screenshot offers a visual reference for setting up the Quick Action in Automator.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
