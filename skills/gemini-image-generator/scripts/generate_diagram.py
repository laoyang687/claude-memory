#!/usr/bin/env python3
"""
Gemini Diagram Generator - Generate diagrams using Google Gemini API

Usage:
    python generate_diagram.py "<description>" [options]

Examples:
    python generate_diagram.py "User registration flow" --type flowchart
    python generate_diagram.py "AI applications" --type mindmap
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

try:
    import google.generativeai as genai
except ImportError:
    print("Required packages not found. Installing...")
    os.system(f"{sys.executable} -m pip install google-generativeai python-dotenv")
    import google.generativeai as genai


# Configure Gemini API
API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    print("[X] Error: GEMINI_API_KEY not found in .env file")
    sys.exit(1)

genai.configure(api_key=API_KEY)


def create_diagram_prompt(description, diagram_type, style=None):
    """Create a detailed prompt for diagram generation"""

    type_instructions = {
        'flowchart': f"Create a detailed flowchart for: {description}. Include start/end points, decision points, and process steps.",
        'mindmap': f"Create a comprehensive mind map for: {description}. Include main topic, major branches, and sub-branches with details.",
        'architecture': f"Create a system architecture diagram for: {description}. Include components, connections, data flows, and interactions.",
        'timeline': f"Create a timeline for: {description}. Include key events, milestones, dates, and sequential progression.",
        'hierarchy': f"Create a hierarchical diagram for: {description}. Show levels, reporting structure, and organizational relationships."
    }

    base_prompt = type_instructions.get(diagram_type, f"Create a diagram for: {description}")

    style_instructions = {
        'minimal': "Use minimal, clean design with simple shapes and clear labels.",
        'colorful': "Use vibrant colors, engaging visuals, and creative elements.",
        'professional': "Use professional, corporate styling with clean lines and business-appropriate design."
    }

    if style:
        base_prompt += f"\n\nStyle: {style_instructions.get(style, '')}"

    return base_prompt


def generate_diagram(description, output_path=None, diagram_type='flowchart',
                     style=None, size='1024x1024'):
    """
    Generate diagram using Gemini API

    Args:
        description: Description of the diagram content
        output_path: Output file path
        diagram_type: Type of diagram (flowchart, mindmap, etc.)
        style: Visual style (minimal, colorful, professional)
        size: Image dimensions

    Returns:
        Path to generated diagram
    """
    # Create prompt
    prompt = create_diagram_prompt(description, diagram_type, style)

    print(f"[*] Generating {diagram_type} diagram")
    print(f"    Description: {description}")

    # Create output path
    if output_path:
        output_path = Path(output_path)
    else:
        output_dir = Path(os.getenv('DEFAULT_OUTPUT_DIR', './output'))
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = output_dir / f"diagram_{diagram_type}_{timestamp}.png"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Use Gemini to generate diagram description
        model = genai.GenerativeModel('gemini-pro')

        # Generate detailed diagram specification
        full_prompt = f"""
{prompt}

Please provide:
1. A detailed description of the diagram structure
2. All elements and their relationships
3. Recommended layout and positioning
4. Text labels and content for each element

Format as a structured specification that can be used to create the visual diagram.
        """

        response = model.generate_content(full_prompt)

        # Save diagram specification
        spec_path = output_path.parent / f"{output_path.stem}_spec.txt"
        with open(spec_path, 'w', encoding='utf-8') as f:
            f.write(f"Diagram Type: {diagram_type}\n")
            f.write(f"Description: {description}\n")
            f.write(f"Style: {style if style else 'default'}\n")
            f.write(f"\n{'='*60}\n")
            f.write(f"Diagram Specification:\n")
            f.write(f"{'='*60}\n\n")
            f.write(response.text)

        print(f"[OK] Diagram specification saved: {spec_path}")
        print(f"[!] Note: This generates a diagram specification. For actual visual diagrams,")
        print(f"    you'll need to use the specification with a diagramming tool like:")
        print(f"    - Mermaid.js (for flowcharts, mindmaps)")
        print(f"    - PlantUML (for architecture diagrams)")
        print(f"    - Graphviz (for network diagrams)")
        print(f"    - draw.io / diagrams.net (for general diagrams)")

        return str(spec_path)

    except Exception as e:
        print(f"[X] Error generating diagram: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Generate diagrams using Google Gemini API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_diagram.py "User registration flow" --type flowchart
  python generate_diagram.py "AI applications" --type mindmap --style colorful
  python generate_diagram.py "Microservices architecture" --type architecture
        """
    )

    parser.add_argument('description', help='Description of the diagram content')
    parser.add_argument('--type', '-t',
                        choices=['flowchart', 'mindmap', 'architecture', 'timeline', 'hierarchy'],
                        default='flowchart',
                        help='Diagram type')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--style', '-s',
                        choices=['minimal', 'colorful', 'professional'],
                        help='Visual style')
    parser.add_argument('--size',
                        default='1024x1024',
                        help='Image dimensions (e.g., 1024x1024)')

    args = parser.parse_args()

    # Generate diagram
    result_path = generate_diagram(
        description=args.description,
        output_path=args.output,
        diagram_type=args.type,
        style=args.style,
        size=args.size
    )

    if result_path:
        print(f"\n[OK] Diagram generation complete")
        return 0
    else:
        print("\n[X] Failed to generate diagram")
        return 1


if __name__ == "__main__":
    sys.exit(main())
