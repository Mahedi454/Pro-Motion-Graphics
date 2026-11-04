import themes from './themes.json';
import {ACTIVE_THEME} from './theme.config';
import {fontStack} from './fonts';

type Theme = {id: string; name: string; mood?: string; bg: string; text: string; accent: string; hero: string};

const hexToRgb = (hex: string): [number, number, number] => {
  const h = hex.replace('#', '');
  const f = h.length === 3 ? h.split('').map((c) => c + c).join('') : h;
  return [parseInt(f.slice(0, 2), 16), parseInt(f.slice(2, 4), 16), parseInt(f.slice(4, 6), 16)];
};
/** hex + opacity -> rgba() string */
export const alpha = (hex: string, a: number): string => {
  const [r, g, b] = hexToRgb(hex);
  return `rgba(${r},${g},${b},${a})`;
};
/** Blend a toward b by t (0..1) -> hex */
export const mix = (a: string, b: string, t: number): string => {
  const x = hexToRgb(a);
  const y = hexToRgb(b);
  const c = x.map((v, i) => Math.round(v + (y[i] - v) * t));
  return '#' + c.map((v) => v.toString(16).padStart(2, '0')).join('');
};

const all = themes as Theme[];
export const theme: Theme = all.find((t) => t.id === ACTIVE_THEME) ?? all[0];

/**
 * Every colour in the video comes from the 4 theme colours:
 *   bg (background), text, accent (primary UI colour), hero (the focal highlight).
 * Everything else is derived, so changing the theme restyles the whole video.
 */
export const colors = {
  bg: theme.bg,
  text: theme.text,
  accent: theme.accent,
  hero: theme.hero,
  bgAlt: mix(theme.bg, theme.accent, 0.14),
  muted: mix(theme.text, theme.bg, 0.4),
  glow: alpha(theme.accent, 0.22),
  grid: alpha(theme.text, 0.08),
  panel: alpha(theme.text, 0.06),
  panelLine: alpha(theme.text, 0.1),
  veil: alpha(theme.bg, 0.8), // caption pill / overlays
  good: '#22A06B',
};
// Language-aware: Inter for Latin/Cyrillic/Greek, the matching Noto font for other scripts (see fonts.ts).
export const fonts = {
  heading: fontStack,
  body: fontStack,
};
export const safe = {x: 120, y: 90}; // safe margins at 1920x1080
