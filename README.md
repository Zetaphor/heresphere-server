# HereSphere Server

A server to allow HereSphere to view YouTube videos and [any other site supported by yt-dlp](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md). Also supports downloading any viewed videos yt-dlp supported links or direct video file links.

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
python3 main.py
```

## Building Windows binary

The Windows distributable is built with Pyinstaller.

1. Install Pyinstaller:

```bash
pip install pyinstaller
```

2. Run Pyinstaller, making sure to keep the .env file separated:

```bash
 pyinstaller .\main.py
 ```

3. Copy the [ffmpeg binaries](https://github.com/yt-dlp/FFmpeg-Builds#ffmpeg-static-auto-builds) to `C:\Users\zetap\Code\heresphere-server\dist\main\_internal\ffmpeg_x64`.

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

### Get stream URL:

**Youtube Streams**

Youtube videos will return both a `videoUrl` and an `audioUrl`

```bash
curl --location 'localhost:5000/stream' \
--header 'Content-Type: application/json' \
--data '{
    "url": "https://www.youtube.com/watch?v=zd7UqsWydaM",
}'
```

Response:

**Other Sites**

Any site that is in the [yt-dlp supported sites list](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) will be accepted.

Most other sites will only return a `videoUrl``

```bash
curl --location 'localhost:5000/stream' \
--header 'Content-Type: application/json' \
--data '{
    "url": "https://www.adultswim.com/videos/dr-stone/last-man-standing"
}'
````

```json
{
    "audioUrl": null,
    "success": true,
    "videoUrl": "https://tve-vod-aka.warnermediacdn.com/adultswim/3cbf4094adea04217dd1750ab1101604/layer7/layer7_bk.m3u8?hdntl=exp=1707221031~acl=%2fadultswim%2f3cbf4094adea04217dd1750ab1101604%2f*~hmac=0cd211dfc01f28416fc97b50aec0f79aff4e8c4890a295ba0ed22799a429be3b"
}
```

### Download video

Passing a `url` parameter will download the video and provide a local URL.

If the URL is not a direct link to a video file, it must be a site that is in the [yt-dlp supported sites list](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

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
}
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
