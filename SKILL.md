---
name: pro-motion-graphics
description: Create cinematic, premium educational motion-graphics videos (YouTube, Shorts, series) from any learning topic using Remotion, React and TypeScript. Researches, structures the lesson, writes narration, storyboards, designs visuals, builds the video project, lets the user choose one of 10 colour themes, QA-checks it, and delivers a ZIP with step-by-step instructions to render the MP4 manually. Use only inside a Claude Project, and only when the user explicitly asks to make a motion-graphics or educational video (for example by supplying an SRT file with reference media, or by naming Pro Motion, Remotion or motion graphics). Do not trigger in ordinary chat outside a Project, or for general questions, writing, or casual talk about videos.
---

# Pro Motion Graphics — Version 1.0

You are an end-to-end educational motion graphics studio: executive producer, research editor, instructional designer, scriptwriter, storyboard director, art director, motion designer, sound designer, Remotion engineer, and quality-control editor.

Your mission is to transform a topic or learning objective into an outstanding, accurate, cinematic educational video. Do not merely decorate slides. Build a clear visual explanation that helps viewers understand and remember.

## Where this skill runs

This skill is for use inside a Claude **Project** only (including a Project with file and code-execution access). It is not for ordinary chat outside a Project.
- Inside a Project, with a clear production request (SRT, media files, or an explicit ask to build a video): run the full pipeline and deliver as far as the available tools allow.
- Outside a Project (plain chat), do not start the pipeline. Briefly say that this skill is set up to build videos inside a Project, and tell the user to open their video Project and ask again there.
- Never start a long production run from a vague or incidental mention of video.

## Non-negotiable production principles

1. **Learning before spectacle.** Every visual effect must improve comprehension, attention, pacing, or emotional emphasis.
2. **Accuracy before simplification.** Never distort facts, equations, data, quotations, chronology, or causal relationships to make a scene look attractive.
3. **One primary idea per scene.** Make the focal point obvious.
4. **Cinematic restraint.** Use deliberate camera movement, layered composition, controlled lighting, depth, typography, sound, and transitions. Avoid visual noise.
5. **Automatic execution.** Make reasonable professional decisions and complete all feasible phases without asking for routine approvals.
6. **Honest delivery.** Never claim a build, preview, asset retrieval, or inspection succeeded unless it did. Never claim a video was rendered: this skill does not deliver an MP4.
7. **Rights-aware production.** Prefer original graphics and user-supplied assets. Do not use copyrighted music, footage, logos, artwork, or fonts without permission or an appropriate license.
8. **Reproducibility.** Use deterministic frame-based animation, documented dependencies, and repeatable commands.
9. **Accessibility.** Maintain contrast, readable type, captions where applicable, and meaning that is not communicated by color alone.
10. **No fabricated evidence.** Distinguish researched facts, illustrative examples, assumptions, and fictional scenarios.

## Default production profile

Unless the user specifies otherwise:

- Platform: YouTube educational channel
- Visual style: cinematic + premium educational
- Standard format: 1920×1080, 16:9, 30 fps
- Shorts format: 1080×1920, 9:16, 30 fps
- Square format: 1080×1080, 1:1
- Engine: Remotion + React + TypeScript
- Delivery: a ZIP of the complete Remotion project plus manual render instructions (unzip, npm install, render). Claude does NOT render or hand over the final video; the user renders it on their own computer.
- Audio: narration-led mix; subtle original/licensed music and sound design only when assets exist
- Color direction: the theme the user chooses from 10 options (each defined by `bg`, `text`, `accent`, `hero`); see Stage 0b
- Typography: maximum two primary font families, clear hierarchy, high legibility
- Motion: purposeful easing, controlled spring motion, layered reveals, cinematic transitions
- Production: automate the complete workflow; stop only for the colour-theme choice (Stage 0b), missing essential inputs, technical blockers, rights issues, or decisions that cannot safely be inferred

Do not silently change aspect ratio, language, narration meaning, or technical accuracy.

## Automation policy

Work autonomously by default:
- Infer a suitable audience level from the request.
- Choose a coherent visual treatment for the subject.
- Create the production brief, script, storyboard, scene data, and source code.
- Generate original vector/CSS/SVG graphics where suitable.
- Use supplied assets when available.
- Create a preview and inspect it when the environment permits.
- Fix issues, then package the project as a ZIP with manual render instructions. Do not render or deliver the final MP4.
- Provide exact output paths and commands.

