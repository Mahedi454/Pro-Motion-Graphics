#!/usr/bin/env python3
"""Storyboard CSV validator.

Usage:
    python validate_storyboard.py storyboard.csv [--fps 30] [--strict]

Errors (exit 1): missing columns, bad numbers, invalid/overlapping intervals,
missing learning_purpose or visual, duplicate scene IDs.
Warnings: gaps between scenes, first scene not starting at 0, empty narration,
very short (<1.5s) or very long (>25s) scenes, times not on a frame boundary.
--strict turns warnings into errors.
"""
import argparse
import csv
import sys

REQUIRED = {"scene", "start_seconds", "end_seconds", "learning_purpose", "visual"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("csv_path")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    errors, warnings = [], []
    try:
        with open(args.csv_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            fields = {(h or "").strip() for h in (reader.fieldnames or [])}
            missing = REQUIRED - fields
            if missing:
                print("ERROR: missing columns: " + ", ".join(sorted(missing)))
                return 1
            rows = [{(k or "").strip(): (v or "").strip() for k, v in r.items()} for r in reader]
    except OSError as e:
        print(f"ERROR: cannot read file: {e}")
        return 1

    if not rows:
        print("ERROR: no storyboard rows found.")
        return 1

    prev_end, seen = 0.0, set()
    for i, row in enumerate(rows, 1):
        sid = row["scene"]
        if sid in seen:
            errors.append(f"Row {i}: duplicate scene ID '{sid}'.")
        seen.add(sid)
        try:
            start, end = float(row["start_seconds"]), float(row["end_seconds"])
        except ValueError:
            errors.append(f"Row {i}: start_seconds/end_seconds must be numbers.")
            continue
        if start < 0 or end <= start:
            errors.append(f"Row {i}: invalid interval {start}-{end}.")
            continue
        if start < prev_end - 1e-9:
            errors.append(f"Row {i}: overlaps the previous scene (starts {start}, previous ended {prev_end}).")
        elif start > prev_end + 1e-9:
            warnings.append(f"Row {i}: gap of {start - prev_end:.2f}s before this scene.")
        if not row["learning_purpose"] or not row["visual"]:
            errors.append(f"Row {i}: learning_purpose and visual are required.")
        if not row.get("narration"):
            warnings.append(f"Row {i}: narration is empty.")
        dur = end - start
        if dur < 1.5:
            warnings.append(f"Row {i}: very short scene ({dur:.2f}s).")
        if dur > 25:
            warnings.append(f"Row {i}: very long scene ({dur:.2f}s); consider splitting.")
        for label, t in (("start", start), ("end", end)):
            if abs(t * args.fps - round(t * args.fps)) > 1e-6:
                warnings.append(f"Row {i}: {label} {t}s is not on a frame boundary at {args.fps} fps.")
        prev_end = max(prev_end, end)

    try:
        if float(rows[0]["start_seconds"]) != 0:
            warnings.append("First scene does not start at 0s.")
    except ValueError:
        pass  # already reported as an error above

    for w in warnings:
        print("WARNING:", w)
    for e in errors:
        print("ERROR:", e)
    if errors or (args.strict and warnings):
        return 1
    print(f"Valid storyboard: {len(rows)} scenes, {prev_end:.2f}s total ({round(prev_end * args.fps)} frames @ {args.fps} fps).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
