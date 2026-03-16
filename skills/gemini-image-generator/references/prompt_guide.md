# Prompt Engineering Guide for Gemini Image Generation

## Principles of Effective Prompts

### 1. Be Specific and Detailed

**Bad:**
```
A dog
```

**Good:**
```
A golden retriever sitting on a grassy hill, sunset lighting, fluffy fur,
happy expression, detailed fur texture, bokeh background
```

### 2. Include Style and Medium

**Examples:**
- "oil painting of..."
- "watercolor illustration of..."
- "digital art, photorealistic style..."
- "3D render, blender style..."
- "pencil sketch, charcoal drawing..."

### 3. Specify Composition and Framing

**Keywords:**
- **Camera angle:** eye-level, low angle, high angle, bird's eye view
- **Framing:** close-up, medium shot, wide angle, portrait, landscape
- **Focus:** shallow depth of field, sharp focus, soft focus, bokeh

### 4. Describe Lighting

**Lighting types:**
- Natural lighting, golden hour, blue hour
- Studio lighting, softbox, ring light
- Dramatic lighting, chiaroscuro
- Neon lighting, cyberpunk
- Backlit, silhouette

## Prompt Structure Template

```
[Subject] + [Action/Context] + [Style/Medium] + [Lighting] + [Composition] + [Details]
```

**Example:**
```
A mystical forest path + winding through ancient trees + fantasy digital art +
dappled sunlight through leaves + wide angle shot + glowing mushrooms, fireflies,
moss-covered rocks, magical atmosphere
```

## Style Categories

### Photorealistic
- Use for: product photos, portraits, realistic scenes
- Keywords: photorealistic, highly detailed, 8K, professional photography,
  DSLR, sharp focus, natural lighting

### Artistic/Painterly
- Use for: creative visuals, illustrations
- Keywords: oil painting, watercolor, impressionist, abstract expressionist,
  brush strokes, canvas texture

### Digital Art
- Use for: concept art, modern illustrations
- Keywords: digital art, concept art, matte painting, CGI, 3D render,
  blender, octane render

### Minimalist
- Use for: logos, icons, simple designs
- Keywords: minimalist, clean design, simple, flat design,
  vector art, geometric

### Abstract
- Use for: backgrounds, artistic compositions
- Keywords: abstract, surreal, dreamlike, conceptual, artistic interpretation

## Common Mistakes to Avoid

### 1. Too Vague
```
Bad: A nice picture
Good: A serene mountain landscape at sunrise with reflection in lake
```

### 2. Overloading with Contradictions
```
Bad: A realistic cartoon photo of a mythical creature
Good: A stylized illustration of a mythical creature
```

### 3. Missing Important Details
```
Bad: Person working
Good: A focused software engineer working on multiple monitors,
  modern office, keyboard visible, coffee on desk
```

## Advanced Techniques

### Negative Prompts
Specify what you DON'T want:
```
A beautiful beach sunset, negative: crowded, noisy, trash, people
```

### Style Mixing
Combine multiple styles:
```
Japanese ukiyo-e style print of cyberpunk cityscape, traditional woodblock
print aesthetic with neon lights
```

### Artist References (when appropriate)
```
In the style of Studio Ghibli, a cozy cottage in the forest
```

### Technical Specifications
```
Product photography of smartphone, 85mm lens, f/2.8, studio lighting,
white background, professional commercial photography
```

## Examples by Use Case

### Product Photography
```
Professional product shot of wireless headphones, sleek modern design,
studio lighting, white background, 85mm lens, commercial photography,
marketing image
```

### Character Design
```
Fantasy warrior character, female, ornate armor, glowing sword,
determined expression, dynamic pose, digital art, concept art,
dramatic lighting
```

### Landscape/Environment
```
Enchanted forest with bioluminescent plants, mystical atmosphere,
moonlight filtering through trees, fireflies, fantasy art,
highly detailed, cinematic composition
```

### Abstract/Background
```
Abstract fluid art, gradient colors blue and purple, liquid texture,
smooth curves, modern aesthetic, 4K wallpaper, minimalist
```

### Diagram/Technical
```
Clean infographic showing cloud architecture, isometric view, minimalist
design, blue color scheme, professional technical illustration
```

## Testing and Iteration

1. **Start simple** - Basic prompt to get initial result
2. **Add details** - Incrementally add specific elements
3. **Refine** - Adjust based on what works/doesn't work
4. **Experiment** - Try different styles and compositions

## Quick Reference

### Quality Keywords
- High quality, highly detailed, sharp focus, 8K, 4K, HD
- Professional, masterpiece, award-winning

### Lighting Keywords
- Natural, golden hour, blue hour, studio, soft, dramatic
- Backlit, rim lighting, volumetric lighting

### Composition Keywords
- Rule of thirds, centered, symmetrical, dynamic
- Close-up, wide angle, bird's eye view, low angle

### Mood Keywords
- Serene, energetic, mysterious, dramatic, whimsical
- Professional, playful, elegant, rustic, futuristic
