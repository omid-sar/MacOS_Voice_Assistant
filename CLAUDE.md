# Voice Assistant - Development Guide

## Core Architecture

**Main Components:**
- `AudioRecorder` class - Handles microphone recording with threading
- Keyboard listener - Detects F13 key to stop recording
- OpenAI Whisper integration - Transcribes audio to text
- macOS integration - Notifications, Keychain, Automator

**Flow:** F15 starts → Record audio → F13 stops → Transcribe via OpenAI → Copy to clipboard

## Entry Points

- **`voice_to_text.py`** - Production version, minimal output
- **`voice_to_text_verbose.py`** - Debug version with comprehensive logging to `voice_to_text_verbose.log`
- **`rumps_test.py`** - Menu bar app experiment

## Dependencies

```bash
pip install openai speech_recognition pyperclip pynput keyring
pip install rumps  # For menu bar functionality
```

## Configuration

**API Key Storage:**
```bash
security add-generic-password -a "omidsardari" -s "OpenAI_API_Key" -w "your-api-key"
```

**Keyboard Shortcuts:**
- F15: Start recording (via Automator Quick Action)
- F13: Stop recording

## Development Workflow

**Testing:**
```bash
python voice_to_text.py  # Test production version
python voice_to_text_verbose.py  # Debug with logging
```

**Debugging:**
1. Check `voice_to_text_verbose.log` for detailed error info
2. Verify microphone permissions in System Preferences
3. Test API key retrieval from Keychain
4. Check Automator Quick Action setup

## macOS Integration Requirements

**Permissions:**
- Microphone access for Terminal/Python
- Accessibility access for Automator
- Keychain access for API key storage

**Automator Setup:**
- Quick Action with shell script calling Python script
- Assigned to F15 keyboard shortcut

## Known Limitations

- Hardcoded username in Keychain lookup
- Temporary files created in current directory
- Single API provider dependency (OpenAI only)
- No graceful handling of network failures