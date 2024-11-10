from pathlib import Path
import sys

FILE = Path(__file__).resolve()
# Get the parent directory of the current file
ROOT = FILE.parent
if ROOT not in sys.path:
    sys.path.append(str(ROOT))
# Get the relative path of the root directory with respect to the current working directory
ROOT = ROOT.relative_to(Path.cwd())

# Verify paths
audio_files = [
    Path(ROOT/'audios/class1.mp3'),
    Path(ROOT/'audios/class2.mp3'),
    Path(ROOT/'audios/class3.mp3')
]

for audio_file in audio_files:
    if audio_file.exists():
        print(f"{audio_file} exists.")
    else:
        print(f"{audio_file} does not exist.")