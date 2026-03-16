#!/usr/bin/env python3
"""
Scrape all video URLs from a YouTube channel using yt-dlp.
Requires: pip install yt-dlp
"""

import subprocess
import sys
import argparse
from pathlib import Path


def install_yt_dlp():
    """Install yt-dlp if not present."""
    try:
        import yt_dlp
        return True
    except ImportError:
        print("yt-dlp not found. Installing...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yt-dlp'])
            print(" yt-dlp installed successfully")
            return True
        except subprocess.CalledProcessError:
            print(" Failed to install yt-dlp. Please run: pip install yt-dlp")
            return False


def get_video_urls(channel_url: str, output_file: str = None) -> list[str]:
    """
    Extract all video URLs from a YouTube channel.

    Args:
        channel_url: YouTube channel URL (e.g., https://www.youtube.com/@username/videos)
        output_file: Optional file path to save URLs

    Returns:
        List of video URLs
    """
    try:
        import yt_dlp
    except ImportError:
        if not install_yt_dlp():
            return []

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist',  # Faster, doesn't download video info
        'ignoreerrors': True,  # Continue on errors
    }

    video_urls = []

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Fetching videos from: {channel_url}")
            info = ydl.extract_info(channel_url, download=False)

            if 'entries' in info:
                for entry in info['entries']:
                    if entry and 'url' in entry:
                        video_url = entry['url']
                        video_urls.append(video_url)
                        print(f"  Found: {entry.get('title', 'Unknown')} - {video_url}")
            else:
                print(" No videos found. Make sure the URL is a channel/videos page.")
                return []
    except Exception as e:
        print(f" Error fetching videos: {e}")
        print("\nTips:")
        print("  - Make sure the URL ends with /videos")
        print("  - Examples:")
        print("     https://www.youtube.com/@username/videos")
        print("     https://www.youtube.com/channel/UC.../videos")
        return []

    # Save to file if specified
    if output_file and video_urls:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            for url in video_urls:
                f.write(url + '\n')

        print(f"\n Saved {len(video_urls)} video URLs to: {output_file}")

    return video_urls


def main():
    parser = argparse.ArgumentParser(
        description='Scrape all video URLs from a YouTube channel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scrape_youtube_channel.py https://www.youtube.com/@mrbeast/videos
  python scrape_youtube_channel.py https://www.youtube.com/@mrbeast/videos -o my_videos.txt
  python scrape_youtube_channel.py https://www.youtube.com/channel/UC.../videos
        """
    )
    parser.add_argument(
        'channel_url',
        help='YouTube channel videos URL (must end with /videos)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: videos.txt in current directory)',
        default='videos.txt'
    )

    args = parser.parse_args()

    # Ensure URL ends with /videos
    url = args.channel_url
    if not url.endswith('/videos'):
        if '/videos' not in url:
            url = url.rstrip('/') + '/videos'
            print(f"Added /videos to URL: {url}")

    video_urls = get_video_urls(url, args.output)

    if video_urls:
        print(f"\n Total videos found: {len(video_urls)}")
    else:
        print("\n No videos found")
        sys.exit(1)


if __name__ == '__main__':
    main()
