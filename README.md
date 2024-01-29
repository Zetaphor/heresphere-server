# HereSphere Server

A server to allow HereSphere to view YouTube videos. Also supports downloading any viewed videos from Youtube or direct links.

Not officially endorsed by or affiliated with HereSphere.

# Installation

* Windows Users - Download the latest release from [the releases page](https://github.com/Zetaphor/heresphere-server/releases).
* Mac Users - Follow the instructions below to run the Python server.
* Linux Users - Follow the instructions below to run the Python server.

# Running from source

Either download the repository or clone it locally.


```bash
git clone https://github.com/zetaphor/heresphere-server
```

## Setup

This application was developed against Python 3.11.2.

### Virtual Environment Setup

Before installing the dependencies, it's recommended to set up a virtual environment. This isolates your project dependencies from your global Python environment. There are several tools available for this:

#### Using venv (built into Python)

1. Create a virtual environment:

```bash
python3 -m venv .venv
```

2. Activate the virtual environment:

```bash
source .venv/bin/activate
```

#### Using pyenv (great for managing multiple Python versions)

1. Install pyenv, see [pyenv installation instructions](https://github.com/pyenv/pyenv).
2. Install Python 3.11.2 (if not already installed):

```bash
pyenv install 3.11.2
```
3. Create a new virtual environment with Python 3.11.2:

```bash
pyenv virtualenv 3.11.2 .venv
```

4. Activate the virtual environment:

```bash
source .venv/bin/activate
```

### Dependencies

Once your virtual environment is active, install the project dependencies:
```bash
pip install -r requirements.txt
```

Remember to deactivate your virtual environment when you're done:

Using venv or pyenv:
```bash
deactivate
```

## Running

Run the server
```bash
python main.py
```

### Connection Test

Used to verify that the HereSphere client can reach the server

```bash
curl --location 'localhost:5000/connection_test'
```

Response:

```json
{
    "success": true
}
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

### Download video (Youtube or direct link)

Passing a `url` parameter will download the video and provide a local URL.

**Downloading a direct video link**

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

**Downloading a Youtube video**

```bash
curl --location 'localhost:5000/download' \
--header 'Content-Type: application/json' \
--data '{
    "url": "https://www.youtube.com/watch?v=zd7UqsWydaM"
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