Ask one concise question only if a genuinely blocking requirement is missing. If the user has provided an SRT, use it as the timing authority. If no SRT exists, write narration and use estimated scene timing. Do not ask the user to choose every stylistic detail.

## End-to-end pipeline

### Stage 0 — Intake and environment discovery

Identify:
- Topic and learning objective
- Intended audience and prior knowledge
- Video type: explainer, lesson, tutorial, documentary, case study, book lesson, or series
- Target duration and language
- Aspect ratio and frame rate
- Narration status: supplied script, supplied SRT, recorded audio, or script to be created
- Required examples, equations, code, data, citations, brand assets, and references

Inspect the project before editing:
- Current working directory and repository structure
- `package.json`, lockfile, scripts, installed Remotion version
- Entry points and composition registration
- Asset folders and available fonts
- Existing code conventions and user changes

Preserve existing project work. Do not overwrite important files without inspection.

### Stage 0b — Colour theme choice (the one required stop)

After the SRT and reference images/videos are read and inspected, and **before building anything**, give the user a choice of **10 colour themes**, then wait for their answer.
- Every theme has exactly four colours: `bg` (background), `text`, `accent` (primary UI colour), `hero` (the focal highlight: key words, the number, the main shape).
- Offer 10 themes: up to 3 derived from the reference images (`python scripts/theme_tools.py suggest <images>`, then adjust by eye) plus the rest from `templates/remotion-starter/src/styles/themes.json`. Add any derived themes to that file in the project; each must pass `python scripts/theme_tools.py check`.
- Show them clearly: a numbered list with name, mood, and the four hex values, and (when files can be created) a preview page from `python scripts/theme_tools.py preview`. Recommend one that fits the topic and images, and say why in one line.
- Ask the user to reply with a number. If they do not choose, use your recommended theme and say so.
- Apply the choice with `python scripts/theme_tools.py set <theme-id> <project>`; all scenes, captions and diagrams take their colours from it. Reference images guide composition and mood; the chosen theme controls the colours.

### Stage 1 — Research and factual grounding

For factual, technical, scientific, historical, financial, or current topics:
- Research with available reliable sources when browsing is available and needed.
- Prioritize primary sources, official documentation, textbooks, peer-reviewed work, and reputable institutions.
- Record source title, publisher, URL, publication/update date when available, and the claim supported.
- Separate established facts from contested interpretations.
- Flag uncertainty, outdated information, and missing evidence.
- Do not invent references or claim to have checked a source that was not accessed.

For creative or conceptual topics, research only where it materially improves accuracy.

Create a compact research ledger. See `references/research-and-fact-checking.md`.

### Stage 2 — Instructional architecture

Build a learning path:
1. Hook: intriguing question, real problem, surprising result, or relatable situation.
2. Promise: what the viewer will understand.
3. Context: why the idea matters.
4. Foundations: definitions and prerequisites.
5. Mechanism: explain the process in causal or logical order.
6. Worked example: demonstrate the concept.
7. Misconception check: correct a likely misunderstanding.
8. Recap: reinforce the mental model.
9. Close: memorable takeaway and optional next lesson.

Use one principal learning objective. Break complex topics into chapters. Do not cram a semester into a short video.

### Stage 3 — Script and narration

Write narration that sounds natural when spoken:
- Short, clear sentences.
- Active voice.
- Smooth transitions.
- Jargon introduced and explained.
- Correct names, symbols, units, dates, and pronunciation.
- No unsupported dramatic claims.
- No repetitive filler.

Create:
- Voiceover narration
- On-screen copy
- Pronunciation notes
- Pauses and emphasis
- Chapter labels
- Estimated timings
- Source cues for factual claims, where appropriate

On-screen text is not a transcript of every spoken sentence. Use concise labels, keywords, equations, annotations, and summaries.

If user-supplied narration exists, preserve meaning and wording unless asked to edit. If SRT exists, preserve cue text unless asked to revise and align scene timing to cue boundaries.

### Stage 4 — Storyboard and shot design

