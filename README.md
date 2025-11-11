# Video Downloader

A versatile Python-based video downloader that supports YouTube, Vimeo, and many other video platforms. Built with `yt-dlp` and featuring a beautiful CLI interface with progress bars.

## Features

- 🎥 Download videos from multiple platforms (YouTube, Vimeo, etc.)
- 🎵 Extract audio only (MP3, M4A, Opus, WAV)
- 📊 Choose video quality (best, worst, or specific resolutions)
- 📋 List available formats for any video
- 🎨 Beautiful CLI interface with progress bars
- 🔄 Interactive mode for easy usage
- 📁 Organized downloads with custom output directory

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install FFmpeg (required for audio extraction and some video formats):**
   
   - **macOS:**
     ```bash
     brew install ffmpeg
     ```
   
   - **Ubuntu/Debian:**
     ```bash
     sudo apt update
     sudo apt install ffmpeg
     ```
   
   - **Windows:**
     Download from [FFmpeg website](https://ffmpeg.org/download.html) and add to PATH

## Usage

### Basic Usage

```bash
# Download video (best quality)
python video_downloader.py https://www.youtube.com/watch?v=VIDEO_ID

# Interactive mode
python video_downloader.py --interactive

# Download specific quality
python video_downloader.py https://www.youtube.com/watch?v=VIDEO_ID --quality 720p

# Download audio only
python video_downloader.py https://www.youtube.com/watch?v=VIDEO_ID --audio --format mp3

# List available formats
python video_downloader.py https://www.youtube.com/watch?v=VIDEO_ID --list-formats
```

### Command-Line Options

```
positional arguments:
  url                   URL of the video to download

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory (default: downloads)
  -q {best,worst,720p,1080p,480p,360p}, --quality {best,worst,720p,1080p,480p,360p}
                        Video quality (default: best)
  -a, --audio           Download audio only
  -f {mp3,m4a,opus,wav}, --format {mp3,m4a,opus,wav}
                        Audio format when using --audio (default: mp3)
  -v {mp4,webm,mkv}, --video-format {mp4,webm,mkv}
                        Video format (default: mp4)
  -l, --list-formats    List available formats for the video
  --interactive         Interactive mode
```

### Examples

```bash
# Download best quality video as MP4
python video_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Download 1080p video
python video_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -q 1080p

# Download audio as MP3
python video_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -a -f mp3

# Download to custom directory
python video_downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o ~/Videos

# Interactive mode
python video_downloader.py --interactive
```

## Supported Platforms

This downloader supports all platforms that `yt-dlp` supports, including:

- YouTube
- Vimeo
- Dailymotion
- Twitter/X
- TikTok
- Facebook
- Instagram
- And many more...

## Requirements

- Python 3.7+
- yt-dlp
- rich (for beautiful CLI)
- FFmpeg (for audio extraction and format conversion)

## License

This project is open source and available for personal use.

## Disclaimer

Please respect copyright laws and terms of service of video platforms. Only download videos you have permission to download or that are in the public domain.

