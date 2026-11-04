#!/usr/bin/env python3
"""Colour-theme tools for the Pro Motion Graphics starter.

Commands:
  python theme_tools.py check   [themes.json]             contrast report for every theme
  python theme_tools.py preview [themes.json] [out.html]  theme preview page (open in a browser)
  python theme_tools.py set <theme-id> [project_dir]      make the project use that theme
  python theme_tools.py palette <image> [<image> ...]     dominant colours of reference images
  python theme_tools.py suggest <image> [<image> ...]     theme JSON entries derived from images

Every theme has exactly four colours: bg, text, accent, hero.
Rules checked: text vs bg >= 7:1, accent vs bg >= 3:1, hero vs bg >= 3:1, accent != hero.
"""
import colorsys
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_THEMES = os.path.join(HERE, "..", "templates", "remotion-starter", "src", "styles", "themes.json")
KEYS = ("bg", "text", "accent", "hero")


def rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexc(c):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(v))) for v in c)


def lum(c):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(v) for v in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la = lum(rgb(a) if isinstance(a, str) else a)
    lb = lum(rgb(b) if isinstance(b, str) else b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def load(path=None):
    with open(path or DEFAULT_THEMES, encoding="utf-8") as f:
        return json.load(f)


def problems(t):
    out = []
    for k in KEYS:
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", str(t.get(k, ""))):
            out.append(f"{k} must be a #RRGGBB colour")
    if out:
        return out
    if ratio(t["text"], t["bg"]) < 7:
        out.append(f"text/bg contrast {ratio(t['text'], t['bg']):.1f} < 7")
    if ratio(t["accent"], t["bg"]) < 3:
        out.append(f"accent/bg contrast {ratio(t['accent'], t['bg']):.1f} < 3")
    if ratio(t["hero"], t["bg"]) < 3:
        out.append(f"hero/bg contrast {ratio(t['hero'], t['bg']):.1f} < 3")
    if t["accent"].lower() == t["hero"].lower():
        out.append("accent and hero must differ")
    return out


def cmd_check(path=None):
    themes = load(path)
    bad = 0
    for t in themes:
        p = problems(t)
        bad += bool(p)
        detail = "; ".join(p) if p else (
            f"text {ratio(t['text'], t['bg']):.1f}  accent {ratio(t['accent'], t['bg']):.1f}  "
            f"hero {ratio(t['hero'], t['bg']):.1f}")
        print(("FAIL " if p else "ok   ") + f"{t['id']:<15} " + detail)
    print(f"{len(themes)} themes, {bad} failing")
    return 1 if bad else 0


def cmd_preview(path=None, out="themes-preview.html"):
    themes = load(path)
    cards = []
    for i, t in enumerate(themes, 1):
        sw = "".join(
            f'<span class="sw" style="background:{t[k]}"><b>{k}</b>{t[k]}</span>' for k in KEYS)
        cards.append(
            f'<div class="card" style="background:{t["bg"]};color:{t["text"]}">'
            f'<div class="n" style="color:{t["accent"]}">THEME {i} &middot; {t["id"]}</div>'
            f'<h2>Why does <span style="color:{t["hero"]}">gravity</span> bend light?</h2>'
            f'<p class="m">{t["name"]} - {t.get("mood", "")}</p>'
            f'<div class="bar"><i style="background:{t["accent"]}"></i><i style="background:{t["hero"]}"></i></div>'
            f'<div class="sws">{sw}</div></div>')
    css = (
        "body{font-family:system-ui,sans-serif;margin:0;padding:24px;background:#888;display:grid;"
        "grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:18px}"
        ".card{border-radius:18px;padding:22px;box-shadow:0 8px 30px rgba(0,0,0,.35)}"
        "h2{margin:.4em 0;font-size:26px}.n{font-size:12px;letter-spacing:.15em;font-weight:700}"
        ".m{opacity:.75;margin:0 0 14px}.bar{display:flex;gap:6px;margin-bottom:14px}"
        ".bar i{height:6px;flex:1;border-radius:3px}"
        ".sws{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}"
        ".sw{font:11px monospace;padding:10px 6px;border-radius:8px;color:#fff;"
        "text-shadow:0 0 3px #000;display:flex;flex-direction:column}.sw b{font-size:12px}"
    )
    html = ('<!doctype html><meta charset="utf-8"><title>Video colour themes</title>'
            f'<style>{css}</style>' + "".join(cards))
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print("Wrote", out)
    return 0


def cmd_set(theme_id, project="."):
    ids = [t["id"] for t in load(os.path.join(project, "src", "styles", "themes.json"))]
    if theme_id not in ids:
        print("Unknown theme. Choose one of:", ", ".join(ids))
        return 1
    p = os.path.join(project, "src", "styles", "theme.config.ts")
    with open(p, "w", encoding="utf-8") as f:
        f.write("// The ONLY line to change to switch the whole video's look.\n"
                "// Use an `id` from src/styles/themes.json (or run: python scripts/theme_tools.py set <id>).\n"
                f"export const ACTIVE_THEME = '{theme_id}';\n")
    print("Theme set to", theme_id)
    return 0


def dominant(path, n=8):
    try:
        from PIL import Image
    except ImportError:
        sys.exit("Pillow is needed for image colours: pip install pillow  (or read the colours by eye)")
    im = Image.open(path).convert("RGB")
    im.thumbnail((160, 160))
    q = im.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[: n * 3]
    found = sorted(q.getcolors(), reverse=True)  # (count, index)
    return [(cnt, tuple(pal[i * 3:i * 3 + 3])) for cnt, i in found]


def cmd_palette(paths):
    for p in paths:
        print(os.path.basename(p))
        cols = dominant(p)
        total = sum(c for c, _ in cols)
        for cnt, c in cols:
            print(f"  {hexc(c)}  {cnt / total * 100:4.1f}%")
    return 0


def hls(c):
    return colorsys.rgb_to_hls(*(v / 255 for v in c))


def vividness(c):
    h, l, s = hls(c)
    return s * (1 - abs(2 * l - 1))


def fit(c, bg, minr):
    """Nudge colour c in lightness until it reaches minr contrast against bg."""
    h, l, s = hls(c)
    dark_bg = lum(rgb(bg)) < 0.4
    for _ in range(40):
        col = tuple(v * 255 for v in colorsys.hls_to_rgb(h, l, s))
        if ratio(col, bg) >= minr:
            return hexc(col)
        l = min(1, l + 0.03) if dark_bg else max(0, l - 0.03)
    return "#FFFFFF" if dark_bg else "#000000"


def cmd_suggest(paths):
    cols = []
    for p in paths:
        cols += [c for _, c in dominant(p, 10)]
    if not cols:
        sys.exit("no colours found")
    by_l = sorted(cols, key=lum)
    vivid = sorted(cols, key=vividness, reverse=True)
    out = []
    for dark in (True, False):
        base = by_l[0] if dark else by_l[-1]
        bg = hexc(tuple(v * 0.35 for v in base)) if dark else hexc(tuple(255 - (255 - v) * 0.25 for v in base))
        accent = vivid[0]
        hero = next((c for c in vivid[1:] if abs(hls(c)[0] - hls(accent)[0]) > 0.08), vivid[-1])
        t = {"id": "image-dark" if dark else "image-light",
             "name": "From your images (" + ("dark" if dark else "light") + ")",
             "mood": "Derived from the reference images",
             "bg": bg, "text": "#F4F7FB" if dark else "#14213D",
             "accent": fit(accent, bg, 3), "hero": fit(hero, bg, 3)}
        if t["accent"].lower() == t["hero"].lower():  # last resort: rotate the hue
            h, l, s = hls(accent)
            t["hero"] = fit(tuple(v * 255 for v in colorsys.hls_to_rgb((h + 0.5) % 1, l, max(s, 0.5))), bg, 3)
        out.append(t)
    for t in out:
        for p in problems(t):
            print(f"warning: {t['id']}: {p} - adjust by hand before offering it", file=sys.stderr)
    print(json.dumps(out, indent=2))
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    c, a = argv[1], argv[2:]
    if c == "check":
        return cmd_check(*a[:1])
    if c == "preview":
        return cmd_preview(*a[:2])
    if c == "set" and a:
        return cmd_set(*a[:2])
    if c == "palette" and a:
        return cmd_palette(a)
    if c == "suggest" and a:
        return cmd_suggest(a)
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