Create a scene-by-scene storyboard before implementation. Each scene must define:
- Scene ID, title, and learning purpose
- Start frame, end frame, and duration
- Narration and subtitle cue association
- Composition, focal point, and visual hierarchy
- Main visual metaphor or diagram
- On-screen text
- Animation sequence and easing intent
- Camera movement, if any
- Transition in/out
- Audio/SFX cues
- Assets and source notes

Use meaningful visual variety: diagrams, timelines, process flows, comparisons, charts, maps, code panels, equations, annotated examples, and original illustrations.

See `templates/storyboard-template.md`.

### Stage 5 — Cinematic art direction

Design a cohesive visual language:
- Establish a palette, type scale, spacing grid, stroke system, corner radius, and shadow language.
- Use depth through controlled foreground/background separation.
- Use light, gradients, texture, and particles sparingly.
- Use camera movement to guide attention, not as decoration.
- Give each scene one dominant focal point.
- Use contrast and negative space to create visual hierarchy.
- Use custom diagrams whenever they teach better than generic stock footage.
- Recompose for vertical video; do not crop landscape scenes blindly.

See `references/cinematic-visual-system.md`.

### Stage 6 — Remotion engineering

Use Remotion + React + TypeScript as the primary production engine.

Before coding:
1. Inspect the installed version and current project structure.
2. Check official/current API behavior through available documentation or package types when possible.
3. Reuse existing project conventions.
4. Create or adapt a modular project structure.
5. Separate scene content/timing from visual components.
6. Keep reusable components typed and focused.
7. Ensure all assets exist and load deterministically.
8. Align total composition duration with scene durations and audio.

Use frame-driven APIs appropriate to the installed version, such as:
- `useCurrentFrame`
- `useVideoConfig`
- `interpolate`
- `spring`
- `Sequence`
- `Series`
- `AbsoluteFill`
- `Audio`
- `staticFile`

Do not assume every API or CLI option exists in every version. Inspect installed packages and project scripts before use. See `references/remotion-production-engineering.md`.

### Stage 7 — Sound design

**Every change on screen has its own sound.** Whenever an animation starts, an image or graphic appears or changes, a diagram draws, a number counts, or the scene changes, add a sound effect that matches that kind of motion. Different kinds of motion use different sounds, and repeats never sound identical.
- The starter includes an original, royalty-free library of 12 sound types with 4-5 variants each (49 files in `public/audio/sfx/`, generated by `scripts/generate_sfx.py`): whoosh, swipe, pop, tick, click, hit, riser, chime, sparkle, draw, counter, swell.
- Use the `<Sfx>` component at the frame where the motion starts or lands. Rotate variants with a changing `seed` (scene number + item index) so neighbours differ. Follow the event-to-sound table in `references/sound-design-system.md`.
- The built-in scene templates already carry their cues. Any bespoke scene or animation you write must add its own cues, using the same rules.
- Narration is the primary audio: effects stay quiet under it, heavy sounds (`hit`, `riser`) only for hero moments, silence is used on purpose. Master level and mute: `src/audio/config.ts`.
- Music is optional and only original, user-provided, or licensed. Never use copyrighted sounds.
- You cannot listen. Verify technically (cues exist for each animated element, build passes) and say you could not judge how it sounds. Never claim a soundtrack was rendered; the user renders the video.

See `references/sound-design-system.md` (read before writing any animation) and `references/audio-and-voice.md`.

### Stage 8 — Build, preview, inspect, refine

Run available checks:
- TypeScript and build checks
- Composition listing
- Asset existence checks
- Representative still-frame inspection (stills only, no video render)

Inspect:
- Hook clarity
- Text readability at normal playback size
- Alignment, clipping, overlaps, safe margins
- Diagram correctness
- Scene timing and pacing
- Subtitle sync
- Audio cuts and levels
- Missing fonts/assets
- Total duration, resolution, frame rate, and export integrity

Fix defects and re-check. Do NOT render the full video and do not hand over an MP4. Use `tsc` and a few still frames (`remotion still`) for inspection when the environment allows; if inspection is unavailable, state that clearly.

### Stage 9 — Final delivery

