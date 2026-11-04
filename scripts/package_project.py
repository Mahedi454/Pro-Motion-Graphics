#!/usr/bin/env python3
"""Zip a finished Remotion video project for manual rendering (no video is rendered).

Usage:
    python package_project.py <project_dir> [--name my-video] [--theme-name "Ocean Teal"]
                              [--out <dir>] [--no-media-copy]

Creates <out>/<name>.zip containing the project (without node_modules/out/.git) plus a
filled-in README-RENDER.md with unzip / npm install / render instructions.
Refuses to run if the project is missing the essentials. Prints the zip path and size.
"""
import argparse
import json
import os
import re
import sys
import zipfile

SKILL_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TEMPLATE = os.path.join(SKILL_ROOT, "templates", "README-RENDER-template.md")
SKIP_DIRS = {"node_modules", "out", ".git", "__pycache__", ".cache"}
SKIP_EXT = {".mp4", ".mov", ".webm"}  # rendered videos are never delivered; media goes in public/media only
REQUIRED = ["package.json", "src/index.ts", "src/Root.tsx", "src/Main.tsx",
            "src/data/scenes.ts", "src/data/captions.ts", "src/data/language.ts", "src/styles/fonts.ts", "src/styles/themes.json", "src/audio/sfx.generated.ts", "public/audio/sfx/whoosh-1.wav", "src/styles/theme.config.ts"]


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--name")
    ap.add_argument("--theme-name")
    ap.add_argument("--out")
    ap.add_argument("--no-media-copy", action="store_true", help="skip public/media (use if files are huge)")
    a = ap.parse_args()

    root = os.path.abspath(a.project_dir)
    missing = [r for r in REQUIRED if not os.path.exists(os.path.join(root, r))]
    if missing:
        sys.exit("Project is incomplete, missing: " + ", ".join(missing))

    name = re.sub(r"[^a-z0-9-]+", "-", (a.name or os.path.basename(root)).lower()).strip("-") or "motion-video"
    out_dir = os.path.abspath(a.out or os.path.join(root, ".."))
    os.makedirs(out_dir, exist_ok=True)
    zip_path = os.path.join(out_dir, name + ".zip")

    # facts for the instructions, read from the project itself (never invented)
    scenes = read(os.path.join(root, "src/data/scenes.ts"))
    fps = int((re.search(r"FPS\s*=\s*(\d+)", scenes) or [0, 30])[1])
    frames = int((re.search(r"TOTAL_FRAMES\s*=\s*(\d+)", scenes) or [0, 0])[1])
    secs = frames / fps if fps else 0
    duration = f"{int(secs // 60)}:{int(secs % 60):02d}"
    theme_id = (re.search(r"ACTIVE_THEME\s*=\s*'([^']+)'", read(os.path.join(root, "src/styles/theme.config.ts"))) or [0, "?"])[1]
    themes = json.loads(read(os.path.join(root, "src/styles/themes.json")))
    theme_name = a.theme_name or next((t["name"] for t in themes if t["id"] == theme_id), theme_id)

    guide = (read(TEMPLATE)
             .replace("{{PROJECT_NAME}}", name).replace("{{THEME_NAME}}", theme_name)
             .replace("{{DURATION}}", duration).replace("{{FRAMES}}", str(frames))
             .replace("{{ZIP_NAME}}", name + ".zip"))

    if os.path.exists(zip_path):
        os.remove(zip_path)
    count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for d, dirs, files in os.walk(root):
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
            rel_d = os.path.relpath(d, root).replace("\\", "/")
            if a.no_media_copy and rel_d.startswith("public/media"):
                continue
            for f in files:
                p = os.path.join(d, f)
                rel = os.path.relpath(p, root).replace("\\", "/")
                if os.path.abspath(p) == zip_path or rel == "README-RENDER.md":
                    continue
                if os.path.splitext(f)[1].lower() in SKIP_EXT and not rel.startswith("public/"):
                    continue
                z.write(p, f"{name}/{rel}")
                count += 1
        z.writestr(f"{name}/README-RENDER.md", guide)
        count += 1
    with zipfile.ZipFile(zip_path) as z:
        assert z.testzip() is None
    print(f"Created {zip_path}\n  {count} files, {os.path.getsize(zip_path) / 1024 / 1024:.2f} MB, "
          f"{duration} ({frames} frames @ {fps} fps), theme: {theme_name}")


if __name__ == "__main__":
    main()
