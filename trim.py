# from pydub import AudioSegment
# from pydub.silence import detect_nonsilent

# def trim_audio(input_file, output_file, silence_thresh=-40, min_silence_len=1000):
#     # Load the audio file
#     audio = AudioSegment.from_file(input_file)

#     nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

#     if not nonsilent_ranges:
#         print("No significant audio detected.")

#     start_trim = nonsilent_ranges[0][0]
#     end_trim = nonsilent_ranges[-1][1]

#     # Trim and export
#     trimmed_audio = audio[start_trim:end_trim]
#     trimmed_audio.export(output_file, format="mp3")

# # Example usage
# trim_audio("chipopo.mp3", "output.mp3")
"""
Audio Trimming Module

This tool automatically removes silence from the beginning and end of an audio file.
It is useful for cleaning up recordings.
"""

import librosa
import soundfile as sf


def trim_audio(
    input_file: str,
    output_file: str,
    top_db: float = 40,
    ref: float = 0.0
) -> None:
    """
    Trim silence from the beginning and end of an audio file.

    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path to the output trimmed audio file.
        top_db (float): Threshold (in dB) below reference to consider as silence.
                        Default: 40 dB. Higher values = more aggressive trimming.
        ref (float): Reference power. Default: 0.0 (maximum power).

    Returns:
        None

    Raises:
        FileNotFoundError: If input_file does not exist.
        Exception: If audio loading or saving fails.

    Example:
        >>> trim_audio("chipopo.mp3", "output.mp3", top_db=40)
    """
    try:
        # Load the audio file (librosa auto-detects format)
        audio, sr = librosa.load(input_file, sr=None)

        # Trim silence from both ends
        # librosa.effects.trim returns (trimmed_audio, index_array)
        trimmed_audio, _ = librosa.effects.trim(audio, top_db=top_db, ref=ref)

        if len(trimmed_audio) == 0:
            print("⚠️  No significant audio detected after trimming.")
            return

        # Export the trimmed audio
        sf.write(output_file, trimmed_audio, sr)
        print(f"✅ Audio trimmed successfully: {output_file}")

    except FileNotFoundError:
        print(f"❌ Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"❌ Error processing audio: {str(e)}")


# Example usage
if __name__ == "__main__":
    trim_audio("chipopo4.m4a", "output.mp3", top_db=40, ref=0.5)