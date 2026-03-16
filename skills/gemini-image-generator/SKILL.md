---
name: gemini-image-generator
description: Generate images using Google Gemini API. Use when you want to create images, diagrams, illustrations, or visual content. Trigger phrases include "generate an image", "create a diagram", "make an illustration", "use Gemini to draw", "visualize this", "create a picture", or "make an image with Gemini". Supports text-to-image generation with various styles including photorealistic, artistic, diagrams, and custom visual content.
---

# Gemini Image Generator

Generate images using Google's Gemini API for text-to-image conversion, diagrams, and illustrations.

## Quick Start

Generate an image from text description:

```bash
python scripts/generate_image.py "A serene mountain landscape at sunset" --output ./output/image1.png
```

Generate with specific style:

```bash
python scripts/generate_image.py "Futuristic cityscape" --style photorealistic --output ./output/city.png
```

Generate a diagram:

```bash
python scripts/generate_diagram.py "Software architecture with microservices" --output ./output/architecture.png
```

## Image Generation Types

### Text-to-Image

Generate any visual content from text descriptions:

```bash
python scripts/generate_image.py "A cozy coffee shop interior" --output ./coffee.png
```

**Style Options:**
- `photorealistic` - Realistic, detailed images
- `artistic` - Painterly, stylized images
- `minimalist` - Simple, clean designs
- `abstract` - Non-representational visuals
- `cartoon` - Animated or illustrated style

**Quality Options:**
- `standard` - Balanced quality and speed
- `high` - Higher detail and refinement
- `ultra` - Maximum quality (slower)

### Diagrams and Visualizations

Create structured diagrams:

```bash
python scripts/generate_diagram.py "Flowchart: User registration process" --output ./flowchart.png

python scripts/generate_diagram.py "Mind map: AI applications" --style mindmap --output ./mindmap.png
```

**Diagram Types:**
- `flowchart` - Process flows and decision trees
- `mindmap` - Hierarchical concept maps
- `architecture` - System and software architecture
- `timeline` - Sequential events and milestones
- `hierarchy` - Organizational structures

### Illustrations

Generate custom illustrations:

```bash
python scripts/generate_image.py "Cute robot mascot for tech startup" --style cartoon --output ./mascot.png
```

## Configuration

### API Key Setup

The API key is pre-configured in: `C:\Users\wqj85\.claude\skills\gemini-image-generator\.env`

```
GEMINI_API_KEY=AIzaSyD5LqX5M6n3ppjhOBnOlfRL2ohk1-j3b6E
```

### Environment Variables

Optional settings in `.env`:

```env
GEMINI_API_KEY=your_api_key
DEFAULT_OUTPUT_DIR=./output
DEFAULT_STYLE=photorealistic
DEFAULT_QUALITY=standard
IMAGE_SIZE=1024x1024
```

## Script Reference

### generate_image.py

Main script for text-to-image generation.

**Usage:**
```bash
python scripts/generate_image.py "<prompt>" [options]
```

**Options:**
- `--output` - Output file path (default: ./output/image_TIMESTAMP.png)
- `--style` - Image style (photorealistic, artistic, minimalist, abstract, cartoon)
- `--quality` - Image quality (standard, high, ultra)
- `--size` - Image dimensions (default: 1024x1024)
- `--negative` - Negative prompt (what to avoid)
- `--count` - Number of images to generate (default: 1)

**Examples:**
```bash
# Basic generation
python scripts/generate_image.py "A peaceful zen garden"

# With style and quality
python scripts/generate_image.py "Cyberpunk street at night" --style photorealistic --quality high

# With negative prompt
python scripts/generate_image.py "Beach sunset" --negative "crowded, noisy"

# Multiple images
python scripts/generate_image.py "Abstract geometric patterns" --count 4
```

### generate_diagram.py

Generate structured diagrams and visualizations.

**Usage:**
```bash
python scripts/generate_diagram.py "<description>" [options]
```

**Options:**
- `--type` - Diagram type (flowchart, mindmap, architecture, timeline, hierarchy)
- `--output` - Output file path
- `--style` - Visual style (minimal, colorful, professional)

**Examples:**
```bash
# Flowchart
python scripts/generate_diagram.py "E-commerce checkout process" --type flowchart

# Mind map
python scripts/generate_diagram.py "Digital marketing strategies" --type mindmap

# Architecture diagram
python scripts/generate_diagram.py "Microservices API gateway pattern" --type architecture
```

### batch_generate.py

Generate multiple images from a text file.

**Usage:**
```bash
python scripts/batch_generate.py <input_file.txt> --output-dir ./output
```

**Input file format:**
```
A serene mountain landscape
Abstract geometric art
Professional headshot of a doctor
```

## Best Practices

### Prompt Engineering

**Good prompts:**
- Specific details: "A modern glass office building with vertical gardens, photographed at golden hour"
- Style guidance: "Watercolor painting of a cottage garden, soft pastel colors"
- Context: "Minimalist logo design for sustainable fashion brand, leaf motif"

**Be specific:**
```
Good: "Professional business woman presenting to diverse team in modern office"
Vague: "Business meeting"
```

**Include style cues:**
```
"Photorealistic portrait of entrepreneur, studio lighting, 85mm lens"
"Ukiyo-e style print of Mount Fuji, traditional Japanese art"
```

### Style Selection

- **Photorealistic**: Product photos, portraits, real-world scenes
- **Artistic**: Concept art, illustrations, creative visuals
- **Minimalist**: Logos, icons, simple graphics
- **Abstract**: Backgrounds, textures, artistic compositions
- **Cartoon**: Characters, mascots, friendly illustrations

### Quality Settings

- **Standard**: Quick previews, concept iterations
- **High**: Final images, presentations, marketing materials
- **Ultra**: Print-ready, large format, maximum detail

## Troubleshooting

**API Authentication Error**
- Verify API key in `.env` file
- Check API key is valid and active
- Ensure network connectivity

**Image Generation Failed**
- Simplify the prompt
- Check for content policy violations
- Try different style/quality settings

**Poor Quality Results**
- Use more detailed prompts
- Increase quality setting
- Add negative prompts to avoid unwanted elements
- Try different style options

**Slow Generation**
- Reduce quality setting
- Decrease image size
- Check network connection

## Resources

### scripts/
- `generate_image.py` - Main image generation script
- `generate_diagram.py` - Diagram and visualization generator
- `batch_generate.py` - Batch processing for multiple images
- `image_utils.py` - Utility functions for image processing

### references/
- `prompt_guide.md` - Comprehensive prompt engineering guide
- `style_reference.md` - Visual style examples and use cases
- `api_docs.md` - Gemini API documentation

### assets/
- `example_prompts.txt` - Collection of effective prompts
- `style_templates/` - Example prompts for different styles
