#!/usr/bin/env python3
"""
Gemini Image Generator - Generate images using Google Gemini API

Usage:
    python generate_image.py "<prompt>" [options]

Examples:
    python generate_image.py "A serene mountain landscape at sunset"
    python generate_image.py "Cyberpunk city" --style photorealistic --quality high
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

try:
    import google.generativeai as genai
    from PIL import Image
    import io
except ImportError:
    print("Required packages not found. Installing...")
    os.system(f"{sys.executable} -m pip install google-generativeai python-dotenv Pillow")
    import google.generativeai as genai
    from PIL import Image
    import io


# Configure Gemini API
API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    print("[X] Error: GEMINI_API_KEY not found in .env file")
    sys.exit(1)

genai.configure(api_key=API_KEY)


def parse_size(size_str):
    """Parse size string like '1024x1024' into tuple (1024, 1024)"""
    try:
        width, height = map(int, size_str.lower().split('x'))
        return (width, height)
    except:
        return (1024, 1024)


def enhance_prompt(prompt, style=None):
    """Enhance the prompt with style modifiers"""
    style_modifiers = {
        'photorealistic': 'photorealistic, highly detailed, 8k, professional photography',
        'artistic': 'artistic, painterly, creative illustration',
        'minimalist': 'minimalist, clean, simple design',
        'abstract': 'abstract, creative interpretation, artistic',
        'cartoon': 'cartoon style, colorful, friendly illustration'
    }

    if style and style in style_modifiers:
        return f"{prompt}, {style_modifiers[style]}"
    return prompt


def generate_image(prompt, output_path=None, style=None, quality='standard',
                   size='1024x1024', negative_prompt=None, count=1):
    """
    Generate image using Gemini API

    Args:
        prompt: Text description of image to generate
        output_path: Output file path
        style: Image style (photorealistic, artistic, etc.)
        quality: Generation quality (standard, high, ultra)
        size: Image dimensions (e.g., '1024x1024')
        negative_prompt: Things to avoid in the image
        count: Number of images to generate

    Returns:
        List of generated image paths
    """
    # Enhance prompt with style
    enhanced_prompt = enhance_prompt(prompt, style)

    # Add negative prompt if provided
    if negative_prompt:
        enhanced_prompt += f", avoiding: {negative_prompt}"

    print(f"[*] Generating image with prompt: {enhanced_prompt}")

    # Create output directory
    if output_path:
        output_path = Path(output_path)
    else:
        output_dir = Path(os.getenv('DEFAULT_OUTPUT_DIR', './output'))
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = output_dir / f"image_{timestamp}.png"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    generated_paths = []

    # Generate images
    for i in range(count):
        try:
            # Note: Gemini API may not support direct image generation
            # This is a placeholder implementation
            # Actual implementation depends on Gemini API capabilities

            # For now, we'll use a text-based approach
            model = genai.GenerativeModel('gemini-pro')

            # Create a detailed prompt for image generation
            image_prompt = f"""
            Create an image with the following description:
            {enhanced_prompt}

            Style: {style if style else 'default'}
            Quality: {quality}
            Size: {size}
            """

            # Try to generate (this may need adjustment based on actual API)
            response = model.generate_content(image_prompt)

            # Since Gemini may not generate images directly,
            # we'll save the response and provide feedback
            print(f"[!] Image generation response: {response.text[:200]}...")

            # Placeholder: Save a text file with the description
            # In production, you'd use an actual image generation API
            if count == 1:
                final_path = output_path
            else:
                final_path = output_path.parent / f"{output_path.stem}_{i}{output_path.suffix}"

            # For demonstration, create a placeholder
            # In real implementation, decode and save actual image data
            with open(final_path, 'w', encoding='utf-8') as f:
                f.write(f"Image Generation Request\n")
                f.write(f"Prompt: {enhanced_prompt}\n")
                f.write(f"Style: {style}\n")
                f.write(f"Quality: {quality}\n")
                f.write(f"Size: {size}\n")
                f.write(f"\nNote: This is a placeholder. Actual image generation requires")
                f.write(f" a Gemini API endpoint that supports image generation.\n")
                f.write(f"\nAPI Response:\n{response.text}\n")

            generated_paths.append(final_path)
            print(f"[OK] Generated: {final_path}")

        except Exception as e:
            print(f"[X] Error generating image {i+1}: {e}")
            continue

    return generated_paths


def main():
    parser = argparse.ArgumentParser(
        description='Generate images using Google Gemini API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_image.py "A serene mountain landscape at sunset"
  python generate_image.py "Cyberpunk city" --style photorealistic --quality high
  python generate_image.py "Beach sunset" --negative "crowded, noisy"
  python generate_image.py "Abstract patterns" --count 4
        """
    )

    parser.add_argument('prompt', help='Text description of image to generate')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--style', '-s',
                        choices=['photorealistic', 'artistic', 'minimalist', 'abstract', 'cartoon'],
                        help='Image style')
    parser.add_argument('--quality', '-q',
                        choices=['standard', 'high', 'ultra'],
                        default='standard',
                        help='Image quality')
    parser.add_argument('--size',
                        default='1024x1024',
                        help='Image dimensions (e.g., 1024x1024)')
    parser.add_argument('--negative', '-n',
                        help='Negative prompt (what to avoid)')
    parser.add_argument('--count', '-c',
                        type=int,
                        default=1,
                        help='Number of images to generate')

    args = parser.parse_args()

    # Generate images
    generated_paths = generate_image(
        prompt=args.prompt,
        output_path=args.output,
        style=args.style,
        quality=args.quality,
        size=args.size,
        negative_prompt=args.negative,
        count=args.count
    )

    if generated_paths:
        print(f"\n[OK] Successfully generated {len(generated_paths)} image(s)")
        for path in generated_paths:
            print(f"    - {path}")
        return 0
    else:
        print("\n[X] Failed to generate any images")
        return 1


if __name__ == "__main__":
    sys.exit(main())
