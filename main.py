from flask import Flask, render_template, request, jsonify
import os
import logging
import sys
import datetime
import threading
import network
from logger_config import get_logger
from videos import download_yt, get_stream, download_direct, is_youtube_url, get_static_directory
import api
from ws_server import start_websocket_server_thread

logger = get_logger()

DEBUG = 1
UI_PORT = 5000
WS_PORT = 6789

log_level = 'DEBUG' if DEBUG else 'INFO'
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file_path = f"logs/log_{timestamp}.log"
logger.add(log_file_path, rotation="1 week", level=log_level)

# Hide Flask debug banner
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

static_folder_path = get_static_directory()

logger.debug(f"Static Folder Path: {static_folder_path}")

app = Flask(__name__, static_folder=static_folder_path)
app.logger.setLevel(logging.WARNING)

all_ips = network.get_all_ips()
lan_ip = network.get_lan_ip()

def download_progress(d):
    if d['status'] == 'downloading':
        logger.info(f"Downloading... {d['_percent_str']} complete at {d['_speed_str']}, ETA {d['_eta_str']}")
    elif d['status'] == 'finished':
        logger.info("Download completed", d['filename'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/connection_test')
def connection_test():
    return jsonify({"success": True})

@app.route('/api/list')
def get_files():
    return jsonify(api.list_files())

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url:
        logger.error("No direct video URL provided in the request")
        return jsonify({"success": False, "error": "No URL provided"}), 400

    video_url = None

    if is_youtube_url(url):
        video_url = download_yt(url, download_progress)
    else:
        video_url = download_direct(url, download_progress)

    if video_url is None:
        return jsonify({"success": False, "error": "Failed to download video"}), 500
    return jsonify({"success": True, "url": video_url, "videoUrl": f"http://{lan_ip}:{UI_PORT}{video_url}"})

@app.route('/stream', methods=['POST'])
def resolve_yt():
    data = request.get_json()
    url = data.get("url")

    if not url:
        logger.error("No URL provided in the request")
        return jsonify({"success": False, "error": "No URL provided"}), 400

    video_url, audio_url = get_stream(url)
    if video_url is None and audio_url is None:
        return jsonify({"success": False, "error": "Failed to retrieve video and audio streams"}), 500
    return jsonify({"success": True, "videoUrl": video_url, "audioUrl": audio_url})

def start_server():
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')

    flask_thread = threading.Thread(target=lambda: app.run(debug=DEBUG, port=UI_PORT, use_reloader=False, host='0.0.0.0'))
    flask_thread.start()

    ws_thread = threading.Thread(target=start_websocket_server_thread, args=(WS_PORT,))
    ws_thread.start()

    tab = "\t"
    tabnewline = "\n\t"
    logger.info(f"""
██   ██ ███████ ███████ ███████ ██████  ██    ██ ███████ ██████
██   ██ ██      ██      ██      ██   ██ ██    ██ ██      ██   ██
███████ ███████ ███████ █████   ██████  ██    ██ █████   ██████
██   ██      ██      ██ ██      ██   ██  ██  ██  ██      ██   ██
██   ██ ███████ ███████ ███████ ██   ██   ████   ███████ ██   ██

┌───────────────────────────────────────────────────────────────┐
│                        STEAM USERS                            │
└───────────────────────────────────────────────────────────────┘
  SteamVR users need to connect via the localhost address.
  Your localhost address is:
{tab}http://localhost:{UI_PORT}/

┌───────────────────────────────────────────────────────────────┐
│                        QUEST USERS                            │
└───────────────────────────────────────────────────────────────┘
  Quest users will need to connect via the LAN IP.
  I think your LAN IP is {lan_ip}, so your LAN address would be:
{tab}http://{lan_ip}:{UI_PORT}/

  Here is a list of all the other network interfaces on this machine:
{tabnewline}{tabnewline.join([f"{interface}: http://{', '.join(ips)}:{UI_PORT}/" for interface, ips in all_ips.items() if interface != "lo"])}
    """)

if __name__ == '__main__':
    start_server()

