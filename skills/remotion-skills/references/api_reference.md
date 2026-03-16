# Remotion API Reference

Complete reference for Remotion framework APIs and common patterns.

## Core Hooks

### useCurrentFrame()

Returns the current frame number (0-indexed).

```tsx
import {useCurrentFrame} from 'remotion';

const MyComponent = () => {
  const frame = useCurrentFrame();
  return <div>Frame: {frame}</div>;
};
```

**Use cases:**
- Frame-based animations
- Timing calculations
- Progress tracking

### useVideoConfig()

Returns video configuration settings.

```tsx
import {useVideoConfig} from 'remotion';

const MyComponent = () => {
  const {fps, width, height, durationInFrames} = useVideoConfig();
  return <div>{width}x{height} @ {fps}fps</div>;
};
```

**Returns:**
- `fps`: Frames per second
- `width`: Video width in pixels
- `height`: Video height in pixels
- `durationInFrames`: Total duration

### AbsoluteFill

Component that fills the entire video frame.

```tsx
import {AbsoluteFill} from 'remotion';

<AbsoluteFill style={{background: 'blue'}}>
  <div>Content</div>
</AbsoluteFill>
```

### interpolate()

Interpolates values based on frame.

```tsx
import {interpolate} from 'remotion';

const opacity = interpolate(
  frame,
  [0, 30],      // Input range
  [0, 1],       // Output range
  {extrapolateRight: 'clamp'}  // Options
);
```

**Options:**
- `extrapolateLeft`: Behavior before input range
- `extrapolateRight`: Behavior after input range
- `easing`: Easing function

## Animation APIs

### spring()

Spring-based animation (bouncy, natural).

```tsx
import {spring} from 'remotion';

const scale = spring({
  frame,
  fps: 30,
  config: {
    stiffness: 100,  // Stiffness (0-300)
    damping: 10,     // Damping (0-50)
    mass: 1          // Mass (0-10)
  }
});
```

###_timing()_Timing-based animation

```tsx
import {timing} from 'remotion';

const value = timing({
  frame,
  fps: 30,
  durationInFrames: 30  // Animation duration
});
```

## Sequence & Series

### Sequence

Display components for specific frame ranges.

```tsx
import {Sequence} from 'remotion';

<Sequence from={0} durationInFrames={90}>
  <SceneOne />
</Sequence>
<Sequence from={90} durationInFrames={90}>
  <SceneTwo />
</Sequence>
```

**Props:**
- `from`: Start frame
- `durationInFrames`: Duration
- `name`: Optional name for debugging

### Series

Sequential playback helper.

```tsx
import {Series} from 'remotion';

<Series>
  <Series.Sequence durationInFrames={90}>
    <SceneOne />
  </Series.Sequence>
  <Series.Sequence durationInFrames={90}>
    <SceneTwo />
  </Series.Sequence>
</Series>
```

## Audio Hooks

### useAudioData()

Extract audio data for visualization.

```tsx
import {useAudioData} from '@remotion/media-utils';

const AudioViz = () => {
  const audioData = useAudioData();

  if (!audioData) return null;

  return (
    <div>
      {audioData.map((channel, i) => (
        <div key={i}>
          {channel.map((sample, j) => (
            <div key={j} style={{height: sample * 100}} />
          ))}
        </div>
      ))}
    </div>
  );
};
```

### useAudioFrame()

Sync audio with video frames.

```tsx
import {useAudioFrame} from '@remotion/media-utils';

const frame = useAudioFrame();  // Audio-synced frame number
```

## Rendering APIs

### renderMedia()

Server-side video rendering.

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
    durationInFrames: 300
  },
  outputLocation: 'out/video.mp4',
  inputProps: {},
  codec: 'h264',
  bundleLocation
});
```

### renderStill()

Render single frame as image.

```tsx
import {renderStill} from '@remotion/renderer';

await renderStill({
  composition,
  outputLocation: 'still.png',
  inputProps: {}
});
```

## Composition Registration

### Root Component

Register all compositions.

```tsx
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
        defaultProps={{title: "Hello"}}  // Default props
      />
    </>
  );
};
```

## Common Patterns

### Fade In/Out

```tsx
export const FadeInOut = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(
    frame,
    [0, 30, 270, 300],  // Keyframes
    [0, 1, 1, 0],       // Opacity values
    {extrapolateRight: 'clamp', extrapolateLeft: 'clamp'}
  );

  return (
    <AbsoluteFill style={{opacity}}>
      <div>Content</div>
    </AbsoluteFill>
  );
};
```

### Slide In

```tsx
export const SlideIn = () => {
  const frame = useCurrentFrame();
  const x = interpolate(frame, [0, 30], [-1920, 0]);

  return (
    <div style={{
      transform: `translateX(${x}px)`,
      position: 'absolute'
    }}>
      Content
    </div>
  );
};
```

### Scale Animation

```tsx
export const ScaleUp = () => {
  const frame = useCurrentFrame();
  const scale = spring({
    frame,
    fps: 30,
    config: {stiffness: 100, damping: 10}
  });

  return (
    <div style={{
      transform: `scale(${scale})`,
      transformOrigin: 'center'
    }}>
      Content
    </div>
  );
};
```

### Rotate Animation

```tsx
export const Rotate = () => {
  const frame = useCurrentFrame();
  const rotation = interpolate(frame, [0, 300], [0, 360]);

  return (
    <div style={{
      transform: `rotate(${rotation}deg)`
    }}>
      Content
    </div>
  );
};
```

### Text Typewriter

```tsx
export const Typewriter = ({text}: {text: string}) => {
  const frame = useCurrentFrame();
  const charIndex = Math.floor(frame / 2);  // 2 frames per char
  const visibleText = text.slice(0, charIndex);

  return <div>{visibleText}</div>;
};
```

### Counter Animation

```tsx
export const Counter = ({end}: {end: number}) => {
  const frame = useCurrentFrame();
  const value = Math.floor(
    interpolate(frame, [0, 60], [0, end])
  );

  return <div>{value}</div>;
};
```

## Component Patterns

### Reusable Animation Component

```tsx
interface AnimatedProps {
  children: React.ReactNode;
  delay?: number;
  duration?: number;
}

