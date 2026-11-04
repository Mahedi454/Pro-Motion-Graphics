# Motion Design Language — modern, eye-catching, educational

Goal: motion that feels like a premium explainer channel (clean, confident, rhythmic) while every move teaches something.

## Principles
1. **Motion = meaning.** Animate to show cause, sequence, change, comparison or emphasis. Never animate just because it is possible.
2. **Hierarchy in time.** Background settles first, the key idea enters next, supporting detail last. One thing moves at a time as the primary focus.
3. **Rhythm.** Animate on the narration: key words land on beats from the SRT. Use a consistent stagger (4–8 frames at 30 fps).
4. **Anticipation, overshoot, settle.** Entrances use a quick ease-out or a damped spring; exits are 30–40% faster than entrances.
5. **Always alive, never busy.** Keep a slow ambient layer (drifting gradient, grid parallax, 1–4% scale push) so held frames never feel frozen; keep it at low contrast.
6. **Depth.** At least three layers per scene: background, subject/diagram, foreground annotations/captions. Parallax them at different speeds.

## Timing table (30 fps)
| Action | Frames | Notes |
|---|---|---|
| Micro feedback (highlight, tick) | 4–8 | snappy |
| Text/element entrance | 12–20 | spring `damping:200` or `damping:14,stiffness:120` for a light pop |
| Stagger between items | 4–8 | keep constant within a group |
| Scene transition | 12–24 | overlap scenes, never hard-cut unless intentional |
| Camera push-in over a scene | whole scene, 3–6% scale | slow, linear-ish ease |
| Number count-up | 30–60 | ease-out, land on the exact value |
| Hold before next idea | ≥ 15 | give the eye time to read |

Reading time: ≥ 0.25 s per word on screen, and ≤ 7 words per keyword block.

## Easing and springs
- Entrance: ease-out (`Easing.out(Easing.cubic)`) or `spring({damping:200})` for a smooth settle.
- Playful emphasis: `spring({damping:12, stiffness:140})`, used rarely.
- Exit: ease-in, short.
- Camera: `Easing.inOut(Easing.sin)` or linear for slow pushes.
- Avoid bouncy springs on serious subjects, equations and data.

## Signature techniques (use a varied mix, 2–3 per scene)
- **Kinetic typography:** words or lines slide + fade in with mask reveal; emphasised words scale, colour or underline on the spoken beat.
- **Animated captions:** active cue highlighted, optional word-level emphasis; keep inside safe area, bottom third, max 2 lines.
- **Mask / wipe reveals:** shapes grow from a point, line draws on (`stroke-dashoffset`), panels slide with clip-path.
- **Draw-on diagrams:** arrows and connectors draw, then nodes pop, then labels appear in causal order.
- **Number counters and animated charts:** bars grow from zero baseline, lines draw left to right, highlight the one value that matters.
- **Morphing / shared element:** the same object transforms between scenes to carry the story (a circle becomes a planet, a node becomes a chart bar).
- **Camera moves:** push-in, drift, pan across a timeline, rack-focus (blur background, sharpen subject), parallax between layers.
- **Reference media treatment:** Ken Burns on images, rounded-corner device/frame cards with soft shadow, video loops with slow-mo or freeze-frame emphasis, duotone/overlay to unify styles.
- **Glass and light:** subtle glass panels, soft glows behind the subject, grain overlay (3–5% opacity), vignette.
- **Match cuts and transitions:** whip pan, shape wipe, zoom-through, colour flood; choose one transition family per video and reuse it.

## Scene-kind recipes
| kind | Recipe |
|---|---|
| hook | Dark open, single bold question or number, push-in, one accent reveal, sound hit. |
| question | Large question text, pause, answer builds in 2–3 steps. |
| stat | Counter animates to the figure; context bar or icon grid makes the scale tangible; label below. |
| steps | Numbered nodes connected by drawing line; active step highlighted in time with narration. |
| compare | Split screen or sliding divider; same axes on both sides; difference highlighted with accent. |
| definition | Term appears large, breaks into parts, each gets a label and a tiny example. |
| quote | Calm typographic scene, attribution fades last. |
| concept | Visual metaphor or diagram with progressive disclosure. |
| recap | 3 key takeaways stacked and checked off in sync with narration, callback to the hook visual. |

## Pacing arc
Open energetic (hook, 0–10 s) → settle into steady explanation → build to the "aha" with the biggest motion and sound moment → calm recap. Vary scene length (4–12 s); avoid ten identical scene shapes in a row.

## Palette and type for energy without noise
- One dominant dark or light base, one primary accent, one warm highlight, neutrals. Use accent only for the thing being taught.
- Headings 72–120 px, body 36–48 px at 1080p; max two font families; weight contrast for hierarchy.
- Safe margins 120 px sides / 90 px top and bottom (landscape); account for platform UI in vertical formats.

## Anti-patterns
Constant whooshes; everything moving at once; text over busy footage without a scrim; bouncy motion on equations; stock-template look repeated each scene; animating decoration while the key word is static; ignoring the narration beat.
