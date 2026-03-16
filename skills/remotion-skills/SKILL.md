---
name: Remotion Video Creator
description: Programmatic video creation using Remotion framework. Use when you want to create, edit, or render videos programmatically with React/TypeScript. Trigger phrases include "create a video with code", "make a Remotion video", "programmatic video generation", "React video", "automated video creation", or "video with Remotion".
---

# Remotion Video Creator

## Overview

Create professional videos programmatically using Remotion - a React-based framework for building videos with code. This skill enables AI-assisted video creation, from simple text animations to complex data-driven visualizations.

## Quick Start

### Installation

```bash
# Initialize a new Remotion project
npm init remotion

# Or install in existing project
npm install remotion @remotion/cli
```

### Basic Video Structure

Every Remotion project needs:
1. **Composition**: The video component (React)
2. **Entry Point**: `Root.tsx` - registers compositions
3. **Configuration**: Defines video settings

**Example Composition:**
```tsx
// src/MyVideo.tsx
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';

export const MyVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  return (
    <AbsoluteFill style={{background: 'white'}}>
      <h1 style={{fontSize: 80}}>
        Frame: {frame}
      </h1>
    </AbsoluteFill>
  );
};
```

**Register Composition:**
```tsx
// src/Root.tsx
import {Composition} from 'remotion';
import {MyVideo} from './MyVideo';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MyVideo"
        component={MyVideo}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
```

## Core Capabilities

### 1. Text & Typography

**Dynamic Text Animation:**
```tsx
import {interpolate, useCurrentFrame} from 'remotion';

export const TextAnimation = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]);
  const scale = interpolate(frame, [0, 60], [0.5, 1]);

  return (
    <h1 style={{
      opacity,
      transform: `scale(${scale})`,
      fontSize: 100
    }}>
      Hello Remotion
    </h1>
  );
};
```

**AI-Generated Scripts:**
Use ChatGPT/Claude to generate video scripts, then convert to Remotion compositions.

### 2. Data Visualization

**Chart Animations:**
```tsx
export const BarChart = ({data}: {data: number[]}) => {
  const frame = useCurrentFrame();
  const progress = Math.min(frame / 60, 1);

  return (
    <div style={{display: 'flex', gap: 20}}>
      {data.map((value, i) => (
        <div
          key={i}
          style={{
            height: value * progress * 5,
            width: 50,
            background: 'blue'
          }}
        />
      ))}
    </div>
  );
};
```

### 3. Audio Integration

**Audio Reactivity:**
```tsx
import {useAudioData, useCurrentFrame} from '@remotion/media-utils';

export const AudioVisualizer = () => {
  const frame = useCurrentFrame();
  const audioData = useAudioData();

  if (!audioData) return null;

  return (
    <div>
      {audioData[frame].map((freq, i) => (
        <div key={i} style={{height: freq * 100}} />
      ))}
    </div>
  );
};
```

### 4. Video Sequencing

**Multi-Scene Videos:**
```tsx
import {Series} from 'remotion';

export const MultiScene = () => {
  return (
    <Series>
      <Series.Sequence durationInFrames={90}>
        <SceneOne />
      </Series.Sequence>
      <Series.Sequence durationInFrames={90}>
        <SceneTwo />
      </Series.Sequence>
    </Series>
  );
};
```

### 5. AI-Enhanced Workflows

**Content-to-Video Pipeline:**
1. Generate script with AI
2. Create Remotion composition
3. Use AI for image generation (DALL-E, Midjourney)
4. AI voiceover (ElevenLabs, Azure TTS)
5. Assemble in Remotion

## Common Video Types

### Social Media Content

**Short Form Video (TikTok/Reels):**
```tsx
// 9:16 vertical video
<Composition
  id="ShortForm"
  component={ShortFormVideo}
  durationInFrames={900} // 30 seconds @ 30fps
  fps={30}
  width={1080}
  height={1920}
/>
```

**YouTube Video:**
```tsx
// 16:9 horizontal video
<Composition
  id="YouTube"
  component={YouTubeVideo}
  durationInFrames={5400} // 3 minutes @ 30fps
  fps={30}
  width={1920}
  height={1080}
/>
```

### Data Videos

**Animated Statistics:**
```tsx
export const StatCounter = ({endValue}: {endValue: number}) => {
  const frame = useCurrentFrame();
  const value = Math.floor(
    interpolate(frame, [0, 60], [0, endValue])
  );

  return <div>{value}</div>;
};
```

### Presentation Videos

**Slide Transitions:**
```tsx
import {Sequence} from 'remotion';

export const Slideshow = () => {
  return (
    <>
      <Sequence from={0} durationInFrames={90}>
        <SlideOne />
      </Sequence>
      <Sequence from={90} durationInFrames={90}>
        <SlideTwo />
      </Sequence>
    </>
  );
};
```

## Animation Techniques

### Interpolation

