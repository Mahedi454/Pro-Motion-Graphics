# Quality Assurance Checklist

## Learning and editorial
- [ ] One clear learning objective.
- [ ] Hook and promise are clear.
- [ ] Definitions and prerequisites are explained.
- [ ] Claims and examples are accurate.
- [ ] Uncertainty and assumptions are visible.
- [ ] No misleading metaphor or chart.
- [ ] Recap reinforces the core model.

## Visual
- [ ] One clear focal point per scene.
- [ ] Cohesive typography, color, grid, and motion.
- [ ] Readable at normal playback and mobile size.
- [ ] No clipping, overlap, overflow, or unsafe-edge placement.
- [ ] Diagrams and labels are correct.
- [ ] Motion supports comprehension.
- [ ] Aspect ratio is intentionally composed.

## Timing and audio
- [ ] Scene durations align with narration.
- [ ] Dense information has enough reading time.
- [ ] Captions are synchronized and readable.
- [ ] No unintended silence or abrupt cuts.
- [ ] Narration is intelligible over music/effects.
- [ ] Audio cues are licensed or original.
- [ ] Every animation, image/graphic change, draw-on, counter and scene change has a matching `<Sfx>` cue; same-type sounds rotate variants.
- [ ] No more than ~3 overlapping sounds; heavy sounds only on hero moments; effects sit under narration.

## Technical
- [ ] Composition dimensions, fps, and duration are correct.
- [ ] Every asset path resolves.
- [ ] Type/build checks pass where available.
- [ ] Preview rendered and inspected, or limitation disclosed.
- [ ] No video was rendered or delivered; the ZIP contains the project and `README-RENDER.md`.
- [ ] ZIP builds with `scripts/package_project.py` and lists no `node_modules` or `out/`.
- [ ] Chosen theme applied (`theme.config.ts`) and every colour comes from `bg/text/accent/hero`.
- [ ] Output filename and format are correct.
- [ ] Source project and README are included where requested.
