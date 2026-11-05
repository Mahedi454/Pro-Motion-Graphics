# How to render your video (manual steps)

Claude has built the video project for you but has **not** rendered the video. The ZIP contains the complete Remotion project. You render it on your own computer, which takes a few minutes.

**Project:** {{PROJECT_NAME}}  |  **Theme:** {{THEME_NAME}}  |  **Size:** 1920x1080 @ 30 fps  |  **Length:** {{DURATION}} ({{FRAMES}} frames)

## 1. Install Node.js (one time)
Download the **LTS** version from https://nodejs.org (version 18 or newer). Check it worked:
```
node -v
npm -v
```

## 2. Unzip the project
- **Windows:** right-click the ZIP -> **Extract All...** (not "open"; extract it to a normal folder such as `Documents`).
- **macOS:** double-click the ZIP.
- **Linux / terminal:** `unzip {{ZIP_NAME}}` (it creates the `{{PROJECT_NAME}}` folder for you)

Open a terminal inside the extracted project folder (the one that contains `package.json`):
- **Windows:** open the folder, click the address bar, type `cmd`, press Enter.
- **macOS:** right-click the folder -> *New Terminal at Folder*.
- **Linux:** `cd {{PROJECT_NAME}}`

## 3. Install the dependencies (one time, about 1-3 minutes)
```
npm install
```

## 4. Add your files (if they are not already inside)
- Reference images/videos -> `public/media/`
- Narration audio -> `public/audio/narration/main.mp3`, then open `src/Main.tsx` and set
  `const NARRATION = 'audio/narration/main.mp3';`

### Fonts and languages
The video loads its font from Google Fonts the first time you preview or render, so **be online for the first render** (it is cached afterwards). To work fully offline, put a font file such as `NotoSansBengali.ttf` in `public/fonts/`, then add this to `src/styles/fonts.ts` (replace the `fontStack` line at the bottom): `export const fontStack = '"MyFont", system-ui, sans-serif';` and register it once with `new FontFace('MyFont', 'url(' + staticFile('fonts/NotoSansBengali.ttf') + ')').load().then((f) => document.fonts.add(f));`.
Right-to-left languages (Arabic, Persian, Urdu, Hebrew) are mirrored automatically. The language is stored in `src/data/language.ts`.

## 5. Preview (optional but recommended)
```
npm run preview
```
A browser window opens. Press Space to play, drag the timeline to check scenes and captions. Close it with Ctrl+C in the terminal.

## 6. Render the video
```
npm run render
```
Your video is saved at **`out/video.mp4`**.

Shortcut: on Windows double-click `render.bat`; on macOS/Linux run `bash render.sh`. Both install and render in one step.

### Useful variations
| Goal | Command |
|---|---|
| Faster draft (half size) | `npx remotion render src/index.ts Main out/draft.mp4 --scale=0.5` |
| Smaller file | `npx remotion render src/index.ts Main out/video.mp4 --crf=26` |
| One frame as an image | `npx remotion still src/index.ts Main out/frame.png --frame=60` |
| Render only a range | `npx remotion render src/index.ts Main out/part.mp4 --frames=0-299` |

## Sound effects
The video includes original sound effects that match the animations (whooshes for transitions, pops for elements, ticks for steps, chimes for checkmarks, and more). They are generated from scratch and royalty-free, and they are rendered into the MP4 automatically.
- Turn all effects off: open `src/audio/config.ts` and set `SFX_ENABLED = false`.
- Make them quieter or louder: change `SFX_VOLUME` (0 to 1).
- Add your narration as described in step 4. Effects stay under the voice.

## Change the colours
Open `src/styles/theme.config.ts` and change the id, for example `'ocean-teal'`. Available themes (each has `bg`, `text`, `accent`, `hero` colours) are listed in `src/styles/themes.json`; you can also edit those four colours directly.

## Troubleshooting
- **`node` / `npm` not recognised:** reinstall Node.js, then open a **new** terminal.
- **`npm install` fails:** check your internet connection; delete the `node_modules` folder and run it again.
- **Browser download error on first render:** Remotion downloads a small Chrome the first time. Allow it through your firewall and retry.
- **Out of memory / very slow:** close other apps and use `--concurrency=2`, or render a draft with `--scale=0.5`.
- **Missing file error:** the file named in the message must exist under `public/` with exactly that name.
- **Captions early/late:** set `CAPTION_OFFSET_FRAMES` in `src/components/Captions.tsx`.
- **Still stuck:** copy the full error text and ask Claude in the same Project.

## What is in the ZIP
| Path | Purpose |
|---|---|
| `src/` | Video source code (scenes, theme, captions) |
| `src/data/scenes.ts`, `src/data/captions.ts` | Scene timing and captions from your SRT |
| `public/` | Your images, videos, audio |
| `production/` | Brief, script, storyboard, asset and rights notes |
| `README-RENDER.md` | This guide |
