#!/usr/bin/env python3
"""
Complete workflow: Scrape YouTube channel, download subtitles, translate to Chinese.
This script combines all functionality into a single workflow.
"""

import sys
import argparse
from pathlib import Path


def check_dependencies():
    """Check and install required dependencies."""
    required = {
        'yt_dlp': 'yt-dlp',
        'googletrans': 'googletrans==4.0.0-rc1'
    }

    missing = []

    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print("Installing missing dependencies...")
        import subprocess
        for package in missing:
            print(f"  Installing {package}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"   {package} installed")
            except subprocess.CalledProcessError:
                print(f"   Failed to install {package}")
                print(f"    Please run manually: pip install {package}")
                return False

    print(" All dependencies installed")
    return True


def scrape_channel(channel_url: str, output_dir: str) -> list[str]:
    """Step 1: Scrape all video URLs from YouTube channel."""
    print("\n" + "="*60)
    print("STEP 1: Scraping YouTube Channel")
    print("="*60)

    # Import here to avoid import errors if not installed
    try:
        import yt_dlp
    except ImportError:
        if not check_dependencies():
            return []

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Ensure URL ends with /videos
    if not channel_url.endswith('/videos'):
        if '/videos' not in channel_url:
            channel_url = channel_url.rstrip('/') + '/videos'

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist',
        'ignoreerrors': True,
    }

    video_urls = []

    try:
        print(f"Fetching videos from: {channel_url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)

            if 'entries' in info:
                for entry in info['entries']:
                    if entry and 'url' in entry:
                        video_urls.append(entry['url'])
                        print(f"  Found: {entry.get('title', 'Unknown')}")
            else:
                print(" No videos found")
                return []
    except Exception as e:
        print(f" Error: {e}")
        return []

    # Save to file
    urls_file = output_path / 'video_urls.txt'
    with open(urls_file, 'w', encoding='utf-8') as f:
        for url in video_urls:
            f.write(url + '\n')

    print(f"\n Saved {len(video_urls)} video URLs to: {urls_file}")
    return video_urls


def download_subtitles(video_urls: list[str], output_dir: str) -> list[str]:
    """Step 2: Download subtitles for all videos."""
    print("\n" + "="*60)
    print("STEP 2: Downloading Subtitles")
    print("="*60)

    import re

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    subtitle_files = []

    for i, video_url in enumerate(video_urls, 1):
        print(f"\n[{i}/{len(video_urls)}] Processing: {video_url}")

        try:
            import yt_dlp

            # Extract video ID
            match = re.search(r'(?:v=|/)([0-9A-Za-z_-]{11})', video_url)
            if not match:
                print(f"   Could not extract video ID")
                continue

            video_id = match.group(1)

            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['en'],
                'skip_download': True,
                'outtmpl': str(output_path / f'{video_id}.%(ext)s'),
                'subtitlesformat': 'vtt',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            vtt_file = output_path / f'{video_id}.en.vtt'

            if vtt_file.exists():
                # Convert to Markdown
                md_file = vtt_to_md(vtt_file)
                if md_file:
                    subtitle_files.append(md_file)
                    print(f"   Subtitle downloaded and converted")
                else:
                    print(f"   Failed to convert to Markdown")
            else:
                print(f"   No subtitles found")

        except Exception as e:
            print(f"   Error: {e}")

    print(f"\n Downloaded {len(subtitle_files)} subtitle(s)")
    return subtitle_files


def vtt_to_md(vtt_file: str) -> str:
    """Convert VTT file to Markdown format."""
    import re

    vtt_path = Path(vtt_file)

    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    subtitles = []

    for line in lines:
        line = line.strip()
        if line.startswith('WEBVTT') or '-->' in line or not line or line.startswith('NOTE'):
            continue

        line = re.sub(r'<[^>]+>', '', line).strip()

        if line and line not in subtitles:
            subtitles.append(line)

    if not subtitles:
        return None

    md_file = vtt_path.with_suffix('.md')

    with open(md_file, 'w', encoding='utf-8') as f:
        f.write('# Video Subtitles\n\n')
        for subtitle in subtitles:
            f.write(f'{subtitle}\n')

    return str(md_file)


def translate_subtitles(md_files: list[str], output_dir: str):
    """Step 3: Translate subtitles to Chinese."""
    print("\n" + "="*60)
    print("STEP 3: Translating to Chinese")
    print("="*60)

    try:
        from googletrans import Translator
    except ImportError:
        if not check_dependencies():
            return

    import time

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    translator = Translator()

    for i, md_file in enumerate(md_files, 1):
        print(f"\n[{i}/{len(md_files)}] Translating: {Path(md_file).name}")

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            translated_lines = []
            in_content = False

            for line in lines:
                if line.strip().startswith('#'):
                    translated_lines.append(line)
                    in_content = True
                    continue

                if not line.strip():
                    translated_lines.append(line)
                    continue

                if in_content:
                    text = line.strip()
                    if text:
                        try:
                            result = translator.translate(text, src='en', dest='zh-CN')
                            # Format: English\nChinese\n
                            translated_lines.append(f"{text}\n")
                            translated_lines.append(f"{result.text}\n\n")
                            time.sleep(0.3)  # Rate limiting
                        except Exception as e:
                            print(f"   Translation error: {e}")
                            translated_lines.append(line)
                    else:
                        translated_lines.append(line)
                else:
                    translated_lines.append(line)

            # Save translated file
            input_path = Path(md_file)
            output_file = output_path / f"{input_path.stem}_translated.md"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.writelines(translated_lines)

            print(f"   Translation saved")

        except Exception as e:
            print(f"   Error: {e}")

    print(f"\n Translation complete!")


def main():
    parser = argparse.ArgumentParser(
        description='Complete YouTube channel to translated subtitles workflow',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full workflow
  python youtube_to_md.py https://www.youtube.com/@username/videos -o ./output

  # Step-by-step
  python youtube_to_md.py https://www.youtube.com/@username/videos -o ./output --step scrape
  python youtube_to_md.py -o ./output --step download
  python youtube_to_md.py -o ./output --step translate
        """
    )
    parser.add_argument(
        'channel_url',
        nargs='?',
        help='YouTube channel URL (must end with /videos)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output directory (default: ./youtube_content)',
        default='./youtube_content'
    )
    parser.add_argument(
        '--step',
        choices=['scrape', 'download', 'translate'],
        help='Run specific step only'
    )

    args = parser.parse_args()

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    output_dir = Path(args.output)

    # Determine which steps to run
    if args.step == 'scrape':
        # Only scrape
        urls_file = output_dir / 'video_urls.txt'
        if not urls_file.exists():
            print(" video_urls.txt not found. Run full workflow first.")
            sys.exit(1)

        with open(urls_file, 'r') as f:
            video_urls = [line.strip() for line in f if line.strip()]

        print(f"Found {len(video_urls)} URLs")

    elif args.step == 'download':
        # Only download and translate
        vtt_dir = output_dir / 'subtitles_vtt'
        md_dir = output_dir / 'subtitles_md'

        if not vtt_dir.exists():
            print(" VTT directory not found. Run scrape step first.")
            sys.exit(1)

        vtt_files = list(vtt_dir.glob('*.vtt'))
        print(f"Found {len(vtt_files)} VTT files")

        # Convert to MD
        md_files = []
        for vtt_file in vtt_files:
            md_file = vtt_to_md(vtt_file)
            if md_file:
                md_files.append(md_file)

        print(f"Converted {len(md_files)} files to Markdown")

    elif args.step == 'translate':
        # Only translate
        md_dir = output_dir / 'subtitles_md'

        if not md_dir.exists():
            print(" Markdown directory not found. Run download step first.")
            sys.exit(1)

        md_files = list(md_dir.glob('*.md'))
        print(f"Found {len(md_files)} MD files")

        translated_dir = output_dir / 'translated'
        translate_subtitles([str(f) for f in md_files], str(translated_dir))

    else:
        # Full workflow
        if not args.channel_url:
            parser.print_help()
            print("\n Error: Please provide a channel URL")
            sys.exit(1)

        # Step 1: Scrape channel
        video_urls = scrape_channel(args.channel_url, str(output_dir))

        if not video_urls:
            print("\n No videos found")
            sys.exit(1)

        # Step 2: Download subtitles
        vtt_dir = output_dir / 'subtitles_vtt'
        md_dir = output_dir / 'subtitles_md'

        md_files = download_subtitles(video_urls, str(vtt_dir))

        if not md_files:
            print("\n No subtitles downloaded")
            sys.exit(1)

        # Move MD files to dedicated directory
        md_path = Path(md_dir)
        md_path.mkdir(parents=True, exist_ok=True)

        for md_file in md_files:
            md_src = Path(md_file)
            md_dst = md_path / md_src.name
            md_src.rename(md_dst)

        # Step 3: Translate
        translated_dir = output_dir / 'translated'
        md_files = [str(f) for f in md_path.glob('*.md')]
        translate_subtitles(md_files, str(translated_dir))

        print("\n" + "="*60)
        print("WORKFLOW COMPLETE!")
        print("="*60)
        print(f"\nOutput directory: {output_dir}")
        print(f"  - video_urls.txt: List of all video URLs")
        print(f"  - subtitles_md/: Original English subtitles")
        print(f"  - translated/: Translated Chinese subtitles")


if __name__ == '__main__':
    main()
