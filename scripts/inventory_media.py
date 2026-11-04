#!/usr/bin/env python3
"""Inventory reference images/videos so they can be analysed and assigned to scenes.

Usage:
    python inventory_media.py <media_dir> [--out media.json] [--copy-to public/media]

Lists every image/video/audio file with size and (when ffprobe is on PATH) dimensions,
duration and fps. With --copy-to, copies files into the Remotion public/ folder using
safe lowercase names. The script does NOT look at the pixels: Claude must open each
image (and sample video frames, e.g. `ffmpeg -i in.mp4 -vf fps=1/3 f_%03d.jpg`) to
describe subject, palette, composition and style before assigning it to a scene.
"""
import argparse
import json
import os
import re
import shutil
import subprocess

IMG = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif"}
VID = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}
AUD = {".mp3", ".wav", ".m4a", ".aac", ".ogg"}


def probe(path):
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=width,height,r_frame_rate:format=duration", "-of", "json", path],
            capture_output=True, text=True, timeout=30)
        d = json.loads(out.stdout or "{}")
        s = (d.get("streams") or [{}])[0]
        info = {"width": s.get("width"), "height": s.get("height"),
                "duration": float(d.get("format", {}).get("duration", 0) or 0)}
        r = s.get("r_frame_rate", "0/1").split("/")
        if len(r) == 2 and float(r[1]):
            info["fps"] = round(float(r[0]) / float(r[1]), 2)
        return info
    except (OSError, ValueError, subprocess.SubprocessError):
        return {}


def safe(name):
    return re.sub(r"[^a-z0-9._-]+", "-", name.lower()).strip("-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("media_dir")
    ap.add_argument("--out", default="media.json")
    ap.add_argument("--copy-to")
    a = ap.parse_args()

    items, used = [], set()
    for d, _, fs in os.walk(a.media_dir):
        for f in sorted(fs):
            ext = os.path.splitext(f)[1].lower()
            kind = "image" if ext in IMG else "video" if ext in VID else "audio" if ext in AUD else None
            if not kind:
                continue
            p = os.path.join(d, f)
            item = {"file": os.path.relpath(p, a.media_dir).replace("\\", "/"), "kind": kind,
                    "bytes": os.path.getsize(p)}
            if kind != "image" or ext not in {".svg"}:
                item.update(probe(p))
            if a.copy_to:
                os.makedirs(a.copy_to, exist_ok=True)
                dest = safe(f)
                base, ext2 = os.path.splitext(dest)
                n = 2
                while dest in used:  # avoid collisions between folders
                    dest = f"{base}-{n}{ext2}"
                    n += 1
                used.add(dest)
                shutil.copy2(p, os.path.join(a.copy_to, dest))
                item["public_name"] = dest
            item["notes"] = "TODO: describe subject, palette, mood, usable region, rights"
            items.append(item)

    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)
    print(f"{len(items)} media files -> {a.out}")


if __name__ == "__main__":
    main()
