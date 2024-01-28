from flask import Flask, render_template, request, jsonify
import asyncio
import websockets
import os
import logging
import sys
import datetime
import threading
import network
from dotenv import load_dotenv
from logger_config import get_logger
from videos import download_yt, get_yt_streams

logger = get_logger()
load_dotenv()

DEBUG = bool(int(os.getenv('DEBUG')))
UI_PORT = int(os.getenv('UI_PORT'))
WS_PORT = int(os.getenv('WS_PORT'))

log_level = 'DEBUG' if DEBUG else 'INFO'
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file_path = f"logs/log_{timestamp}.log"
logger.add(log_file_path, rotation="1 week", level=log_level)

# Hide Flask debug banner
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app = Flask(__name__)
app.logger.setLevel(logging.WARNING)

all_ips = network.get_all_ips()
lan_ip = network.get_lan_ip()

connected_clients = set()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url:
        logger.error("No direct video URL provided in the request")
        return jsonify({"success": False, "error": "No URL provided"}), 400

    video_url = download_yt(url)
    if video_url is None:
        return jsonify({"success": False, "error": "Failed to download video"}), 500
    return jsonify({"success": True, "url": video_url, "full_url": f"http://{lan_ip}:{UI_PORT}{video_url}"})

@app.route('/youtube', methods=['POST'])
def resolve_yt():
    data = request.get_json()
    url = data.get("url")
    separate_streams = data.get("separate_streams", False)

    if not url:
        logger.error("No YouTube URL provided in the request")
        return jsonify({"success": False, "error": "No URL provided"}), 400

    if not separate_streams:
        video_url = download_yt(url)
        if video_url is None:
            return jsonify({"success": False, "error": "Failed to download video"}), 500
        return jsonify({"success": True, "url": video_url, "full_url": f"http://{lan_ip}:{UI_PORT}{video_url}"})
    else:
        video_url, audio_url = get_yt_streams(url)
        if video_url is None or audio_url is None:
            return jsonify({"success": False, "error": "Failed to retrieve video and audio streams"}), 500
        return jsonify({"success": True, "video_url": video_url, "audio_url": audio_url})

async def broadcast(message):
    for websocket in set(connected_clients):
        try:
            await websocket.send(message)
        except Exception as e:
            logger.error(f"Error sending message to WebSocket: {e}")

async def websocket_server(websocket):
    connected_clients.add(websocket)
    try:
      async for message in websocket:
          print(f"Received message: {message}")
          await websocket.send(f"Echo: {message}")
    finally:
      connected_clients.remove(websocket)

def start_websocket_server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()

    start_server = websockets.serve(websocket_server, '0.0.0.0', WS_PORT)
    loop.run_until_complete(start_server)
    loop.run_forever()

def start_server():
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    flask_thread = threading.Thread(target=lambda: app.run(debug=DEBUG, port=UI_PORT, use_reloader=False, host='0.0.0.0'))
    flask_thread.start()

    ws_thread = threading.Thread(target=start_websocket_server)
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
