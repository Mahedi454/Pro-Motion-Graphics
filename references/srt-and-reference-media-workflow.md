# SRT + Reference Media Workflow

The typical user input is **an SRT file plus reference images and/or videos** (and maybe a topic line). Work from these without asking for more unless something is blocking.

## 1. Intake
- Locate the `.srt` and the media folder (ask only if not found).
- Validate the SRT: `python scripts/srt_to_storyboard.py input.srt production/storyboard.csv --captions src/data/captions.ts --fps 30`.
- The SRT is the timing authority and its text is preserved verbatim in captions and narration. Do not reword cues unless asked. Mention any parse problems (overlapping cues, empty cues, very long cues).
- Any language works. The script reads the encoding and detects script and direction (writes `src/data/language.ts`). On an encoding WARNING, check the text by eye and use `--encoding` if needed. Write all on-screen text in the SRT's language, fill the `label` column in that language, and check a still frame for missing glyphs. See SKILL.md, section "Language".

## 2. Understand the content
Read the full SRT before designing. Write in `production/brief.md`: topic, audience, learning objective, tone, chapters (group of scenes), key terms, numbers/claims needing verification, and the story arc (hook → tension → insight → payoff → recap).

## 3. Analyse the reference media
Run `python scripts/inventory_media.py <media_dir> --out production/media.json --copy-to public/media`.
Then actually look at the files:
- **Images:** open each; note subject, palette, mood, composition, safe crop areas, text legibility, resolution, and style (photo, illustration, screenshot, diagram).
- **Videos:** extract frames (`ffmpeg -i clip.mp4 -vf fps=1/3 frames/clip_%03d.jpg` if ffmpeg exists), watch for motion, shot type, duration, and usable in/out points. Note audio and whether to mute.
- **Style references:** if the images/videos are style references (not content), extract palette, typography feel, pacing, transition style and layer treatment, and encode them in `src/styles/tokens.ts` and the brief. Say which files you treated as style vs content.
- Record rights/ownership. If provenance is unknown, use as the user's supplied reference, flag it in the asset register, and do not claim a license.
- If a file is low resolution, vertical in a landscape project, or visually busy, plan a treatment (blurred-fill background, scrim, crop, rounded card) instead of stretching it.

## 4. Map media to scenes
In the storyboard `assets` column list `file1|file2` (names inside `public/`). Match by meaning first (the image shows what the narration says), then by variety (alternate full-bleed, card, split, picture-in-picture). Every scene needs a visual idea even without media: original diagram, typography, counter, chart. Do not force a reference image into a scene where it does not teach.

## 5. Build
- `python scripts/validate_storyboard.py production/storyboard.csv`
- `python scripts/storyboard_to_scenes.py production/storyboard.csv src/data/scenes.ts`
- Scene kind → template in the starter (`HookScene`, `StatScene`, `StepsScene`, `CompareScene`, `ConceptScene`, `RecapScene`, `MediaScene`); extend or write bespoke scenes for the important beats. The default templates are a floor, not the ceiling: the hook, the "aha" moment and the recap should get custom, hand-designed animation.
- Captions come from `captions.ts` via `<Captions />`; time on-screen keywords to cue starts.
- Apply `references/motion-design-language.md` to every scene: depth layers, staggered reveals, a transition, an ambient layer.

## Caption sync troubleshooting
- Always generate `captions.ts` and `scenes.ts` with the same `--fps` as the composition (default 30). `captions.ts` records `CAPTIONS_FPS` and the component rescales if they differ.
- Captions consistently early/late versus the voice: the audio does not start at the same moment as the SRT (leading silence or trimmed intro). Set `CAPTION_OFFSET_FRAMES` in `src/components/Captions.tsx` (frames; positive = later).
- Drift that grows over time: the SRT was timed for a different audio file/speed than the one in the video. Re-export the SRT from the final audio.
- Check SRT quality first: overlapping cues, cues under 0.3 s, or timestamps past the audio length.
- Word highlighting is estimated from word length, not true word timing; use word-level timestamps if exact karaoke sync is required.

## 6. Verify
Render stills at several frames per scene (`remotion still`), inspect for clipping, caption overlap, unreadable text over media, and mismatches between the visual and the narration. Check total frames equals SRT end. Report limitations honestly.
