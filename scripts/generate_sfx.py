#!/usr/bin/env python3
"""Synthesize the original sound-effect library for the Pro Motion Graphics starter.

Usage:
    python generate_sfx.py [--out public/audio/sfx] [--manifest src/audio/sfx.generated.ts]

Pure Python (standard library only). Every sound is generated from maths, so the whole
library is original and royalty-free: no copyrighted audio. Each sound type has several
different variants (different pitch, sweep, timbre), so repeated animations never sound identical.

Sound types and what they are for:
  whoosh   scene transition (long sweep)        swipe    panel / image sliding in (short sweep)
  pop      element appears (bubble pop)         tick     list item / step highlight
  click    typed / kinetic text word            hit      heavy impact: hero reveal, landing
  riser    tension build before a reveal        chime    success, checkmark (ascending pentatonic)
  sparkle  image / media reveal shimmer         draw     line or diagram drawing on
  counter  number counting tick                 swell    soft pad for diagrams / emphasis
"""
import argparse
import json
import math
import os
import random
import struct
import wave

SR = 44100
TAU = 2 * math.pi


class LP:
    """One-pole low-pass."""
    def __init__(self, fc):
        self.a = 1 - math.exp(-TAU * fc / SR)
        self.y = 0.0

    def __call__(self, x):
        self.y += self.a * (x - self.y)
        return self.y


class BP:
    """State-variable band-pass whose centre frequency can change every sample."""
    def __init__(self, q=1.5):
        self.low = self.band = 0.0
        self.q = 1.0 / q

    def __call__(self, x, fc):
        f = 2 * math.sin(math.pi * min(fc, SR * 0.45) / SR)
        self.low += f * self.band
        high = x - self.low - self.q * self.band
        self.band += f * high
        return self.band


def n_samples(dur):
    return int(dur * SR)


def whoosh(v, long=True):
    rng = random.Random(f"whoosh{long}{v}")
    dur = (0.75 + 0.08 * (v % 3)) if long else (0.26 + 0.03 * v)
    rising = v % 2 == 0
    f0, f1 = ((260 + 70 * v, 3600 + 500 * v) if long else (700 + 150 * v, 6000 + 600 * v))
    if not rising:
        f0, f1 = f1 * 0.7, f0 * 1.2
    bp, out = BP(1.4), []
    for i in range(n_samples(dur)):
        t = i / SR
        x = t / dur
        fc = f0 * (f1 / f0) ** x
        peak = 0.55 if rising else 0.4
        env = (x / peak) ** 1.5 if x < peak else max(0.0, 1 - (x - peak) / (1 - peak)) ** 1.8
        out.append(bp(rng.uniform(-1, 1), fc) * env * 2.2)
    return out


def pop(v):
    base = [620, 700, 780, 860][v % 4]
    dur, out, ph = 0.2, [], 0.0
    rng = random.Random(f"pop{v}")
    for i in range(n_samples(dur)):
        t = i / SR
        f = base * (0.55 + 0.45 * math.exp(-t / 0.025))
        ph += TAU * f / SR
        s = math.sin(ph) * math.exp(-t / 0.055)
        s += rng.uniform(-1, 1) * math.exp(-t / 0.002) * 0.35
        out.append(s)
    return out


def tick(v):
    f = [3200, 3600, 4000, 2800][v % 4]
    dur, out = 0.09, []
    for i in range(n_samples(dur)):
        t = i / SR
        out.append(math.sin(TAU * f * t) * math.exp(-t / 0.012) + (0.6 if i < 4 else 0))
    return out


def click(v):
    rng = random.Random(f"click{v}")
    lp = LP(1800 + 300 * v)
    dur, out = 0.07, []
    for i in range(n_samples(dur)):
        t = i / SR
        n = rng.uniform(-1, 1)
        hp = n - lp(n)
        out.append(hp * math.exp(-t / 0.007) + math.sin(TAU * (170 + 25 * v) * t) * math.exp(-t / 0.02) * 0.5)
    return out


def hit(v):
    rng = random.Random(f"hit{v}")
    base = 44 + 5 * v
    lp1, lp2 = LP(900), LP(320)
    dur, out, ph = 1.1, [], 0.0
    for i in range(n_samples(dur)):
        t = i / SR
        f = base + 90 * math.exp(-t / 0.055)
        ph += TAU * f / SR
        body = math.sin(ph) * math.exp(-t / 0.28)
        n = rng.uniform(-1, 1)
        thump = lp1(n) * math.exp(-t / 0.05) * 0.7
        tail = lp2(n) * math.exp(-t / 0.42) * 0.22
        out.append(body + thump + tail)
    return out


def riser(v):
    rng = random.Random(f"riser{v}")
    lo, hi = 260 + 60 * v, 4800 + 500 * v
    dur = 1.25 + 0.1 * (v % 2)
    bp, out, ph = BP(2.2), [], 0.0
    for i in range(n_samples(dur)):
        t = i / SR
        x = t / dur
        fc = lo * (hi / lo) ** x
        ph += TAU * (180 + 1100 * x ** 1.5) / SR
        amp = x ** 2.2
        out.append((bp(rng.uniform(-1, 1), fc) * 2.0 + math.sin(ph) * 0.18) * amp)
    return out


SCALE = [523.25, 587.33, 659.25, 783.99, 880.0]  # C D E G A pentatonic: any order sounds pleasant


