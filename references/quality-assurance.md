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
- [ ] Still frames inspected (several per scene type and per language/direction), or limitation disclosed.
- [ ] No video was rendered or delivered; the ZIP contains the project and `README-RENDER.md`.
- [ ] ZIP builds with `scripts/package_project.py` and lists no `node_modules` or `out/`.
- [ ] The theme options were presented as 3 light / 3 dark / 4 colour, each colour's role was explained, and the user's choice (or the stated default) was applied.
- [ ] Chosen theme applied (`theme.config.ts`) and every colour comes from `bg/text/accent/hero`.
- [ ] The ZIP file and the folder inside it are named after the project, and the `production/` notes are inside.
- [ ] Source project and README are included where requested.
