#!/usr/bin/env python3
"""
Video Downloader - A versatile video downloader using yt-dlp
Supports YouTube, Vimeo, and many other video platforms
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional

try:
    import yt_dlp
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.panel import Panel
    from rich.text import Text
except ImportError as e:
    print(f"Error: Missing required package. Please install dependencies:")
    print(f"  pip install -r requirements.txt")
    print(f"\nMissing package: {e.name}")
    sys.exit(1)


console = Console()


class VideoDownloader:
    """Main video downloader class"""
    
    def __init__(self, output_dir: str = "downloads"):
        """Initialize the downloader with output directory"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def progress_hook(self, d, progress: Progress, task):
        """Hook to update progress bar"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                progress.update(task, completed=d['downloaded_bytes'], total=d['total_bytes'])
            elif 'total_bytes_estimate' in d:
                progress.update(task, completed=d['downloaded_bytes'], total=d['total_bytes_estimate'])
        elif d['status'] == 'finished':
            progress.update(task, completed=100, total=100)
    
    def get_video_info(self, url: str) -> dict:
        """Get video information without downloading"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'formats': info.get('formats', []),
                    'thumbnail': info.get('thumbnail', ''),
                }
        except Exception as e:
            console.print(f"[red]Error getting video info: {str(e)}[/red]")
            return {}
    
    def download_video(
        self,
        url: str,
        quality: str = "best",
        format_type: str = "video",
        audio_format: str = "mp3",
        video_format: str = "mp4"
    ) -> bool:
        """
        Download video from URL
        
        Args:
            url: Video URL
            quality: Video quality (best, worst, or specific like 720p, 1080p)
            format_type: Type to download (video, audio, both)
            audio_format: Audio format (mp3, m4a, opus, etc.)
            video_format: Video format (mp4, webm, etc.)
        """
        console.print(f"\n[bold blue]Fetching video information...[/bold blue]")
        
        # Get video info first
        info = self.get_video_info(url)
        if not info:
            return False
        
        # Display video information
        title = info.get('title', 'Unknown')
        duration = info.get('duration', 0)
        uploader = info.get('uploader', 'Unknown')
        
        duration_str = f"{duration // 60}:{duration % 60:02d}" if duration else "Unknown"
        
        console.print(Panel(
            f"[bold]{title}[/bold]\n"
            f"Uploader: {uploader}\n"
            f"Duration: {duration_str}",
            title="Video Info",
            border_style="blue"
        ))
        
        # Configure download options
        ydl_opts = {
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
        }
        
        # Set format based on quality and type
        if format_type == "audio":
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': '192',
            }]
        elif format_type == "video":
            if quality == "best":
                ydl_opts['format'] = f'bestvideo[ext={video_format}]+bestaudio[ext=m4a]/best[ext={video_format}]/best'
            elif quality == "worst":
                ydl_opts['format'] = 'worst'
            else:
                # Try to match quality string (e.g., "720p", "1080p")
                ydl_opts['format'] = f'bestvideo[height<={quality.replace("p", "")}]+bestaudio/best[height<={quality.replace("p", "")}]'
        else:
            # Download both
            ydl_opts['format'] = 'best'
        
        # Download with progress
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=console
            ) as progress:
                task = progress.add_task("[green]Downloading...", total=100)
                
                def progress_hook_wrapper(d):
                    self.progress_hook(d, progress, task)
                
                ydl_opts['progress_hooks'] = [progress_hook_wrapper]
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            
            console.print(f"\n[bold green]✓ Download complete![/bold green]")
            console.print(f"[dim]Saved to: {self.output_dir}[/dim]")
            return True
            
        except Exception as e:
            console.print(f"\n[red]Error downloading video: {str(e)}[/red]")
            return False
    
    def list_formats(self, url: str):
        """List available formats for a video"""
        ydl_opts = {
            'listformats': True,
            'quiet': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(url, download=False)
        except Exception as e:
            console.print(f"[red]Error listing formats: {str(e)}[/red]")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Video Downloader - Download videos from various platforms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://www.youtube.com/watch?v=VIDEO_ID
  %(prog)s https://www.youtube.com/watch?v=VIDEO_ID --quality 720p
  %(prog)s https://www.youtube.com/watch?v=VIDEO_ID --audio --format mp3
  %(prog)s https://www.youtube.com/watch?v=VIDEO_ID --list-formats
        """
    )
    
    parser.add_argument(
        'url',
        nargs='?',
        help='URL of the video to download'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='downloads',
        help='Output directory (default: downloads)'
    )
    
    parser.add_argument(
        '-q', '--quality',
        default='best',
        choices=['best', 'worst', '720p', '1080p', '480p', '360p'],
        help='Video quality (default: best)'
    )
    
    parser.add_argument(
        '-a', '--audio',
        action='store_true',
        help='Download audio only'
    )
    
    parser.add_argument(
        '-f', '--format',
        default='mp3',
        choices=['mp3', 'm4a', 'opus', 'wav'],
        help='Audio format when using --audio (default: mp3)'
    )
    
    parser.add_argument(
        '-v', '--video-format',
        default='mp4',
        choices=['mp4', 'webm', 'mkv'],
        help='Video format (default: mp4)'
    )
    
    parser.add_argument(
        '-l', '--list-formats',
        action='store_true',
        help='List available formats for the video'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode'
    )
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive or not args.url:
        console.print("[bold cyan]Video Downloader - Interactive Mode[/bold cyan]\n")
        
        if not args.url:
            url = console.input("[bold]Enter video URL: [/bold]")
        else:
            url = args.url
        
        if args.list_formats:
            downloader = VideoDownloader(args.output)
            downloader.list_formats(url)
            return
        
        # Ask for options
        console.print("\n[bold]Download options:[/bold]")
        console.print("1. Video (best quality)")
        console.print("2. Video (specific quality)")
        console.print("3. Audio only")
        
        choice = console.input("\n[bold]Select option (1-3): [/bold]")
        
        downloader = VideoDownloader(args.output)
        
        if choice == "1":
            downloader.download_video(url, quality="best")
        elif choice == "2":
            quality = console.input("[bold]Enter quality (720p, 1080p, etc.): [/bold]")
            downloader.download_video(url, quality=quality)
        elif choice == "3":
            audio_format = console.input("[bold]Enter audio format (mp3, m4a, etc.) [default: mp3]: [/bold]") or "mp3"
            downloader.download_video(url, format_type="audio", audio_format=audio_format)
        else:
            console.print("[red]Invalid choice[/red]")
    
    # Command-line mode
    else:
        downloader = VideoDownloader(args.output)
        
        if args.list_formats:
            downloader.list_formats(args.url)
        else:
            format_type = "audio" if args.audio else "video"
            downloader.download_video(
                args.url,
                quality=args.quality,
                format_type=format_type,
                audio_format=args.format,
                video_format=args.video_format
            )


if __name__ == "__main__":
    main()

