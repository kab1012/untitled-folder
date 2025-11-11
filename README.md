# Video Downloader

A versatile Python-based video downloader that supports YouTube, Vimeo, and many other video platforms. Built with `yt-dlp` and featuring a beautiful CLI interface with progress bars.

## Features

- 🎥 Download videos from multiple platforms (YouTube, Vimeo, etc.)
- 🎵 Extract audio only (MP3, M4A, Opus, WAV)
- 📊 Choose video quality (best, worst, or specific resolutions)
- 📋 List available formats for any video
- 📂 Playlist support and duplicate avoidance via download archive
- 📝 Better filenames: `%(uploader)s/%(upload_date)s - %(title).200B [%(id)]`
- 🧩 Subtitles download (manual or auto) and optional embedding; choose format (SRT/VTT/ASS)
- 🖼️ Thumbnails write and optional embedding
- 🎛️ Media polish: remux containers, `--merge-output-format`, MP4 `--faststart`, audio loudness normalization
- 🍪 Cookies from browser for age/region-restricted content
- 🌐 Proxy, rate limit, and concurrent fragment downloads
- 🧾 Batch file support (many URLs)
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
     Download from `https://ffmpeg.org/download.html` and add to PATH

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

### Advanced Examples

```bash
# Use a nicer filename template and archive to skip already-downloaded videos
python video_downloader.py URL \
  --filename-template '%(uploader)s/%(upload_date>%Y-%m-%d)s - %(title).200B [%(id)s].%(ext)s' \
  --archive archive.txt

# Subtitles: prefer manual subs, fall back to auto, embed into output, in SRT
python video_downloader.py URL --subtitles --auto-subs --sub-langs en,en-US --sub-format srt --embed-subs

# Write and embed thumbnail into the media
python video_downloader.py URL --write-thumbnail --embed-thumbnail

# Media polish: remux to mp4 container and optimize for streaming
python video_downloader.py URL --remux-to mp4 --faststart

# Merge to MKV when combining separate video/audio streams
python video_downloader.py URL --merge-output-format mkv

# Audio-only with loudness normalization
python video_downloader.py URL -a -f m4a --audio-normalize

# Use cookies from your browser for restricted videos
python video_downloader.py URL --cookies-from-browser chrome

# Limit download rate and set a proxy
python video_downloader.py URL --rate-limit 2M --proxy http://127.0.0.1:8080

# Speed up HLS/fragmented downloads
python video_downloader.py URL --concurrent-fragments 8

# Remove SponsorBlock segments (use with care)
python video_downloader.py URL --sponsorblock-remove sponsor,intro,outro

# Batch download from a file of URLs (one per line, '#' for comments)
python video_downloader.py --batch-file urls.txt
```

### Command-Line Options (excerpt)

```
positional arguments:
  url                               URL of the video to download (or playlist URL)

optional arguments:
  -h, --help                        show this help message and exit
  -o OUTPUT, --output OUTPUT        Output directory (default: downloads)
  --filename-template TEMPLATE      Output filename template (yt-dlp syntax)
  --archive ARCHIVE                 Download archive file path (avoid duplicates)
  -q {best,worst,720p,1080p,480p,360p}, --quality {best,worst,720p,1080p,480p,360p}
                                    Video quality (default: best)
  -a, --audio                       Download audio only
  -f {mp3,m4a,opus,wav}, --format {mp3,m4a,opus,wav}
                                    Audio format when using --audio (default: mp3)
  -v {mp4,webm,mkv}, --video-format {mp4,webm,mkv}
                                    Video format (default: mp4)
  --merge-output-format {mp4,mkv,webm}
                                    Container for merging separate streams
  --remux-to {mp4,mkv,webm}         Remux output container without re-encoding
  --faststart                       Optimize MP4 for streaming (moov atom at start)
  --audio-normalize                 Normalize audio loudness (EBU R128)
  --subtitles                       Download subtitles (if available)
  --embed-subs                      Embed subtitles into video
  --sub-langs SUB_LANGS             Comma-separated subtitle languages (e.g., "en,en-US")
  --sub-format {srt,vtt,ass}        Subtitle file format
  --auto-subs                       Allow auto-generated subtitles when needed
  --write-thumbnail                 Write thumbnail file
  --embed-thumbnail                 Embed thumbnail into media file
  --cookies-from-browser BROWSER    Load cookies from browser (chrome, brave, firefox)
  --proxy PROXY                     HTTP(S) proxy URL (e.g., http://127.0.0.1:8080)
  --rate-limit RATE                 Max download rate, e.g., 2M or 500K
  --concurrent-fragments N          Number of fragments to download concurrently
  --sponsorblock-remove CATS        Comma-separated SponsorBlock categories to remove
  --batch-file FILE                 File containing URLs (one per line)
  -l, --list-formats                List available formats for the video
  --interactive                     Interactive mode
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

## Notes

- An `archive.txt` file is kept in the output directory to skip downloads already completed.
- Logs are written to `downloads/downloader.log` by default.

## License

This project is open source and available for personal use.

## Disclaimer

Please respect copyright laws and terms of service of video platforms. Only download videos you have permission to download or that are in the public domain.

