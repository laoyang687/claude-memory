#!/usr/bin/env python3
"""
Translate subtitle Markdown files using Google Translate.
Supports batch translation of multiple files.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional
import time


def install_translator():
    """Install googletrans if not present."""
    try:
        from googletrans import Translator
        return True
    except ImportError:
        print("googletrans not found. Installing...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'googletrans==4.0.0-rc1'])
            print(" googletrans installed successfully")
            return True
        except subprocess.CalledProcessError:
            print(" Failed to install googletrans. Please run: pip install googletrans==4.0.0-rc1")
            return False


def translate_text(text: str, src: str = 'en', dest: str = 'zh-CN') -> Optional[str]:
    """
    Translate text using Google Translate.

    Args:
        text: Text to translate
        src: Source language code (default: 'en')
        dest: Target language code (default: 'zh-CN')

    Returns:
        Translated text, or None if failed
    """
    from googletrans import Translator

    try:
        translator = Translator()
        result = translator.translate(text, src=src, dest=dest)
        return result.text
    except Exception as e:
        print(f"   Translation error: {e}")
        return None


def translate_markdown_file(
    input_file: str,
    output_file: str = None,
    src: str = 'en',
    dest: str = 'zh-CN',
    keep_original: bool = True
) -> bool:
    """
    Translate a Markdown subtitle file.

    Args:
        input_file: Input Markdown file path
        output_file: Output Markdown file path (optional)
        src: Source language code
        dest: Target language code
        keep_original: Whether to keep original text alongside translation

    Returns:
        True if successful, False otherwise
    """
    input_path = Path(input_file)
    if not input_path.exists():
        print(f" Input file not found: {input_file}")
        return False

    # Read input file
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Determine output file
    if output_file is None:
        output_path = input_path.parent / f"{input_path.stem}_translated{input_path.suffix}"
    else:
        output_path = Path(output_file)

    print(f"Translating: {input_path.name}")

    # Process each line
    translated_lines = []
    in_content = False

    for line in lines:
        # Skip header
        if line.strip().startswith('#'):
            translated_lines.append(line)
            in_content = True
            continue

        # Skip empty lines
        if not line.strip():
            translated_lines.append(line)
            continue

        # Translate content lines
        if in_content:
            text = line.strip()
            if text:
                print(f"  Translating: {text[:50]}...")
                translation = translate_text(text, src, dest)

                if translation:
                    if keep_original:
                        # Format: English text\nChinese translation
                        translated_lines.append(f"{text}\n")
                        translated_lines.append(f"{translation}\n\n")
                    else:
                        translated_lines.append(f"{translation}\n\n")

                # Rate limiting to avoid API errors
                time.sleep(0.3)
            else:
                translated_lines.append(line)
        else:
            translated_lines.append(line)

    # Write output file
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(translated_lines)

    print(f"   Translation saved: {output_path}")
    return True


def translate_directory(
    input_dir: str,
    output_dir: str = None,
    pattern: str = '*.md',
    src: str = 'en',
    dest: str = 'zh-CN',
    keep_original: bool = True
) -> int:
    """
    Translate all Markdown files in a directory.

    Args:
        input_dir: Input directory path
        output_dir: Output directory path (optional)
        pattern: File pattern to match (default: '*.md')
        src: Source language code
        dest: Target language code
        keep_original: Whether to keep original text alongside translation

    Returns:
        Number of files successfully translated
    """
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f" Input directory not found: {input_dir}")
        return 0

    # Find all markdown files
    md_files = list(input_path.glob(pattern))

    if not md_files:
        print(f" No Markdown files found in: {input_dir}")
        return 0

    print(f"Found {len(md_files)} file(s) to translate")

    # Create output directory
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = input_path / 'translated'

    output_path.mkdir(parents=True, exist_ok=True)

    # Translate each file
    success_count = 0

    for md_file in md_files:
        output_file = output_path / md_file.name
        if translate_markdown_file(str(md_file), str(output_file), src, dest, keep_original):
            success_count += 1

    return success_count


def main():
    parser = argparse.ArgumentParser(
        description='Translate subtitle Markdown files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Translate single file
  python translate_subtitles.py video1.md

  # Translate directory
  python translate_subtitles.py -i ./subtitles -o ./translated

  # Translate without keeping original
  python translate_subtitles.py -i ./subtitles --no-keep-original

  # Specify languages
  python translate_subtitles.py video1.md --src en --dest zh-CN
        """
    )
    parser.add_argument(
        'file',
        nargs='?',
        help='Input Markdown file (or use -i for directory)'
    )
    parser.add_argument(
        '-i', '--input',
        help='Input directory containing Markdown files'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output directory/file (default: adds "_translated" suffix)'
    )
    parser.add_argument(
        '--src',
        help='Source language code (default: en)',
        default='en'
    )
    parser.add_argument(
        '--dest',
        help='Target language code (default: zh-CN)',
        default='zh-CN'
    )
    parser.add_argument(
        '--no-keep-original',
        action='store_true',
        help='Do not keep original text alongside translation'
    )
    parser.add_argument(
        '-p', '--pattern',
        help='File pattern to match (default: *.md)',
        default='*.md'
    )

    args = parser.parse_args()

    # Check dependencies
    if not install_translator():
        sys.exit(1)

    # Process single file
    if args.file:
        success = translate_markdown_file(
            args.file,
            args.output,
            args.src,
            args.dest,
            not args.no_keep_original
        )
        if success:
            print("\n Translation complete!")
        else:
            print("\n Translation failed")
            sys.exit(1)

    # Process directory
    elif args.input:
        count = translate_directory(
            args.input,
            args.output,
            args.pattern,
            args.src,
            args.dest,
            not args.no_keep_original
        )

        if count > 0:
            print(f"\n Translated {count} file(s)!")
        else:
            print("\n No files were translated")
            sys.exit(1)

    else:
        parser.print_help()
        print("\n Error: Please provide a file or directory with -i")
        sys.exit(1)


if __name__ == '__main__':
    main()
