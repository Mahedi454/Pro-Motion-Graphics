#!/usr/bin/env python3
"""Build pro-motion-graphics.skill (a ZIP with a single top-level folder) and refresh MANIFEST.json.

Usage (from the skill folder): python scripts/package_skill.py
"""
import json
import os
import zipfile

NAME = "pro-motion-graphics"
OUT = NAME + ".skill"
SKIP_DIRS = {"node_modules", "out", "__pycache__", ".git"}


def main() -> None:
    files = []
    for d, dirs, fs in os.walk("."):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in fs:
            p = os.path.relpath(os.path.join(d, f), ".").replace("\\", "/")
            if p not in ("MANIFEST.json", ".gitignore") and not p.endswith(".skill") and not p.endswith(".pyc"):
                files.append(p)
    files.sort()
    manifest = {
        "skill": NAME,
        "version": "1.0.0",
        "engine": ["Remotion", "React", "TypeScript"],
        "default_profile": {"width": 1920, "height": 1080, "fps": 30, "aspect_ratio": "16:9"},
        "files": files,
    }
    with open("MANIFEST.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files + ["MANIFEST.json"]:
            z.write(p, f"{NAME}/{p}")
    with zipfile.ZipFile(OUT) as z:
        assert z.testzip() is None
        print(f"Built {OUT} with {len(z.namelist())} files")


if __name__ == "__main__":
    main()
