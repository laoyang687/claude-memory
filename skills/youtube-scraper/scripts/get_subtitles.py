#!/usr/bin/env python3
"""
Download subtitles from YouTube video URLs.
Supports auto-generated and manual subtitles.
"""

import subprocess
import sys
import argparse
from pathlib import Path
from typing import Optional


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


def get_video_id(url: str) -> Optional[str]:
    """Extract video ID from YouTube URL."""
    import re

    patterns = [
        r'(?:v=|/)([0-9A-Za-z_-]{11}).*',
        r'youtu\.be/([0-9A-Za-z_-]{11})',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def get_subtitles(
    video_url: str,
    output_dir: str,
    lang: str = 'en',
    auto_subs: bool = True
) -> Optional[str]:
    """
    Download subtitles from a YouTube video.

    Args:
        video_url: YouTube video URL
        output_dir: Directory to save subtitle files
        lang: Language code (default: 'en')
        auto_subs: Whether to use auto-generated subtitles if manual not available

    Returns:
        Path to downloaded subtitle file, or None if failed
    """
    try:
        import yt_dlp
    except ImportError:
        if not install_yt_dlp():
            return None

    video_id = get_video_id(video_url)
    if not video_id:
        print(f" Could not extract video ID from: {video_url}")
        return None

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Configure yt-dlp options
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'writesubtitles': True,
        'writeautomaticsub': auto_subs,
        'subtitleslangs': [lang],
        'skip_download': True,
        'outtmpl': str(output_path / f'{video_id}.%(ext)s'),
        'subtitlesformat': 'vtt',  # WebVTT format
    }

    try:
        print(f"Downloading subtitles for: {video_url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Find the downloaded subtitle file
        vtt_file = output_path / f'{video_id}.{lang}.vtt'

        if vtt_file.exists():
            print(f"   Subtitle saved: {vtt_file}")
            return str(vtt_file)
        else:
            print(f"   No subtitles found for this video")
            return None

    except Exception as e:
        print(f"   Error downloading subtitles: {e}")
        return None


def vtt_to_md(vtt_file: str, output_md: str = None) -> str:
    """
    Convert VTT subtitle file to Markdown format.

    Args:
        vtt_file: Path to VTT subtitle file
        output_md: Path to output Markdown file (optional)

    Returns:
        Path to generated MD file, or None if failed
    """
    import re

    vtt_path = Path(vtt_file)
    if not vtt_path.exists():
        print(f" VTT file not found: {vtt_file}")
        return None

    # Read VTT content
    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse VTT and extract text
    lines = content.split('\n')
    subtitles = []

    for line in lines:
        line = line.strip()
        # Skip header, timestamps, and empty lines
        if (
            line.startswith('WEBVTT') or
            '-->' in line or
            not line or
            line.startswith('NOTE')
        ):
            continue

        # Remove VTT-specific formatting
        line = re.sub(r'<[^>]+>', '', line)  # Remove HTML tags
        line = line.strip()

        if line and line not in subtitles:
            subtitles.append(line)

    if not subtitles:
        print(f" No subtitle text found in: {vtt_file}")
        return None

    # Generate output path
    if output_md is None:
        output_md = vtt_path.with_suffix('.md')
    else:
        output_md = Path(output_md)

    # Write Markdown file
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write('# Subtitles\n\n')
        for subtitle in subtitles:
            f.write(f'{subtitle}\n')

    print(f"   Markdown saved: {output_md}")
    return str(output_md)


def main():
    parser = argparse.ArgumentParser(
        description='Download subtitles from YouTube videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download single video subtitles
  python get_subtitles.py https://www.youtube.com/watch?v=xxx

  # Download from list of URLs
  python get_subtitles.py -i videos.txt -o ./subtitles

  # Specify language
  python get_subtitles.py https://www.youtube.com/watch?v=xxx -l en
        """
    )
    parser.add_argument(
        'url',
        nargs='?',
        help='YouTube video URL (or use -i for file input)'
    )
    parser.add_argument(
        '-i', '--input',
        help='Input file containing video URLs (one per line)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output directory for subtitle files (default: ./subtitles)',
        default='./subtitles'
    )
    parser.add_argument(
        '-l', '--lang',
        help='Subtitle language code (default: en)',
        default='en'
    )
    parser.add_argument(
        '--no-auto',
        action='store_true',
        help='Do not use auto-generated subtitles'
    )
    parser.add_argument(
        '--convert-md',
        action='store_true',
        help='Convert VTT to Markdown format'
    )

    args = parser.parse_args()

    if not args.url and not args.input:
        parser.print_help()
        print("\n Error: Please provide a URL or input file with -i")
        sys.exit(1)

    video_urls = []

    if args.url:
        video_urls.append(args.url)

    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f" Input file not found: {args.input}")
            sys.exit(1)

        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                url = line.strip()
                if url and url.startswith('http'):
                    video_urls.append(url)

    print(f"Processing {len(video_urls)} video(s)...")

    for url in video_urls:
        vtt_file = get_subtitles(url, args.output, args.lang, not args.no_auto)

        if vtt_file and args.convert_md:
            vtt_to_md(vtt_file)

    print("\n Done!")


if __name__ == '__main__':
    main()
