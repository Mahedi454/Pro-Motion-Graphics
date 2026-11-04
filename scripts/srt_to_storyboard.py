#!/usr/bin/env python3
"""Turn an SRT file (any language) into a draft storyboard CSV, captions and language data.

Usage:
    python srt_to_storyboard.py input.srt storyboard.csv [--captions src/data/captions.ts]
                                [--language-out src/data/language.ts] [--encoding utf-8]
                                [--fps 30] [--min 4] [--max 12] [--gap 0.9]

* Reads any encoding (UTF-8/16 with or without BOM, and legacy code pages with a warning).
* Detects the writing system (Bengali, Arabic, Devanagari, CJK, Thai, Cyrillic, ...) and
  whether it is right-to-left, and writes src/data/language.ts so the video loads the
  correct font and layout direction.
* The SRT is the timing authority. Cues are grouped into scenes at sentence ends (including
  . ! ? and their Arabic, Indic and CJK forms) or long pauses.
* Scene `kind` guesses use language-neutral signals (numbers, question marks) plus English
  keywords; for other languages Claude must review and refine `kind`, `label` and
  `on_screen_text`. ALL on-screen text must be written in the SRT's language.
"""
import argparse
import codecs
import csv
import json
import os
import re
import sys
import unicodedata

TS = re.compile(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)")
SENT_END = r"[.!?。！？｡।॥؟۔։።។៕‼…]"

# (script id, ranges). First match by codepoint.
SCRIPTS = [
    ("bengali", [(0x0980, 0x09FF)]), ("devanagari", [(0x0900, 0x097F)]), ("gurmukhi", [(0x0A00, 0x0A7F)]),
    ("gujarati", [(0x0A80, 0x0AFF)]), ("oriya", [(0x0B00, 0x0B7F)]), ("tamil", [(0x0B80, 0x0BFF)]),
    ("telugu", [(0x0C00, 0x0C7F)]), ("kannada", [(0x0C80, 0x0CFF)]), ("malayalam", [(0x0D00, 0x0D7F)]),
    ("sinhala", [(0x0D80, 0x0DFF)]), ("thai", [(0x0E00, 0x0E7F)]), ("lao", [(0x0E80, 0x0EFF)]),
    ("myanmar", [(0x1000, 0x109F)]), ("khmer", [(0x1780, 0x17FF)]), ("georgian", [(0x10A0, 0x10FF)]),
    ("armenian", [(0x0530, 0x058F)]), ("ethiopic", [(0x1200, 0x137F)]), ("hebrew", [(0x0590, 0x05FF)]),
    ("arabic", [(0x0600, 0x06FF), (0x0750, 0x077F), (0x08A0, 0x08FF), (0xFB50, 0xFDFF), (0xFE70, 0xFEFF)]),
    ("kana", [(0x3040, 0x30FF)]), ("hangul", [(0xAC00, 0xD7AF), (0x1100, 0x11FF), (0x3130, 0x318F)]),
    ("han", [(0x4E00, 0x9FFF), (0x3400, 0x4DBF)]),
    ("cyrillic", [(0x0400, 0x04FF)]), ("greek", [(0x0370, 0x03FF)]),
]
RTL = {"arabic", "hebrew"}
NO_SPACES = {"thai", "lao", "myanmar", "khmer", "kana", "han"}  # words are not separated by spaces


def to_s(h, m, s, ms):
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms.ljust(3, "0")[:3]) / 1000


# ---------------------------------------------------------------- encoding

def read_text(path, forced=None):
    """Return (text, encoding_used, warning_or_None)."""
    raw = open(path, "rb").read()
    if forced:
        return raw.decode(forced), forced, None
    if raw.startswith(codecs.BOM_UTF8):
        return raw.decode("utf-8-sig"), "utf-8-sig", None
    if raw.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        return raw.decode("utf-16"), "utf-16", None
    try:
        return raw.decode("utf-8"), "utf-8", None
    except UnicodeDecodeError:
        pass
    if raw and raw.count(b"\x00") > len(raw) * 0.25:  # UTF-16 without BOM
        for enc in ("utf-16-le", "utf-16-be"):
            try:
                return raw.decode(enc), enc, None
            except UnicodeDecodeError:
                pass
    try:  # best detector, if installed
        from charset_normalizer import from_bytes
        best = from_bytes(raw).best()
        if best is not None:
            return str(best), best.encoding, f"encoding detected as {best.encoding}; verify the text looks right"
    except ImportError:
        pass
    # legacy code pages: pick the one that yields the most letters
    best_enc, best_score, best_txt = None, -1, None
    for enc in ("cp1256", "cp1251", "cp1253", "cp1255", "cp874", "cp1254", "cp1250", "cp1258",
                "gb18030", "big5", "shift_jis", "euc-kr", "cp1252"):
        try:
            txt = raw.decode(enc)
        except UnicodeDecodeError:
            continue
        non_ascii = [c for c in txt if ord(c) > 127]
        score = sum(c.isalpha() for c in non_ascii) / (len(non_ascii) or 1)
        if score > best_score:
            best_enc, best_score, best_txt = enc, score, txt
    if best_txt is None:
        return raw.decode("utf-8", errors="replace"), "utf-8", "could not decode cleanly; text may be corrupted"
    return best_txt, best_enc, (f"file is not UTF-8; guessed {best_enc}. CHECK the text. If it looks wrong, re-save the "
                                "SRT as UTF-8 or rerun with --encoding <name> (e.g. cp1256, cp1251, shift_jis)")