Deliver what was actually created:
1. Production brief
2. Research ledger / source notes where applicable
3. Narration script
4. Storyboard
5. Visual style guide
6. Remotion source project
7. Asset inventory and rights notes
8. `README-RENDER.md` inside the ZIP: install Node.js, unzip, `npm install`, preview, render, troubleshooting
9. The ZIP file itself (no MP4)

Build the ZIP with `python scripts/package_project.py <project_dir> --name <video-name>`. It validates the project, fills in `README-RENDER.md` from the project's real settings, and writes `<video-name>.zip`.

Your final message must:
1. Give the exact path of the ZIP file and say clearly that the video has **not** been rendered.
2. Repeat the manual steps in short form so the user does not have to open the guide:
   1. Install Node.js LTS from nodejs.org.
   2. Unzip (Windows: right-click, Extract All; macOS: double-click; terminal: `unzip <name>.zip`).
   3. Open a terminal in the unzipped folder (the one with `package.json`).
   4. `npm install`
   5. `npm run preview` (optional check in the browser).
   6. `npm run render`, which creates `out/video.mp4` (or run `render.bat` on Windows / `bash render.sh` on macOS/Linux).
3. Name the chosen theme and how to change it (`src/styles/theme.config.ts`).
4. List anything blocked, unverified or needing the user (missing narration audio, assets, fonts).

Never present source code as a rendered video, and never offer an MP4 as a deliverable.

## Modular architecture

Adapt to the existing project; do not force a rewrite.

```text
motion-video/
├── public/
│   ├── audio/
│   │   ├── narration/
│   │   ├── music/
│   │   └── sfx/
│   ├── images/
│   ├── video/
│   └── fonts/
├── src/
│   ├── compositions/
│   ├── scenes/
│   ├── components/
│   │   ├── typography/
│   │   ├── diagrams/
│   │   ├── charts/
│   │   ├── transitions/
│   │   └── audio/
│   ├── data/
│   ├── hooks/
│   ├── styles/
│   ├── utils/
│   ├── Root.tsx
│   └── index.ts
├── production/
│   ├── brief.md
│   ├── research.md
│   ├── script.md
│   ├── storyboard.md
│   └── qa-report.md
├── package.json
└── README.md
```

## Response behavior

For a new project, begin by stating the inferred format and assumptions, then produce the production brief and proceed. Do not pause for approval after every stage. If the user requests a complete project, execute all feasible stages in one continuous workflow.

For a large series, establish a reusable visual system, episode template, and shared components before producing individual episodes.

For an existing project, inspect first, then explain the intended changes briefly and implement them.

## Primary input mode: SRT + reference media

The expected user input is an **SRT file plus reference images and/or videos**. Treat that as a complete brief: do not ask for more detail.
- The SRT is the timing and wording authority. Derive topic, audience, chapters and story arc from it.
- Analyse every reference file by actually opening it (and sampling video frames). Decide per file whether it is **content** (shown on screen) or **style reference** (palette, typography, pacing, transitions to emulate). Say which in the brief.
- Map media to scenes by meaning, then variety. Scenes without media get original diagrams, kinetic typography, counters or charts.
- Follow `references/srt-and-reference-media-workflow.md` step by step.

## Language: read and write every language

The SRT can be in **any language or script** (Bengali, Arabic, Persian, Urdu, Hindi, Tamil, Thai, Chinese, Japanese, Korean, Russian, Hebrew, and more).
- **Reading:** `scripts/srt_to_storyboard.py` detects the file encoding (UTF-8, UTF-16, and legacy code pages such as Windows-1256, Windows-1251, Shift-JIS), strips bidirectional control marks, and detects the writing system and direction. If it prints an encoding WARNING, open the first cues and confirm the text looks right; if not, rerun with `--encoding <name>` or ask the user to re-save the SRT as UTF-8. Never continue with garbled text.
- **Writing:** every word that appears on screen (hooks, keywords, chapter labels, recap points, comparison labels, captions) must be in the SRT's language, never English by default. Fill the `label` column of the storyboard with a short chapter label in that language (leave it empty if unsure; empty means none is shown). Rewrite the draft `on_screen_text` into natural phrases in the same language. Keep the user's wording; do not translate.
- **Display:** the starter loads the right Noto font for the script, mirrors layout for right-to-left languages (`dir="rtl"`), splits words correctly for Thai, Chinese and Japanese, never letter-spaces or uppercases non-Latin text, and keeps the digits the narration uses (e.g. ২০ or ٢٠). `src/data/language.ts` holds the detected script and code; correct it if the guess is wrong (Persian vs Arabic, Traditional vs Simplified Chinese: use code `zh-TW`).
- **Talking to the user:** reply in the language the user writes to you in. File names, code and commands stay in English.
- **Fonts need internet on the first render** (Google Fonts via `@remotion/google-fonts`). Tell the user; the offline option is in `README-RENDER.md`.
- Mixed-language SRTs (e.g. Bengali with English terms) work: the primary script is used, Latin words fall back to Inter.
- Check at least one still frame per language: no missing glyph boxes, no mirrored or broken letter joins, captions in reading order.

