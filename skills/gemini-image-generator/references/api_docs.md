# Gemini API Reference for Image Generation

## Overview

This skill uses Google's Gemini API for image generation and diagram creation. The API key is pre-configured in the `.env` file.

## API Configuration

### Environment Variables

```env
GEMINI_API_KEY=AIzaSyD5LqX5M6n3ppjhOBnOlfRL2ohk1-j3b6E
DEFAULT_OUTPUT_DIR=./output
DEFAULT_STYLE=photorealistic
DEFAULT_QUALITY=standard
IMAGE_SIZE=1024x1024
```

### Installation

Required Python packages:
```bash
pip install google-generativeai python-dotenv Pillow
```

## API Models

### Gemini Pro

Text-based model for generating descriptions and specifications:

```python
import google.generativeai as genai

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("Your prompt here")
print(response.text)
```

## Image Generation Capabilities

Note: As of the current implementation, Gemini API is primarily used for text generation. For actual image generation, consider:

1. **Text-to-Image Description**: Use Gemini to create detailed image descriptions
2. **Diagram Specifications**: Generate structured specifications for diagrams
3. **Prompt Enhancement**: Improve and refine image generation prompts

## Implementation Notes

### Current Limitations

The current implementation generates text-based specifications and descriptions. For actual visual output, you would need:

1. **Image Generation API**: Integration with a dedicated image generation service
2. **Diagram Rendering**: Use diagramming libraries (Mermaid, PlantUML, Graphviz)
3. **Visual Creation**: Graphics generation tools or services

### Alternative Image Generation Services

If you need actual image generation, consider integrating:

- **DALL-E API**: OpenAI's image generation
- **Stable Diffusion**: Open-source image generation
- **Midjourney**: API access where available
- **Imagen**: Google's image generation model

## Example Integration Pattern

```python
import google.generativeai as genai

# Configure
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Generate image description
prompt = """
Describe in detail an image of a serene mountain landscape at sunset.
Include composition, lighting, colors, and mood.
"""

response = model.generate_content(prompt)
image_description = response.text

# Use description with image generation service
# generate_image(description)
```

## Best Practices

### Prompt Design
- Be specific and detailed
- Include style and medium preferences
- Specify composition and lighting
- Describe mood and atmosphere

### Error Handling
```python
try:
    response = model.generate_content(prompt)
except Exception as e:
    print(f"API Error: {e}")
    # Handle error appropriately
```

### Rate Limiting
- Implement appropriate delays between requests
- Cache responses when possible
- Use batch operations for multiple generations

## API Response Structure

```python
response = model.generate_content(prompt)

# Access generated text
text = response.text

# Check for safety ratings
if hasattr(response, 'candidates'):
    for candidate in response.candidates:
        print(candidate.finish_reason)
        if hasattr(candidate, 'safety_ratings'):
            for rating in candidate.safety_ratings:
                print(f"{rating.category}: {rating.probability}")
```

## Diagram Generation Workflow

### 1. Create Specification
Use Gemini to generate detailed diagram structure:

```python
prompt = f"""
Create a flowchart specification for: {description}

Include:
- All steps and decision points
- Connections and flow arrows
- Labels and text
- Layout recommendations
"""

response = model.generate_content(prompt)
specification = response.text
```

### 2. Render with Diagramming Tool

Convert specification to visual diagram:

**Mermaid.js Example:**
```
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```

**PlantUML Example:**
```
@startuml
start
:Step 1;
if (Condition?) then (yes)
  :Action 1;
else (no)
  :Action 2;
endif
stop
@enduml
```

## Troubleshooting

### Common Errors

**API Key Invalid**
```
Error: API key not valid
Solution: Check GEMINI_API_KEY in .env file
```

**Quota Exceeded**
```
Error: Quota exceeded
Solution: Wait or upgrade API tier
```

**Content Policy Violation**
```
Error: Content policy violation
Solution: Modify prompt to comply with policies
```

### Debugging

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check API status:
```python
# Test connection
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Hello")
print(response.text)
```

## Resources

- [Google AI Studio](https://makersuite.google.com/) - Interactive testing
- [Gemini API Documentation](https://ai.google.dev/docs) - Official docs
- [Python SDK Reference](https://ai.google.dev/python) - Python library docs
- [Prompt Guidelines](https://ai.google.dev/prompt-guide) - Prompt engineering

## Future Enhancements

Potential improvements for this skill:

1. **Direct Image Generation**: Integrate with Imagen or other image APIs
2. **Batch Processing**: Optimize for multiple generations
3. **Style Templates**: Pre-configured style presets
4. **Image Editing**: Modification and refinement capabilities
5. **Interactive Refinement**: Iterative improvement workflow
