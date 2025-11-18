"""
Audio Merging Module with Ducking

This tool merges a voice audio file with a background music file.
It automatically lowers the music volume when speech is detected (audio ducking)
to ensure the voice remains clear.
"""

import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def merge_with_ducking(
    voice_path: str,
    music_path: str,
    output_path: str,
    duck_amount_db: float = 15.0,
    silence_thresh_db: int = -40,
    min_silence_len_ms: int = 500,
    repeat_music: bool = False
) -> None:
    """
    Merges a voice track with background music, applying audio ducking.

    Args:
        voice_path (str): Path to the voice audio file.
        music_path (str): Path to the background music file.
        output_path (str): Path to save the final mixed audio file.
        duck_amount_db (float): How many dB to lower the music volume during speech.
                                A higher positive value means more ducking. Default is 15.0.
        silence_thresh_db (int): Threshold below which audio is considered silence.
        min_silence_len_ms (int): Minimum duration of silence to be considered a pause.
    
    Returns:
        None
    
    Raises:
        FileNotFoundError: If voice or music file does not exist.
    """
    try:
        print("🎙️  Loading voice and music files...")
        voice = AudioSegment.from_file(voice_path)
        music = AudioSegment.from_file(music_path)

        # 1. Ensure music is long enough for the voice track
        if repeat_music and len(music) < len(voice):
            print(" Music is shorter than voice, looping music...")
            # Calculate how many times to repeat the music
            repeat_factor = -(-len(voice) // len(music)) # Ceiling division
            music = music * repeat_factor
        
        # Trim music to be the exact length of the voice
        music = music[:len(voice)]

        # 2. Find where the voice is speaking
        print("🤫 Detecting speech segments in the voice track...")
        nonsilent_ranges = detect_nonsilent(
            voice,
            min_silence_len=min_silence_len_ms,
            silence_thresh=silence_thresh_db
        )

        if not nonsilent_ranges:
            print("⚠️ No speech detected in the voice file. Performing a simple merge.")
            final_audio = voice.overlay(music)
            final_audio.export(output_path, format="mp3")
            print(f"✅ Simple merge completed: {output_path}")
            return

        # 3. Apply ducking to the music track
        print(f"🦆 Applying ducking of {duck_amount_db} dB to music...")
        ducked_music = music
        for start, end in nonsilent_ranges:
            music_segment = ducked_music[start:end]
            ducked_segment = music_segment - duck_amount_db
            ducked_music = ducked_music[:start].append(ducked_segment).append(ducked_music[end:])
        
        # 4. Overlay the original voice on the ducked music
        print("🎚️  Mixing final audio...")
        final_audio = voice.overlay(ducked_music)

        # 5. Export the result
        final_audio.export(output_path, format="mp3")
        print(f"✅ Audio merged with ducking successfully: {output_path}")

    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


# --- Example Usage ---
if __name__ == "__main__":
    # IMPORTANT: Replace these with your actual file paths for testing
    voice_file = "chipopo.mp3"  # A voice recording (e.g., the output of trim.py)
    music_file = "music.mp3" # A music file
    output_file = "final_mix.mp3"
    
    # Check if example files exist before running
    if os.path.exists(voice_file) and os.path.exists(music_file):
        merge_with_ducking(voice_file, music_file, output_file, duck_amount_db=20)
    else:
        print("------------------------------------------------------------------")
        print("⚠️  To test this script, please provide two audio files:")
        print(f"   1. A voice file named '{voice_file}'")
        print(f"   2. A music file named '{music_file}'")
        print("   Place them in the same directory as this script.")
        print("------------------------------------------------------------------")