# ---------------------------------------------------------------- language

def script_of(ch):
    cp = ord(ch)
    for name, ranges in SCRIPTS:
        for lo, hi in ranges:
            if lo <= cp <= hi:
                return name
    return None


def detect_language(text):
    counts = {}
    letters = 0
    for ch in text:
        if not ch.isalpha():
            continue
        letters += 1
        s = script_of(ch) or ("latin" if ord(ch) < 0x250 else "other")
        counts[s] = counts.get(s, 0) + 1
    if not letters:
        return {"script": "latin", "code": "en", "rtl": False, "noSpaces": False}
    # Japanese uses kana + han together; Korean hangul (+ some han)
    if counts.get("kana"):
        counts["kana"] += counts.pop("han", 0)
    top = max(counts, key=counts.get)
    # prefer a non-Latin script if it is a meaningful share (mixed English words are common)
    non_latin = {k: v for k, v in counts.items() if k not in ("latin", "other")}
    if non_latin and sum(non_latin.values()) >= 0.2 * letters:
        top = max(non_latin, key=non_latin.get)
    code = {"bengali": "bn", "devanagari": "hi", "gurmukhi": "pa", "gujarati": "gu", "oriya": "or", "tamil": "ta",
            "telugu": "te", "kannada": "kn", "malayalam": "ml", "sinhala": "si", "thai": "th", "lao": "lo",
            "myanmar": "my", "khmer": "km", "georgian": "ka", "armenian": "hy", "ethiopic": "am", "hebrew": "he",
            "arabic": "ar", "kana": "ja", "hangul": "ko", "han": "zh", "cyrillic": "ru", "greek": "el",
            "latin": "en"}.get(top, "en")
    if top == "arabic":
        if re.search(r"[پچژگ]", text):
            code = "fa"
        if re.search(r"[ٹڈڑںے]", text):
            code = "ur"
    if top == "han":
        top = "han"
    return {"script": top, "code": code, "rtl": top in RTL, "noSpaces": top in NO_SPACES}


def write_language(path, info):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("// Generated by srt_to_storyboard.py from the SRT. Drives font, direction and word splitting.\n"
                "// If the guess is wrong (e.g. Persian vs Arabic, Traditional vs Simplified Chinese), edit it here.\n"
                "export type Lang = {script: string; code: string; rtl: boolean; noSpaces: boolean};\n"
                f"export const LANG: Lang = {json.dumps(info, ensure_ascii=False)};\n")


# ---------------------------------------------------------------- SRT

