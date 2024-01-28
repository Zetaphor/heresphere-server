# HereSphere Server

A server to allow HereSphere to view YouTube videos. Also supports downloading any viewed videos from Youtube or direct links.

Not officially endorsed or affiliated with HereSphere.

## Setup

Install requirements:
```bash
pip install -r requirements.txt
```

Run the server:
```bash
python server.py
```

### Download Youtube video
```bash
curl --location 'localhost:5000/youtube' \
--header 'Content-Type: application/json' \
--data '{
    "url": "https://www.youtube.com/watch?v=zd7UqsWydaM",
    "separate_streams": false # Optional, defaults to false
}'
```

Response:

```json
{
    "full_url": "http://<detected ip>:5000/static/videos/youtube/zd7UqsWydaM___360_Shark_Megalodon_Bites_The_Ship_The_Largest_Shark_In_The_World_Vr_360_Video___3840x2160.webm",
    "success": true,
    "url": "/static/videos/youtube/zd7UqsWydaM___360_Shark_Megalodon_Bites_The_Ship_The_Largest_Shark_In_The_World_Vr_360_Video___3840x2160.webm"
}
```

### Get YouTube stream URLs:

Setting the `separate_streams` parameter to true will return two URLs: one for the audio stream and one for the video stream.

```bash
curl --location 'localhost:5000/youtube' \
--header 'Content-Type: application/json' \
--data '{
    "url": "https://www.youtube.com/watch?v=zd7UqsWydaM",
    "separate_streams": true
}'
```

Response:

```json
{
    "audio_url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1706424056/ei/mKK1Za7FG5D72_gPo7KSkAU/.../playlist/index.m3u8",
    "success": true,
    "video_url": "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1706424056/ei/mKK1Za7FG5D72_gPo7KSkAU/.../playlist/index.m3u8"
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
    "full_url": "http://<detected ip>:5000/static/videos/direct/test_video___test_video.webm",
    "success": true,
    "url": "/static/videos/direct/test_video___test_video.webm"
}}
```