def chime(v):
    f0 = SCALE[v % 5]
    dur, out = 1.1, []
    for i in range(n_samples(dur)):
        t = i / SR
        s = (math.sin(TAU * f0 * t) * math.exp(-t / 0.38)
             + 0.35 * math.sin(TAU * f0 * 2.0 * t) * math.exp(-t / 0.2)
             + 0.15 * math.sin(TAU * f0 * 3.01 * t) * math.exp(-t / 0.1))
        out.append(s * min(1.0, t / 0.003))
    return out


def sparkle(v):
    rng = random.Random(f"sparkle{v}")
    dur = 0.85
    blips = [(rng.uniform(0, 0.5), rng.uniform(3000, 8200), rng.uniform(0.4, 1.0)) for _ in range(7 + v)]
    out = []
    for i in range(n_samples(dur)):
        t = i / SR
        s = 0.0
        for st, f, a in blips:
            if t >= st:
                d = t - st
                s += math.sin(TAU * f * d) * math.exp(-d / 0.06) * a
        out.append(s * 0.35)
    return out


def draw(v):
    rng = random.Random(f"draw{v}")
    dur = 0.6 + 0.08 * v
    bp, out = BP(3.0), []
    for i in range(n_samples(dur)):
        t = i / SR
        x = t / dur
        out.append(bp(rng.uniform(-1, 1), 700 + 1700 * x + 150 * v) * math.sin(math.pi * x) ** 1.5 * 1.6)
    return out


def counter(v):
    f = [1800, 2000, 2200, 2400][v % 4]
    dur, out = 0.055, []
    for i in range(n_samples(dur)):
        t = i / SR
        out.append(math.sin(TAU * f * t) * math.exp(-t / 0.009))
    return out


def swell(v):
    semis = [0, 2, 4, 5][v % 4]
    k = 2 ** (semis / 12)
    freqs = [220 * k, 277.18 * k, 329.63 * k, 440 * k]
    dur, out = 1.7, []
    for i in range(n_samples(dur)):
        t = i / SR
        x = t / dur
        env = math.sin(math.pi * x) ** 2
        s = sum(math.sin(TAU * f * t) + 0.5 * math.sin(TAU * f * 1.004 * t) for f in freqs) / 8
        out.append(s * env * (1 + 0.08 * math.sin(TAU * 5 * t)))
    return out


# name -> (generator, number of variants, default volume 0..1, short description)
LIBRARY = {
    "whoosh": (lambda v: whoosh(v, True), 4, 0.40, "scene transition"),
    "swipe": (lambda v: whoosh(v, False), 4, 0.35, "panel or image slides in"),
    "pop": (pop, 4, 0.45, "element appears"),
    "tick": (tick, 4, 0.30, "list item or step highlight"),
    "click": (click, 4, 0.20, "kinetic text word"),
    "hit": (hit, 4, 0.55, "heavy impact for the hero moment"),
    "riser": (riser, 4, 0.35, "tension build before a reveal"),
    "chime": (chime, 5, 0.40, "success / checkmark (ascending notes)"),
    "sparkle": (sparkle, 4, 0.30, "image or media reveal"),
    "draw": (draw, 4, 0.22, "line or diagram drawing on"),
    "counter": (counter, 4, 0.18, "number counting tick"),
    "swell": (swell, 4, 0.22, "soft pad for diagrams and emphasis"),
}


def finish(samples):
    """Remove DC offset, fade the edges, normalise to -3 dB peak."""
    mean = sum(samples) / len(samples)
    s = [x - mean for x in samples]
    fi, fo = int(0.003 * SR), int(0.015 * SR)
    for i in range(min(fi, len(s))):
        s[i] *= i / fi
    for i in range(min(fo, len(s))):
        s[-1 - i] *= i / fo
    peak = max(abs(x) for x in s) or 1.0
    return [x / peak * 0.7 for x in s]


def write_wav(path, samples):
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, x)) * 32767)) for x in samples))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="public/audio/sfx")
    ap.add_argument("--manifest", default="src/audio/sfx.generated.ts")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    manifest, total = {}, 0
    for name, (gen, n, vol, desc) in LIBRARY.items():
        files, durs = [], []
        for v in range(n):
            s = finish(gen(v))
            fn = f"{name}-{v + 1}.wav"
            write_wav(os.path.join(a.out, fn), s)
            files.append(fn)
            durs.append(round(len(s) / SR, 3))
            total += os.path.getsize(os.path.join(a.out, fn))
        manifest[name] = {"files": files, "durations": durs, "volume": vol, "use": desc}
    os.makedirs(os.path.dirname(os.path.abspath(a.manifest)), exist_ok=True)
    with open(a.manifest, "w", encoding="utf-8") as f:
        f.write("// Generated by scripts/generate_sfx.py. Original synthesized sounds (royalty-free).\n"
                "export type SfxName = " + " | ".join(f"'{k}'" for k in manifest) + ";\n"
                "export const SFX: Record<SfxName, {files: string[]; durations: number[]; volume: number; use: string}> = "
                + json.dumps(manifest, indent=2) + ";\n")
    print(f"{sum(m['files'].__len__() for m in manifest.values())} sounds, {total / 1024 / 1024:.2f} MB -> {a.out}")


if __name__ == "__main__":
    main()
