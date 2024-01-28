import os
import time
import platform
from logger_config import get_logger
from moviepy.editor import VideoFileClip

logger = get_logger()

def get_video_info(filename):
    try:
        clip_info = ('Unknown', 'Unknown')
        with VideoFileClip(filename) as clip:
            resolution = f"{clip.size[0]}x{clip.size[1]}"
            fps = clip.fps
            duration = clip.duration
        return (resolution, fps, duration)
    except OSError as e:
        logger.error(f"Error getting video info: {e}")
        return clip_info

def get_file_size_formatted(filename):
    size_bytes = os.path.getsize(filename)

    size_mb = size_bytes / (1024 * 1024)

    if size_mb < 1024:
        return f"{size_mb:.2f} MB"
    else:
        size_gb = size_mb / 1024
        return f"{size_gb:.2f} GB"

def format_duration(duration):
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def get_creation_date(filename):
    if platform.system() == 'Windows':
        creation_time = os.path.getctime(filename)
    else:
        creation_time = os.path.getmtime(filename)

    readable_time = time.ctime(creation_time)
    return readable_time

def parse_youtube_filename(filename):
    parts = filename.split('___')
    logger.debug(parts)

    id_part = parts[0]
    title_part = parts[1]

    return id_part, title_part

def list_files():
    extracted_details = []

    for root, dirs, files in os.walk('./static/videos'):
        for filename in files:
            resolution, fps, duration = get_video_info(os.path.join(root, filename))
            if filename.count('___') == 1:
                id, title = parse_youtube_filename(filename)
                extracted_details.append({
                    'yt_id': id,
                    'title': title,
                    'fps': fps,
                    'resolution': resolution,
                    'duration': format_duration(duration),
                    'filename': f"/static/videos/youtube/{filename}",
                    'created': get_creation_date(os.path.join(root, filename)),
                    'filesize': get_file_size_formatted(os.path.join(root, filename))
                })
            else:
                extracted_details.append({
                    'yt_id': None,
                    'title': os.path.splitext(filename)[0],
                    'fps': fps,
                    'resolution': resolution,
                    'duration': format_duration(duration),
                    'filename': f"/static/videos/direct/{filename}",
                    'created': get_creation_date(os.path.join(root, filename)),
                    'filesize': get_file_size_formatted(os.path.join(root, filename))
                })

    return extracted_details