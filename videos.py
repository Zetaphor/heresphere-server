import os
import re
import yt_dlp
from logger_config import get_logger
from dotenv import load_dotenv

logger = get_logger()
load_dotenv()
root_path = os.path.dirname(os.path.abspath(__file__))

is_windows = os.name == 'nt' # Anguish

def get_static_directory():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    if os.name == 'nt' and '_internal' in base_dir:
        # Fix path for Windows Pyinstaller directory
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # Construct the path to the 'static' folder
    static_folder_path = os.path.join(base_dir, 'static')
    return static_folder_path

# Set the path to the static ffmpeg executable for Windows
if is_windows:
    ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.getenv('FFMPEG_PATH'), 'ffmpeg.exe')
else:
    ffmpeg_path = None

def filename_with_ext(filename, youtube=True):
    path = os.path.join(root_path, 'static', 'videos', 'youtube')
    if not youtube: path = os.path.join(root_path, 'static', 'videos', 'direct')

    # Fix path for Windows Pyinstaller directory
    if is_windows and '_internal' in root_path:
        path = os.path.join(os.path.dirname(root_path), 'static', 'videos', 'youtube')
        if not youtube: os.path.join(os.path.dirname(root_path), 'static', 'videos', 'direct')

    for file in os.listdir(path):
        basename, _ = os.path.splitext(file)
        if basename == filename:
            return file

    return None

def is_youtube_url(url):
    """Check if the provided URL is a valid YouTube URL."""
    pattern = r'^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$'
    return bool(re.match(pattern, url))

def get_video_info(url):
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        vid = info_dict.get('id', None)
        video_title = info_dict.get('title', vid)
        filename = re.sub(r'\W+', '_', video_title)
        return vid, filename

def download_yt(url, progress_function):
  vid, filename = get_video_info(url)
  filename = f"{vid}___{filename}"
  logger.debug(f"Downloading YouTube video {filename}")

  ydl_opts = {
      'format': '(bv+ba/b)[protocol^=http][protocol!=dash] / (bv*+ba/b)',
      'outtmpl': os.path.join('static', 'videos', 'youtube', filename) + '.%(ext)s',
      'progress_hooks': [progress_function],
  }

  if is_windows:
      logger.debug(f"Windows detected, using ffmpeg binary from {ffmpeg_path}")
      ydl_opts['ffmpeg_location'] = ffmpeg_path    

  try:
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          ydl.download([url])
      logger.debug(f"Downloaded YouTube video {filename}")
  except Exception as e:
      logger.error(f"Error downloading YouTube video: {e}")
      return None
  return f"/static/videos/youtube/{filename_with_ext(filename)}"

def get_yt_streams(url):
    ydl_opts = {
        'format': '(bv+ba/b)[protocol^=http][protocol!=dash] / (bv*+ba/b)',
        'quiet': True
    }

    if is_windows:
        logger.debug(f"Windows detected, using ffmpeg binary from {ffmpeg_path}")
        ydl_opts['ffmpeg_location'] = ffmpeg_path    

    try:
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [info])
        video_url = next((f['url'] for f in formats if f.get('vcodec') != 'none'), None)
        audio_url = next((f['url'] for f in formats if f.get('acodec') != 'none'), None)

        if not video_url or not audio_url:
            raise Exception("Could not retrieve both video and audio URLs")

        return video_url, audio_url
    except Exception as e:
      logger.error(f"Error retrieving video and audio streams: {e}")
      return None, None

def download_direct(url, progress_function):
  _, filename = get_video_info(url)

  logger.debug(f"Downloading direct video {filename}")

  ydl_opts = {
      'outtmpl': os.path.join('static', 'videos', 'direct', filename) + '.%(ext)s',
      'progress_hooks': [progress_function],
  }

  if is_windows:
      logger.debug(f"Windows detected, using ffmpeg binary from {ffmpeg_path}")
      ydl_opts['ffmpeg_location'] = ffmpeg_path

  try:
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          ydl.download([url])
      logger.debug(f"Downloaded direct video {filename}")
  except Exception as e:
      logger.error(f"Error downloading direct video: {e}")
      return None
  return f"/static/videos/direct/{filename_with_ext(filename, False)}"