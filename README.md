# HereSphere Server

A server to allow HereSphere to view YouTube videos. Also supports downloading any viewed videos from Youtube or direct links.

Not officially endorsed or affiliated with HereSphere.

## Setup

This application was developed against Python 3.11.2.

Install requirements:
```bash
pip install -r requirements.txt
```

Run the server
```bash
python server.py
```

### Get YouTube stream URLs:
```bash
curl --location 'localhost:5000/youtube' \
--header 'Content-Type: application/json' \
--data '{
    "url": "https://www.youtube.com/watch?v=zd7UqsWydaM",
}'
```

Response:

```json
{
    "audioUrl": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1706424056/ei/mKK1Za7FG5D72_gPo7KSkAU/.../playlist/index.m3u8",
    "success": true,
    "videoUrl": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1706424056/ei/mKK1Za7FG5D72_gPo7KSkAU/.../playlist/index.m3u8"
}
```

### Download Youtube video

Providing the optional `separate_streams` (defaults to true) parameter will download the video and provide a local URL instead of the Google hosted audio and video URLs.

```bash
curl --location 'localhost:5000/youtube' \
--header 'Content-Type: application/json' \
--data '{
    "url": "https://www.youtube.com/watch?v=zd7UqsWydaM",
    "separate_streams": false # Optional, defaults to true
}'
```

Response:

```json
{
    "videoUrl": "http://<local ip>:5000/static/videos/youtube/zd7UqsWydaM___360_Shark_Megalodon_Bites_The_Ship_The_Largest_Shark_In_The_World_Vr_360_Video___3840x2160.webm",
    "success": true,
    "url": "/static/videos/youtube/zd7UqsWydaM___360_Shark_Megalodon_Bites_The_Ship_The_Largest_Shark_In_The_World_Vr_360_Video___3840x2160.webm"
}
```

### Download direct video
```bash
curl --location 'localhost:5000/download' \
--header 'Content-Type: application/json' \
--data '{
    "url": "https://f005.backblazeb2.com/file/zetaphor-vr-content/test_video.webm"
}'
```

Response:

```json
{
    "videoUrl": "http://<local ip>:5000/static/videos/direct/test_video___test_video.webm",
    "success": true,
    "url": "/static/videos/direct/test_video___test_video.webm"
}}
```

