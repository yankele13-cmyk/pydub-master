import os
os.environ['TRANSFORMERS_ATTN_IMPLEMENTATION'] = 'eager'

from pathlib import Path
import sys
import pandas as pd
import torch
import soundfile as sf
from chatterbox.mtl_tts import ChatterboxMultilingualTTS as cbox


def prepare_cloning_model():
    # Automatically detect the best available device
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    print(f"Using device: {device}")

    return cbox.from_pretrained(device)


def clone_voice(model: cbox, text, file_name, voice_audio_file, output_path):
    voice_audio_file = Path(voice_audio_file)
    wav = model.generate(text, language_id='he', audio_prompt_path=voice_audio_file, exaggeration=2.0)
    path = file_name + '.wav'
    path = path if not output_path else os.path.join(output_path, path)
    sf.write(path, wav.cpu().numpy().squeeze(), model.sr)
    print(f'Generated "{text}" with the cloned voice "{voice_audio_file.stem}" to {path}')


def main(csv, voice_file, output_path):
    items = pd.read_csv(csv, header=None)
    model = prepare_cloning_model()
    for row in items.itertuples(index=False):
        text, file_name = row
        clone_voice(model, text, file_name, voice_file, output_path)


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print('No items specified.')
    else:
        main(sys.argv[1], '29_1.wav', sys.argv[2] if len(sys.argv) > 2 else '')