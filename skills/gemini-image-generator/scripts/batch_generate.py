#!/usr/bin/env python3
"""
Batch Image Generator - Generate multiple images from a text file

Usage:
    python batch_generate.py <input_file.txt> [options]

Input file format:
    One prompt per line
    Empty lines and lines starting with # are ignored
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import os

# Import the generate_image function
try:
    from generate_image import generate_image
except ImportError:
    print("[X] Error: Could not import generate_image module")
    sys.exit(1)


def load_prompts(input_file):
    """Load prompts from text file, ignoring comments and empty lines"""
    prompts = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith('#'):
                prompts.append(line)
    return prompts


def batch_generate(input_file, output_dir=None, style=None, quality='standard'):
    """
    Generate multiple images from prompts in a text file

    Args:
        input_file: Path to text file with prompts
        output_dir: Output directory for generated images
        style: Style to apply to all images
        quality: Quality setting for all images

    Returns:
        Tuple of (success_count, fail_count, all_generated_paths)
    """
    # Load prompts
    prompts = load_prompts(input_file)

    if not prompts:
        print("[X] No prompts found in input file")
        return 0, 0, []

    print(f"[*] Loaded {len(prompts)} prompts from {input_file}")

    # Create output directory
    if output_dir:
        output_dir = Path(output_dir)
    else:
        output_dir = Path('./output')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate images for each prompt
    success_count = 0
    fail_count = 0
    all_paths = []

    for i, prompt in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}] Processing: {prompt[:50]}...")

        # Create unique output path for each image
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = output_dir / f"batch_{timestamp}_{i:03d}.png"

        try:
            generated_paths = generate_image(
                prompt=prompt,
                output_path=str(output_path),
                style=style,
                quality=quality,
                count=1
            )

            if generated_paths:
                success_count += 1
                all_paths.extend(generated_paths)
            else:
                fail_count += 1

        except Exception as e:
            print(f"[X] Error: {e}")
            fail_count += 1
            continue

    return success_count, fail_count, all_paths


def main():
    parser = argparse.ArgumentParser(
        description='Generate multiple images from prompts in a text file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python batch_generate.py prompts.txt
  python batch_generate.py prompts.txt --output-dir ./results
  python batch_generate.py prompts.txt --style photorealistic --quality high

Input file format:
  # This is a comment
  A serene mountain landscape
  Abstract geometric patterns
  Professional business person in office
        """
    )

    parser.add_argument('input_file', help='Text file with prompts (one per line)')
    parser.add_argument('--output-dir', '-o', help='Output directory for generated images')
    parser.add_argument('--style', '-s',
                        choices=['photorealistic', 'artistic', 'minimalist', 'abstract', 'cartoon'],
                        help='Style to apply to all images')
    parser.add_argument('--quality', '-q',
                        choices=['standard', 'high', 'ultra'],
                        default='standard',
                        help='Quality setting for all images')

    args = parser.parse_args()

    # Check input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"[X] Error: Input file not found: {args.input_file}")
        return 1

    # Batch generate
    success, fail, all_paths = batch_generate(
        input_file=args.input_file,
        output_dir=args.output_dir,
        style=args.style,
        quality=args.quality
    )

    # Print summary
    print(f"\n{'='*60}")
    print("Batch Generation Summary")
    print(f"{'='*60}")
    print(f"Total prompts:     {success + fail}")
    print(f"Successful:        {success}")
    print(f"Failed:            {fail}")
    print(f"Output directory:  {args.output_dir or './output'}")

    if all_paths:
        print(f"\nGenerated files:")
        for path in all_paths:
            print(f"  - {path}")

    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
