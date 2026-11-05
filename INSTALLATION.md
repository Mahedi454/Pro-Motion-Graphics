# Install Pro Motion Graphics Skill 1.0

1. Upload `pro-motion-graphics.skill` in Claude: Settings > Customize > Skills > create/upload skill (wording may vary).
2. Enable the skill.
3. Test with a small topic, e.g. "Make a 60-second explainer on how vaccines train the immune system."

The `.skill` file is a ZIP archive whose single top-level folder is `pro-motion-graphics/` containing `SKILL.md`.

## Use it only inside a Project

Skills in Claude are enabled for the whole account, and the file cannot lock itself to one place. The skill is written to run only in Projects and to decline in plain chat, but this depends on Claude following its instructions. To set it up:
1. Create a Claude Project for your videos and add the SRT, images and videos to the project files.
2. In the Project's instructions, write: "Use the pro-motion-graphics skill for video work in this project."
3. For a hard guarantee, turn the skill off in Settings > Skills when you are not working on videos.

Bundled: the Remotion starter with 10 colour themes and 49 original sound effects (royalty-free, synthesized).

Not bundled: Node.js, Remotion packages (the starter pins versions; the user runs `npm install`), fonts (loaded from Google Fonts on the first render, so that needs internet), and the user's own media. Python 3 is needed for the helper scripts; Pillow is optional (image colours).
