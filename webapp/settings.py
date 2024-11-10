from pathlib import Path
import sys

# Get the absolute path of the current file
FILE = Path(__file__).resolve()
# Get the parent directory of the current file
ROOT = FILE.parent

AUDIO_DIR = ROOT / 'audios'

# Dictionary mapping class names to their corresponding audio files
AUDIOS_DICT = {
    'class1': AUDIO_DIR / 'class1.mp3',
    'class2': AUDIO_DIR / 'class2.mp3',
    'class3': AUDIO_DIR / 'class3.mp3',
}
# Add the root path to the sys.path list if it is not already there
if ROOT not in sys.path:
    sys.path.append(str(ROOT))
# Get the relative path of the root directory with respect to the current working directory
ROOT = ROOT.relative_to(Path.cwd())

# Sources
IMAGE = 'Image'
VIDEO = 'Video'
WEBCAM = 'Webcam'
RTSP = 'RTSP'
YOUTUBE = 'YouTube'

AUDIOS_DICT = {
    'audio_1': AUDIO_DIR / 'class1.mp3',
    'audio_2': AUDIO_DIR / 'class2.mp3',
    'audio_3': AUDIO_DIR / 'class3.mp3',
}
SOURCES_LIST = [IMAGE, VIDEO, WEBCAM, RTSP, YOUTUBE]

# Images config
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'main_page.png'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'main_page_detected_2.jpg'

# Videos config
VIDEO_DIR = ROOT / 'videos'
VIDEOS_DICT = {
    'video_1': VIDEO_DIR / 'bs_pc.mov',
    'video_2': VIDEO_DIR / 'bs_vl.mov',
    'video_3': VIDEO_DIR / 'np_pc.mov',
    'video_4': VIDEO_DIR / 'h (4).mov',
    'video_5': VIDEO_DIR / 'pc.mp4',
    'video_6': VIDEO_DIR / 'tl_pl_vl.mov'
}

# ML Model config
MODEL_DIR = ROOT / 'weights'
DETECTION_MODEL = MODEL_DIR / 'best.pt'
DETECTION_MODEL_2 = MODEL_DIR / 'yolov8n.pt'

# In case of your custome model comment out the line above and
# Place your custom model pt file name at the line below 
# DETECTION_MODEL = MODEL_DIR / 'my_detection_model.pt'

SEGMENTATION_MODEL = MODEL_DIR / 'yolov8n-seg.pt'

# 
WEBCAM_PATH = 0
