import {LANG} from '../data/language';

/** Sentence-ending punctuation across scripts: . ! ? 。！？ । ॥ ۔ ؟ ։ ። ។ … */
const END = '.!?\\u3002\\uff01\\uff1f\\uff61\\u0964\\u0965\\u061f\\u06d4\\u0589\\u1362\\u17d4\\u17d5\\u2026';
const END_RE = new RegExp(`[^${END}]+[${END}]*`, 'g');
const TRAIL_RE = new RegExp(`[\\s,;:\\u3001\\u060c\\u061b\\uff0c\\uff1b${END}]+$`);

/** Does this video's script write words without spaces (Thai, Lao, Khmer, Myanmar, Chinese, Japanese)? */
export const noSpaces = LANG.noSpaces;
/** Scripts where uppercase, wide letter-spacing and negative tracking make sense. */
export const isCasedLatin = ['latin', 'cyrillic', 'greek'].includes(LANG.script);
export const rtl = LANG.rtl;
/** +1 for left-to-right, -1 for right-to-left: multiply horizontal slide offsets by this. */
export const dirSign = rtl ? -1 : 1;
/** Letter-spacing only for cased scripts; joined/Indic/Arabic scripts must not be tracked. */
export const tracking = (px: number): number => (isCasedLatin ? px : 0);

const LEAD_RE = /^(and|but|so|then|or|while|whereas)\s+/i;

/** Remove leading English conjunctions and trailing punctuation so fragments read as clean labels. */
export const clean = (text: string): string => {
  const t = text.trim().replace(LEAD_RE, '').replace(TRAIL_RE, '');
  return isCasedLatin ? t.charAt(0).toUpperCase() + t.slice(1) : t;
};

/** Split into display words. Uses the browser's word segmenter, so Thai/Chinese/Japanese split correctly. */
export const words = (text: string): string[] => {
  const t = text.trim();
  if (!t) return [];
  if (!noSpaces) return t.split(/\s+/).filter(Boolean);
  const Seg = (Intl as unknown as {Segmenter?: new (l: string, o: object) => {segment: (s: string) => Iterable<{segment: string; isWordLike?: boolean}>}}).Segmenter;
  const out: string[] = [];
  if (Seg) {
    for (const s of new Seg(LANG.code, {granularity: 'word'}).segment(t)) {
      if (!s.segment.trim()) continue;
      if (s.isWordLike === false && out.length) out[out.length - 1] += s.segment; // attach punctuation
      else out.push(s.segment);
    }
    return out;
  }
  return Array.from(t.replace(/\s+/g, '')); // fallback: one character per unit
};

/** Join display words back together with the right separator for the script. */
export const joinWords = (w: string[]): string => w.join(noSpaces ? '' : ' ');

/** Split narration into sentences (any script). */
export const sentences = (text: string): string[] =>
  (text.match(END_RE) ?? [text]).map((s) => s.trim()).filter(Boolean);

/** Shorten to at most `n` words (about 1.5n segmented words for scripts without spaces). */
export const shorten = (text: string, n = 8): string => {
  const c = clean(text);
  if (noSpaces) {
    const w = words(c); // the segmenter keeps words whole (Thai, Chinese, Japanese)
    return w.length <= n * 1.5 ? c : w.slice(0, Math.round(n * 1.5)).join('') + '…';
  }
  const w = c.split(/\s+/);
  return w.length <= n ? w.join(' ') : w.slice(0, n).join(' ') + '…';
};

/** Split into clause-like chunks for steps/lists. */
export const chunks = (text: string, max = 4): string[] => {
  const parts = text
    .split(new RegExp(`[${END}\\u3001\\u060c\\uff0c;]|,\\s+|\\bthen\\b|\\band then\\b|\\bnext\\b|\\bfinally\\b`, 'i'))
    .map(clean)
    .filter((s) => s.length > 1);
  return (parts.length ? parts : [clean(text)]).slice(0, max);
};

// ---- numbers in any digit system (Arabic-Indic, Bengali, Devanagari, Thai, full-width, ...)
const ZEROS: Array<[number, string]> = [
  [0x30, 'latn'], [0x660, 'arab'], [0x6f0, 'arabext'], [0x966, 'deva'], [0x9e6, 'beng'], [0xa66, 'guru'],
  [0xae6, 'gujr'], [0xb66, 'orya'], [0xbe6, 'tamldec'], [0xc66, 'telu'], [0xce6, 'knda'], [0xd66, 'mlym'],
  [0xe50, 'thai'], [0xed0, 'laoo'], [0x1040, 'mymr'], [0x17e0, 'khmr'], [0xff10, 'fullwide'],
];
const zeroOf = (cp: number) => ZEROS.find(([z]) => cp >= z && cp <= z + 9);

/** Find the first number in `text`, in any digit system. Returns its value, decimals, system and % flag. */
export const findNumber = (text: string): {value: number; decimals: number; system: string; percent: boolean} | null => {
  const m = text.match(/\p{Nd}[\p{Nd},٬]*(?:[.٫]\p{Nd}+)?\s*(%|٪|％|percent)?/u);
  if (!m) return null;
  let system = 'latn';
  let ascii = '';
  for (const ch of m[0]) {
    const cp = ch.codePointAt(0) as number;
    const z = zeroOf(cp);
    if (z) {
      ascii += String(cp - z[0]);
      if (z[1] !== 'latn') system = z[1];
    } else if (ch === '.' || ch === '٫') ascii += '.';
  }
  const value = parseFloat(ascii);
  if (Number.isNaN(value)) return null;
  const decimals = ascii.includes('.') ? ascii.split('.')[1].length : 0;
  return {value, decimals, system, percent: Boolean(m[1])};
};

/** Format a number in the digit system the narration used. */
export const formatNumber = (v: number, decimals: number, system: string): string =>
  v.toLocaleString(`en-u-nu-${system}`, {minimumFractionDigits: decimals, maximumFractionDigits: decimals});
