3 files python languages 
1- tts hebrew -> voice clone('TTS_chatterbox.py') -> 
2- audio trimming -> (trim.py)
3- to take an audio file and to add a musical(audio file) in backround 

the descritpion of the flows :
# Audio Processing Toolkit

This project is a collection of tools to create and edit audio files. It has a simple user interface to make the tools easy to use.

### Core Features

1.  **Hebrew Text-to-Speech (TTS) with Voice Cloning** (`TTS_chatterbox.py`)
    *   This tool can read Hebrew text and turn it into speech.
    *   It uses "voice cloning" to copy a voice from a sample audio file. This makes the new speech sound like a specific person.

2.  **Audio Trimming** (`trim.py`)
    *   This tool automatically removes silence from the beginning and end of an audio file.
    *   It is useful for cleaning up recordings.

3.  **Add Background Music** (`merge.py`)
    *   This feature is planned for the future.
    *   It will let you take an audio file (like a voice recording) and add a music file to the background.

### Requirements

To run this project, you need to install several libraries, including `torch`, `torchaudio`, and `ffmpeg`.



requierements :
torch
torchaudio
torchcodec
librosa
safetensors
transformers==4.46.3
s3tokenizer
conformer
diffusers
ffmpeg



