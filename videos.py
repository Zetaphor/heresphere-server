import os
import re
import yt_dlp
from logger_config import get_logger

logger = get_logger()

root_path = os.path.dirname(os.path.abspath(__file__))

def filename_with_ext(filename, youtube=True):
    path = os.path.join(root_path, 'static', 'videos', 'youtube')
    if not youtube: path = os.path.join(root_path, 'static', 'videos', 'direct')

    for file in os.listdir(path):
        basename, extension = os.path.splitext(file)
        if basename == filename:
            return file

    return None

def download_progress(d):
    if d['status'] == 'downloading':
        logger.info(f"Downloading... {d['_percent_str']} complete at {d['_speed_str']}, ETA {d['_eta_str']}")
    elif d['status'] == 'finished':
        logger.info("Download completed", d['filename'])

def get_video_info(url):
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        vid = info_dict.get('id', None)
        video_title = info_dict.get('title', vid)
        filename = re.sub(r'\W+', '_', video_title)
        return vid, filename

def download_yt(url):
  vid, filename = get_video_info(url)
  filename = f"{vid}___{filename}"
  logger.debug(f"Downloading YouTube video {filename}")

  ydl_opts = {
      'format': '(bv+ba/b)[protocol^=http][protocol!=dash] / (bv*+ba/b)',
      'outtmpl': os.path.join('static', 'videos', 'youtube', filename) + '.%(ext)s',
      'progress_hooks': [download_progress],
  }

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

def download_direct(url):
  _, filename = get_video_info(url)

  logger.debug(f"Downloading direct video {filename}")

  ydl_opts = {
      'outtmpl': os.path.join('static', 'videos', 'direct', filename) + '.%(ext)s',
      'progress_hooks': [download_progress],
  }

  try:
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
          ydl.download([url])
      logger.debug(f"Downloaded direct video {filename}")
  except Exception as e:
      logger.error(f"Error downloading direct video: {e}")
      return None
  return f"/static/videos/direct/{filename_with_ext(filename, False)}"