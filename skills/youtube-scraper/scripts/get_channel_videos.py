#!/usr/bin/env python3
"""
Get all video URLs from a YouTube channel.
Supports both channel URLs and user URLs.
"""

import re
import sys
import argparse
from typing import List


def extract_channel_id(url: str) -> str:
    """Extract channel ID or custom channel name from URL."""
    patterns = [
        r'/channel/(UC[\w-]{22})',  # Channel ID format
        r'/c/([\w-]+)',              # Custom channel name
        r'/user/([\w-]+)',           # Username format
        r'/@([\w-]+)',               # Handle format
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    # If URL doesn't match known patterns, try to use it as-is
    return url.strip('/').split('/')[-1]


def generate_videos_url(channel_input: str) -> str:
    """
    Generate YouTube videos URL for a given channel input.
    channel_input can be: channel ID, custom name, or username
    """
    if channel_input.startswith('UC'):
        # It's a channel ID
        return f"https://www.youtube.com/channel/{channel_input}/videos"

    # It's a custom name, username, or handle
    return f"https://www.youtube.com/{channel_input}/videos"


def main():
    parser = argparse.ArgumentParser(
        description='Get YouTube channel videos URL'
    )
    parser.add_argument(
        'channel_url',
        help='YouTube channel URL (e.g., https://www.youtube.com/@username or https://www.youtube.com/channel/UC...)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: videos.txt)',
        default='videos.txt'
    )

    args = parser.parse_args()

    channel_input = extract_channel_id(args.channel_url)
    videos_url = generate_videos_url(channel_input)

    # Save the videos URL to file
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(videos_url + '\n')
        f.write('\n')
        f.write(f'Channel videos page: {videos_url}\n')
        f.write('\n')
        f.write('Note: This file contains the channel\'s videos page URL.\n')
        f.write('The actual video URLs will be extracted by the scraper.\n')

    print(f" Channel videos URL saved to: {args.output}")
    print(f"  Videos page: {videos_url}")
    print(f"\nNext steps:")
    print(f"  1. Use yt-dlp or similar tool to extract video URLs from the page")
    print(f"     Example: yt-dlp --get-id --flat-playlist {videos_url} > video_ids.txt")


if __name__ == '__main__':
    main()
