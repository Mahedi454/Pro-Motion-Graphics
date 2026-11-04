# Sound Design System: every motion gets its own sound

Rule: **whenever something on screen changes (an animation starts, an image or graphic appears, a diagram draws, a number counts, a scene changes) a sound that matches that kind of motion plays with it. Different kinds of motion get different sounds, and repeats of the same kind never sound identical.**

All effects are original and royalty-free: they are synthesized by `scripts/generate_sfx.py` (no copyrighted audio). The starter already contains the generated library in `public/audio/sfx/` (49 files) and the typed list in `src/audio/sfx.generated.ts`. Regenerate only if you change the library.

## Sound types (12) and when to use each
| Motion event | Sound | Why it fits |
|---|---|---|
| Scene change / transition | `whoosh` (long sweep) or `swipe` (short), alternating scene by scene | air movement across the cut |
| Hook: tension, then headline lands | `riser` -> `hit` | build, then impact |
| Hero moment, number lands, divider settles | `hit` (heavy), lower volume for secondary | weight |
| Element or node appears | `pop` | small bubble pop |
| List item / step highlight moves | `tick` | precise, light |
| Words of kinetic text appear | `click` (soft, pitch varies per word) | typing feel |
| Image / video / media reveals | `sparkle` | shimmer for visual content |
| Line, arrow, outline, diagram draws on | `draw` | soft sweep that follows the stroke |
| Number counting up | `counter` ticks, pitch rising with the value | rising count |
| Success / checklist / correct answer | `chime`, variants 0..4 ascending (pentatonic) | satisfying and always in tune |
| Diagram / ambient emphasis | `swell` | soft pad under growing shapes |
| Panel slides in (compare, cards) | `swipe`, a different variant for each panel | direction and speed |

Choose by what the motion *does*, not by scene number: slide -> swipe/whoosh, appear -> pop, draw -> draw, grow/count -> counter/swell, land/impact -> hit, reveal image -> sparkle, success -> chime.

## Variation (no two sounds the same)
- Each type has 4-5 variants with different pitch, sweep direction and timbre. `<Sfx seed={n} />` rotates through them, so use a changing seed (scene number + item index).
- A small deterministic pitch jitter (about 6%) is added automatically. Pass `rate` to set the pitch yourself (for example rising pitch while counting).
- The next scene must not start with the same variant as the previous one: seed with the scene number.
- Renders are deterministic: the same project always produces the same audio.

## Using it in code
```tsx
import {Sfx, sceneNo} from '../components/Sfx';
<Sfx name="pop" at={20} seed={sceneNo(scene.id) + i} />          // at = scene-local frame
<Sfx name="chime" at={30} variant={2} />                          // force a specific variant
<Sfx name="counter" at={6 + i * 4} rate={0.85 + i * 0.06} />      // pitch climbs
```
- `at` is a frame inside the current scene (Sequence). Put the cue on the frame the motion starts (or lands, for impacts).
- Built-in templates already add cues: scene transitions (SceneShell), kinetic text (KineticText), media reveals (MediaFrame), and every scene type. **Any bespoke scene or new animation you write must add its own cues with the table above.**
- Bespoke animation checklist: every new entrance, exit, draw-on, counter, image/graphic change has a cue; no two consecutive cues use the same variant; no more than 3 sounds overlapping.

## Mixing rules
- Narration is the primary audio. Effects sit under it: default volumes are 0.18-0.55 and the master level is `SFX_VOLUME` (0.7) in `src/audio/config.ts`.
- Do not trigger more than about 3 sounds per second apart from fast counters and word clicks (those are very quiet).
- Leave silence on purpose: a calm explanation scene needs only its transition and one or two accents.
- Heavy sounds (`hit`, `riser`) are for hero moments only: at most once per scene, not every scene.
- To mute all effects: `SFX_ENABLED = false` in `src/audio/config.ts`.
- Music is separate and optional (user-supplied or licensed only). Never add copyrighted sounds.

## Verification
Claude cannot listen. Verify technically and say so: the project builds, `Sfx` cues exist for each animated element, and a short test render (for example `--frames=0-150`, never delivered) contains an audio track whose energy peaks line up with the cues. Never claim to have judged how it sounds.