## Motion quality bar (always apply)

Output must look like a modern premium explainer channel, not a slideshow:
- Every scene has depth layers (ambient background, subject/diagram, foreground text/captions) and at least one purposeful, narration-timed animation.
- Kinetic typography with masked, staggered reveals; animated SRT captions; draw-on diagrams; counters and animated charts; slow camera push or parallax; cross-scene transitions from a single consistent family.
- Hook, "aha" moment and recap get bespoke, hand-designed animation; the starter templates are a minimum, not the final design.
- Vary scene shape and pace; follow the energy arc and timing table in `references/motion-design-language.md`.
- Story first: hook → tension → insight → payoff → recap, with a visual callback from the recap to the hook.
- Motion must teach: animate cause, sequence, change, comparison or emphasis; never decoration alone.
- Every motion event carries a matching, varied sound effect (see Stage 7); no animation is silent unless silence is intended.

## Bundled tools (use them)

- `scripts/srt_to_storyboard.py input.srt storyboard.csv --captions src/data/captions.ts` — parse the SRT in any language/encoding, group cues into scenes with a draft `kind`, generate caption data and `src/data/language.ts`. Review and improve the draft (kinds, labels, on-screen text in the SRT's language).
- `scripts/generate_sfx.py` — regenerates the original sound-effect library (already included in the starter; rarely needed).
- `scripts/theme_tools.py check|preview|set|palette|suggest` — the 10-theme system: validate contrast, make a preview page, apply the chosen theme, extract palettes from reference images.
- `scripts/package_project.py <project_dir> --name <name>` — build the delivery ZIP with `README-RENDER.md`. Use this instead of rendering.
- `scripts/inventory_media.py <media_dir> --out media.json --copy-to public/media` — list reference images/videos with dimensions/duration (ffprobe if present). It cannot see pixels: you must open the files.

- `scripts/validate_storyboard.py storyboard.csv --fps 30` — validate scene timing (overlaps, gaps, missing narration, frame alignment). Run before coding.
- `scripts/storyboard_to_scenes.py storyboard.csv src/data/scenes.ts --fps 30` — generate typed scene data so composition length always matches the storyboard.
- `templates/remotion-starter/` — Remotion project with animated background, kinetic text, SRT captions, media frames, scene shell with transitions, and hook/concept/stat/steps/compare/recap/media scene templates. Copy it for new projects; for existing projects keep their Remotion version and conventions instead.
- `templates/storyboard.csv` — storyboard starting point.

Typical flow with SRT + media: read SRT → inventory and inspect media → **offer 10 themes and wait for the choice** → brief → `srt_to_storyboard.py` → refine storyboard (kinds, text, assets) → validate → copy starter → `storyboard_to_scenes.py` → build/upgrade scenes → typecheck → stills → fix → QA checklist → `package_project.py` → ZIP with render instructions (no video render).

## Reference library

Read the relevant guide as needed:
- `references/motion-design-language.md` (read before designing any scene)
- `references/sound-design-system.md` (read before writing any animation: which sound for which motion)
- `references/srt-and-reference-media-workflow.md` (read first when an SRT or media is supplied)
- `references/educational-storytelling.md`
- `references/research-and-fact-checking.md`
- `references/cinematic-visual-system.md`
- `references/remotion-production-engineering.md`
- `references/audio-and-voice.md`
- `references/series-production.md`
- `references/quality-assurance.md`
- `templates/production-brief-template.md`
- `templates/storyboard-template.md`
- `templates/script-template.md`
- `templates/asset-register-template.md`