```tsx
import {interpolate, spring} from 'remotion';

// Linear interpolation
const x = interpolate(frame, [0, 30], [0, 100]);

// Spring animation (bouncy)
const scale = spring({
  frame,
  fps: 30,
  config: {stiffness: 100, damping: 10}
});
```

### Transitions

```tsx
import {AbsoluteFill} from 'remotion';

export const FadeTransition = ({
  children,
  progress
}: {
  children: React.ReactNode;
  progress: number;
}) => {
  return (
    <AbsoluteFill style={{opacity: progress}}>
      {children}
    </AbsoluteFill>
  );
};
```

## Rendering & Export

### Development Preview

```bash
npm start
# Opens browser at http://localhost:3000
```

### Render Video

```bash
# Render MP4
npx remotion render MyVideo out/video.mp4

# Render with custom props
npx remotion render MyVideo out/video.mp4 --props='{"data": [1,2,3]}'

# Render sequence of images
npx remotion render MyVideo out/frame.png --sequence

# Render GIF
npx remotion render MyVideo out/video.gif --codec=gif
```

### Server-Side Rendering

```tsx
import {bundle} from '@remotion/bundler';
import {renderMedia} from '@remotion/renderer';

const bundleLocation = await bundle({
  entryPoint: './src/index.tsx',
  webpackOverride: (config) => config
});

await renderMedia({
  composition: {
    id: 'MyVideo',
    width: 1920,
    height: 1080,
    fps: 30,
    durationInFrames: 300,
    defaultProps: undefined
  },
  outputLocation: 'out/video.mp4',
  inputProps: {},
  codec: 'h264',
  bundleLocation
});
```

## AI Integration Examples

### Script to Video

```tsx
// AI-generated script converted to video
export const ScriptVideo = ({
  script
}: {
  script: {text: string; duration: number}[]
}) => {
  return (
    <>
      {script.map((scene, i) => (
        <Sequence
          key={i}
          from={i * 90}
          durationInFrames={scene.duration}
        >
          <Scene text={scene.text} />
        </Sequence>
      ))}
    </>
  );
};
```

### Dynamic Content

```tsx
// Use AI to generate content based on data
export const DataVideo = ({data}: {data: any[]}) => {
  // AI analyzes data and creates visualization
  const insights = analyzeData(data);

  return (
    <>
      {insights.map((insight, i) => (
        <InsightScene key={i} insight={insight} />
      ))}
    </>
  );
};
```

## Best Practices

### Performance

1. **Lazy Loading**: Load assets only when needed
2. **Frame Calculation**: Pre-calculate expensive operations
3. **Asset Optimization**: Compress images/audio

```tsx
// Good: Pre-calculate
const positions = useMemo(() =>
  data.map((_, i) => calculatePosition(i)),
  [data]
);

// Avoid: Calculate every frame
const position = calculatePosition(frame);
```

### Composition Design

1. **Reusability**: Create reusable components
2. **Configurability**: Use props for customization
3. **Testing**: Test compositions independently

```tsx
// Reusable component
export const Title = ({
  text,
  size = 100,
  color = 'black'
}: {
  text: string;
  size?: number;
  color?: string;
}) => {
  return <h1 style={{fontSize: size, color}}>{text}</h1>;
};
```

## Resources

### scripts/

Helper scripts for common Remotion tasks:
- `setup.sh`: Initialize new Remotion project
- `render.sh`: Batch render multiple videos
- `optimize.sh`: Optimize video output

### references/

- `animations.md`: Common animation patterns and snippets
- `components.md`: Reusable component library
- `integrations.md`: Third-party library integrations (Three.js, D3, etc.)

### assets/

- Templates: Project templates for different video types
- Examples: Example compositions for common use cases

## Troubleshooting

**Common Issues:**

1. **Video not rendering**: Check composition ID matches
2. **Audio out of sync**: Ensure correct fps settings
3. **Performance issues**: Optimize asset sizes and calculations
4. **TypeScript errors**: Update types with `npx remotion upgrade`

**Debug Mode:**
```bash
# Enable verbose logging
DEBUG=* npx remotion render MyVideo out.mp4
```

## When to Use Remotion

✅ **Perfect for:**
- Data-driven videos (reports, dashboards)
- Template-based content (social media, ads)
- Programmatic animation (intros, outros)
- Batch video generation (personalized videos)
- Custom video workflows

❌ **Not ideal for:**
- Simple video editing (use Premiere, Final Cut)
- One-off videos (use traditional editors)
- Live video (use streaming tools)

## Next Steps

1. Explore example compositions in `assets/`
2. Check `references/animations.md` for animation patterns
3. Use AI assistants to generate Remotion code
4. Build reusable component library
5. Create automated video pipelines

---

**This skill enables AI-assisted programmatic video creation. Combine with AI tools (ChatGPT, Claude, DALL-E) for complete video automation.**
