from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def trim_audio(input_file, output_file, silence_thresh=-40, min_silence_len=1000):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

    if not nonsilent_ranges:
        print("No significant audio detected.")

    start_trim = nonsilent_ranges[0][0]
    end_trim = nonsilent_ranges[-1][1]

    # Trim and export
    trimmed_audio = audio[start_trim:end_trim]
    trimmed_audio.export(output_file, format="mp3")

# Example usage
trim_audio("chipopo.mp3", "output.mp3", -35, 800)  # trims from 10s to 20s