# Remotion starter (Pro Motion Graphics)

SRT-driven starter with modern motion: ambient animated background, kinetic typography, SRT captions,
reference-media cards (Ken Burns), cross-scene transitions, and templates for hook / concept / stat / steps / compare / recap / media scenes.

1. Copy this folder to the project location and run `npm install`.
2. Put reference images/videos in `public/media/` (use `scripts/inventory_media.py --copy-to public/media`).
3. From the SRT: `python <skill>/scripts/srt_to_storyboard.py input.srt storyboard.csv --captions src/data/captions.ts`
4. Refine `storyboard.csv` (kind, on_screen_text, `assets` as `file1|file2`), then
   `python <skill>/scripts/validate_storyboard.py storyboard.csv` and
   `python <skill>/scripts/storyboard_to_scenes.py storyboard.csv src/data/scenes.ts`.
5. `python <skill>/scripts/theme_tools.py set <theme-id> .` to apply the chosen colour theme.
6. `npm run typecheck`, then deliver with `python <skill>/scripts/package_project.py . --name <video-name>` (the user runs `npm run render` -> `out/video.mp4` on their own computer; Claude does not render the video).

Customise: colours/fonts in `src/styles/tokens.ts`; add bespoke scenes and register them by id in `custom` in `src/Main.tsx`.
Pinned versions are a baseline; if the user's project already has Remotion, keep its version and adapt.
Narration audio: set `NARRATION` in `Main.tsx`.