export const FadeIn: React.FC<AnimatedProps> = ({
  children,
  delay = 0,
  duration = 30
}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(
    frame,
    [delay, delay + duration],
    [0, 1],
    {extrapolateRight: 'clamp'}
  );

  return (
    <div style={{opacity}}>
      {children}
    </div>
  );
};
```

### Layout Component

```tsx
export const VideoLayout: React.FC = ({
  title,
  content
}) => {
  return (
    <AbsoluteFill style={{background: '#fff'}}>
      <div style={{
        padding: 100,
        height: '100%',
        display: 'flex',
        flexDirection: 'column'
      }}>
        <h1 style={{fontSize: 80}}>{title}</h1>
        <div style={{flex: 1}}>
          {content}
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

## Performance Optimization

### useMemo for Expensive Calculations

```tsx
import {useMemo} from 'react';

export const ExpensiveComponent = ({data}: {data: number[]}) => {
  const positions = useMemo(() =>
    data.map((_, i) => calculatePosition(i)),
    [data]
  );

  return <div>{/* use positions */}</div>;
};
```

### Static Assets Preloading

```tsx
import {staticFile} from 'remotion';

<img src={staticFile('image.png')} />
```

### Frame Calculation Caching

```tsx
// Good: Calculate once
const values = useMemo(() => {
  return Array.from({length: 300}, (_, i) =>
    calculateValue(i)
  );
}, []);

// Use in component
const value = values[frame];
```

## Type Safety

### Defining Props

```tsx
interface MyVideoProps {
  title: string;
  subtitle?: string;  // Optional
  data: number[];
}

export const MyVideo: React.FC<MyVideoProps> = ({
  title,
  subtitle,
  data
}) => {
  return (
    <AbsoluteFill>
      <h1>{title}</h1>
      {subtitle && <h2>{subtitle}</h2>}
    </AbsoluteFill>
  );
};
```

### Composition Props Type

```tsx
import {Composition} from 'remotion';

<Composition
  id="MyVideo"
  component={MyVideo}
  durationInFrames={300}
  fps={30}
  width={1920}
  height={1080>
  defaultPropsProps={{
    title: "Hello",
    data: [1, 2, 3]
  }}
/>
```

## CLI Commands

### Development

```bash
# Start dev server
npm start

# Specify port
npm start -- --port 3001
```

### Rendering

```bash
# Render composition
npx remotion render MyVideo output.mp4

# Render with props
npx remotion render MyVideo output.mp4 --props='{"title":"Hello"}'

# Render specific frames
npx remotion render MyVideo output.mp4 --frames=0-100

# Render image sequence
npx remotion render MyVideo output/frame.png --sequence

# Override codec
npx remotion render MyVideo output.mp4 --codec=prores
```

### Server Rendering

```bash
# Start lambda server
npx remotion lambda server

# Render on lambda
npx remotion lambda render MyVideo
```

## Troubleshooting

### Common Errors

**"Composition not found"**
- Check composition ID matches
- Verify Root.tsx exports composition

**"Audio out of sync"**
- Ensure fps matches across components
- Check audio file sample rate

**"Performance issues"**
- Use useMemo/useCallback
- Optimize image sizes
- Reduce complex calculations

**"TypeScript errors"**
- Run `npx remotion upgrade`
- Check @types/remotion installed
- Verify tsconfig.json

## Best Practices

1. **Use TypeScript** for type safety
2. **Component modularity** for reusability
3. **Props for configurability** over hardcoding
4. **Memoization** for performance
5. **Frame-based** over time-based animations
6. **Test compositions** in isolation
7. **Optimize assets** before importing

## Resources

- Official docs: https://www.remotion.dev/docs
- GitHub: https://github.com/remotion-dev/remotion
- Discord: https://discord.gg/7rVnDgJH4N
- Examples: https://github.com/remotion-dev/remotion/tree/main/examples