def parse_srt(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("﻿")
    cues = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [l for l in block.split("\n") if l.strip()]
        for i, l in enumerate(lines):
            m = TS.search(l)
            if m:
                g = m.groups()
                body = " ".join(x.strip() for x in lines[i + 1:])
                body = re.sub(r"<[^>]+>|\{[^}]+\}", "", body)
                body = re.sub(r"[‎‏‪-‮⁦-⁩]", "", body)  # bidi control marks
                body = re.sub(r"\s+", " ", body).strip()
                if body:
                    cues.append({"start": to_s(*g[:4]), "end": to_s(*g[4:]), "text": body})
                break
    cues.sort(key=lambda c: c["start"])
    return cues


def guess_kind(text, index, total):
    t = text.lower()
    if index == 0:
        return "hook"
    if index == total - 1 or re.search(r"\b(in summary|to recap|remember|takeaway|in short)\b", t):
        return "recap"
    if re.search(r"\d[\d,]*\.?\d*", t) and not re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b", t):
        return "stat"  # contains a number (any digit set); years like 1969 / 2024 excluded
    if re.search(r"\b(first|second|third|step|then|next|finally|stage)\b", t):
        return "steps"
    if re.search(r"\b(vs\.?|versus|compared|difference|whereas|unlike)\b", t):
        return "compare"
    if re.search(r"[?？؟;]", text):
        return "question"
    if re.search(r"\b(is called|is defined|refers to|means|known as)\b", t):
        return "definition"
    if re.search(r"[\"“「«]", text):
        return "quote"
    return "concept"


STOP = set("the a an and or of to in on for with is are was were be it this that as at by from your you we they "
           "their can will not but so if then than into more most very".split())


def _strip_punct(tok):
    """Trim punctuation/symbols from both ends only (keeps combining vowel signs inside words)."""
    s, e = 0, len(tok)
    while s < e and unicodedata.category(tok[s])[0] in "PS":
        s += 1
    while e > s and unicodedata.category(tok[e - 1])[0] in "PS" and tok[e - 1] != "%":
        e -= 1
    return tok[s:e]


def keywords(text, n=4, no_spaces=False):
    if no_spaces:
        return re.sub(r"\s+", "", text)[:14]
    seen, out = set(), []
    for raw in text.split():
        w = _strip_punct(raw)
        lw = w.lower()
        if len(w) < 2 or lw in STOP or lw in seen:
            continue
        seen.add(lw)
        out.append(w)
    return " ".join(out[:n])


def group(cues, lo, hi, gap):
    scenes, cur = [], []
    for c in cues:
        if cur and (c["start"] - cur[-1]["end"]) >= gap and (cur[-1]["end"] - cur[0]["start"]) >= lo:
            scenes.append(cur)
            cur = []
        cur.append(c)
        dur = c["end"] - cur[0]["start"]
        ends_sentence = bool(re.search(SENT_END + r"['\")\]”」»]*$", c["text"]))
        if (dur >= lo and ends_sentence) or dur >= hi:
            scenes.append(cur)
            cur = []
    if cur:
        if scenes and (cur[-1]["end"] - cur[0]["start"]) < lo / 2:
            scenes[-1].extend(cur)
        else:
            scenes.append(cur)
    return scenes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("srt")
    ap.add_argument("out_csv")
    ap.add_argument("--captions")
    ap.add_argument("--language-out")
    ap.add_argument("--encoding")
    ap.add_argument("--lang", help="force language code, e.g. bn, ar, fa, ur, ja, zh")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--min", type=float, default=4.0)
    ap.add_argument("--max", type=float, default=12.0)
    ap.add_argument("--gap", type=float, default=0.9)
    a = ap.parse_args()

    try:
        text, enc, warn = read_text(a.srt, a.encoding)
    except (OSError, LookupError, UnicodeDecodeError) as e:
        sys.exit(f"Cannot read SRT: {e}")
    if warn:
        print("WARNING:", warn, file=sys.stderr)
    cues = parse_srt(text)
    if not cues:
        sys.exit("No cues found in SRT.")
    info = detect_language(" ".join(c["text"] for c in cues))
    if a.lang:
        info["code"] = a.lang
    scenes = group(cues, a.min, a.max, a.gap)

    rows = []
    for i, sc in enumerate(scenes):
        start = 0.0 if i == 0 else sc[0]["start"]
        end = scenes[i + 1][0]["start"] if i + 1 < len(scenes) else sc[-1]["end"] + 0.5
        end = max(end, start + 1.0 / a.fps)
        narr = (" " if not info["noSpaces"] else "").join(c["text"] for c in sc)
        kind = guess_kind(narr, i, len(scenes))
        rows.append({
            "scene": f"S{i + 1:02d}",
            "start_seconds": f"{round(start * a.fps) / a.fps:.3f}",
            "end_seconds": f"{round(end * a.fps) / a.fps:.3f}",
            "kind": kind,
            "label": "",  # on-screen chapter label: WRITE IT IN THE VIDEO'S LANGUAGE (empty = none shown)
            "learning_purpose": {"hook": "Hook", "recap": "Recap", "stat": "Make the number concrete",
                                 "steps": "Show the sequence", "compare": "Contrast two ideas",
                                 "question": "Pose and resolve a question", "definition": "Define the term",
                                 "quote": "Anchor with a quotation"}.get(kind, "Explain the concept"),
            "visual": f"[{kind}] DRAFT - refine: visual metaphor/diagram for this idea",
            "narration": narr,
            "on_screen_text": keywords(narr, no_spaces=info["noSpaces"]),
            "motion": "kinetic keywords, parallax background, eased reveal",
            "audio": "",
            "assets": "",
        })

    cols = ["scene", "start_seconds", "end_seconds", "kind", "label", "learning_purpose", "visual",
            "narration", "on_screen_text", "motion", "audio", "assets"]
    with open(a.out_csv, "w", newline="", encoding="utf-8-sig") as f:  # BOM so Excel shows non-Latin text
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    if a.captions:
        data = [{"startFrame": round(c["start"] * a.fps),
                 "endFrame": max(round(c["end"] * a.fps), round(c["start"] * a.fps) + 1),
                 "text": c["text"]} for c in cues]
        with open(a.captions, "w", encoding="utf-8") as f:
            f.write("// Generated by srt_to_storyboard.py from the SRT. Timing authority: the SRT.\n"
                    "export type Cue = {startFrame: number; endFrame: number; text: string};\n"
                    f"export const CAPTIONS_FPS = {a.fps};\n"
                    f"export const cues: Cue[] = {json.dumps(data, indent=2, ensure_ascii=False)};\n")
    lang_out = a.language_out or (os.path.join(os.path.dirname(os.path.abspath(a.captions)), "language.ts")
                                  if a.captions else None)
    if lang_out:
        write_language(lang_out, info)

    print(f"{len(cues)} cues -> {len(rows)} scenes, {rows[-1]['end_seconds']}s total -> {a.out_csv}")
    print(f"language: script={info['script']} code={info['code']} rtl={info['rtl']} noSpaces={info['noSpaces']} "
          f"(encoding {enc})" + (f" -> {lang_out}" if lang_out else ""))


if __name__ == "__main__":
    main()
