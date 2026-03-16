---
name: youtube-scraper
description: Extract and translate YouTube video content. Use when user wants to: (1) Scrape all video URLs from a YouTube channel, (2) Download video subtitles and convert to Markdown, (3) Translate English subtitles to Chinese, (4) Triggered by phrases like "获取youtube文案", "youtube字幕下载", "youtube字幕翻译", or similar requests involving YouTube content extraction.
---

# YouTube Content Scraper

Extract video URLs, download subtitles, and translate to Chinese from YouTube channels.

## Quick Start

For the complete workflow (scrape → download → translate):

```bash
python scripts/youtube_to_md.py <CHANNEL_URL> -o <OUTPUT_DIR>
```

Example:
```bash
python scripts/youtube_to_md.py https://www.youtube.com/@username/videos -o ./my_content
```

## Individual Steps

### 1. Scrape Channel Videos

Extract all video URLs from a YouTube channel:

```bash
python scripts/scrape_youtube_channel.py <CHANNEL_URL> -o videos.txt
```

**Important**: URL must end with `/videos`
- Valid: `https://www.youtube.com/@username/videos`
- Valid: `https://www.youtube.com/channel/UC.../videos`

### 2. Download Subtitles

Download and convert subtitles to Markdown:

```bash
python scripts/get_subtitles.py -i videos.txt -o ./subtitles --convert-md
```

Options:
- `-i`: Input file with video URLs (one per line)
- `-o`: Output directory (default: `./subtitles`)
- `-l`: Language code (default: `en`)
- `--convert-md`: Convert VTT to Markdown format
- `--no-auto`: Skip auto-generated subtitles

### 3. Translate Subtitles

Translate English Markdown files to Chinese:

```bash
python scripts/translate_subtitles.py -i ./subtitles -o ./translated
```

Options:
- `-i`: Input directory or file
- `-o`: Output directory (optional, adds `_translated` suffix if not specified)
- `--src`: Source language (default: `en`)
- `--dest`: Target language (default: `zh-CN`)
- `--no-keep-original`: Only keep translated text (default keeps both English and Chinese)

## Output Format

Translated Markdown files contain bilingual subtitles:
```markdown
English subtitle text here
中文字幕翻译在这里
```

## Dependencies

Required Python packages (auto-installed):
- `yt-dlp`: YouTube video metadata extraction
- `googletrans==4.0.0-rc1`: Google Translate API

Install manually if needed:
```bash
pip install yt-dlp googletrans==4.0.0-rc1
```

## Tips

- Use channel URL format: `https://www.youtube.com/@username/videos`
- For channels with many videos, the process may take time
- Google Translate has rate limits - add delays in translation script
- Auto-generated subtitles are used if manual subtitles unavailable

## Troubleshooting

**No videos found**: Ensure URL ends with `/videos`

**No subtitles available**: Some videos may not have English subtitles

**Translation errors**: Rate limiting from Google Translate - increase `time.sleep()` delay

**Permission denied**: Check write permissions for output directory
