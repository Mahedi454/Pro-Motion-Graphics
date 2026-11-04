# Remotion Production Engineering

## Inspect before implementation
Read `package.json`, lockfile, project scripts, Remotion package versions, entry points, assets, and current conventions. Do not blindly replace project setup or upgrade packages.

## Frame-based animation
Use the installed Remotion APIs. Common primitives include `useCurrentFrame`, `useVideoConfig`, `interpolate`, `spring`, `Sequence`, `Series`, `AbsoluteFill`, `Audio`, and `staticFile`. Verify exact signatures and behavior against installed types/docs.

Convert seconds to frames using the active composition fps. Keep all animation deterministic. Avoid wall-clock timers, random values without seeded determinism, and external network dependencies during rendering.

## Architecture
Separate composition metadata, scenes, reusable visual components, data, tokens, audio, and utilities. Use typed props and scene data. Keep each component focused. Avoid one giant component for an entire film.

## Rendering
Inspect package scripts first. Typical CLI examples, subject to installed version:

```bash
npx remotion compositions src/index.ts
npx remotion preview src/index.ts
npx remotion render src/index.ts Main out/video.mp4
```

Do not assume these paths or commands match every project. Confirm composition ID and entry point.

## Asset strategy
Prefer local assets. Check every referenced path. Use fonts with appropriate licenses. Avoid remote assets that may fail or change during render. Keep asset attribution and license records.

## Performance
Avoid expensive work on every frame. Use stable keys. Keep SVG complexity reasonable. Test large diagrams and long videos. Ensure font loading and image decoding complete before render.

## Audio
Check source duration, sample behavior, trim, volume, fades, and scene alignment. Avoid abrupt cuts. Confirm audio tracks are included in final export.

## Common patterns
```tsx
// Seconds -> frames
const {fps} = useVideoConfig();
const f = (s: number) => Math.round(s * fps);

// Clamped reveal
const o = interpolate(frame, [f(0.2), f(0.8)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

// Smooth, non-bouncy spring
const s = spring({frame, fps, config: {damping: 200}});

// Staggered list
items.map((it, i) => spring({frame: frame - i * 6, fps, config: {damping: 200}}));

// Narration with fade-in
<Audio src={staticFile('audio/narration/main.mp3')} volume={(fr) => interpolate(fr, [0, 15], [0, 1], {extrapolateRight: 'clamp'})} />
```
Use `Series` for back-to-back scenes and `Sequence from` when timing comes from storyboard/SRT data. Use `Img` (not `<img>`) and load fonts via `@remotion/google-fonts` or local `@font-face` so assets are ready before capture.

## Troubleshooting
- Blank frames: missing background or a failed asset load; check the `remotion studio` console.
- Audio missing in render: file must be in `public/` and referenced via `staticFile`.
- Text overflow in vertical formats: recompose; do not scale landscape layouts.
- Slow render: reduce SVG node counts, avoid large blur filters, lower `--concurrency` if memory runs out.
- Duration mismatch: derive `durationInFrames` from scene data, never hard-code.
- Quick visual check without a full render: `npx remotion still src/index.ts Main out/frame.png --frame=<n>`.

## Delivery
Claude does not render or deliver the final video. Deliver the complete project as a ZIP (`scripts/package_project.py`) with `README-RENDER.md`. Record the exact composition ID (`Main`), dimensions, fps, frame count, duration, theme, and the render command (`npm run render` -> `out/video.mp4`) in the instructions. Verify with `tsc` and a few stills; never claim a render happened.
