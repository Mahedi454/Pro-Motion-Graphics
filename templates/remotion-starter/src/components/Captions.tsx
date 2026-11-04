import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {CAPTIONS_FPS, cues} from '../data/captions';
import {colors, fonts, safe} from '../styles/tokens';
import {noSpaces, words as splitWords} from '../utils/text';

/**
 * Shift all captions (in frames) if the narration audio starts earlier/later than the SRT.
 * Positive = captions appear later. Example: audio has 0.5 s of leading silence -> 15.
 */
export const CAPTION_OFFSET_FRAMES = 0;

/** SRT-driven captions. Place once in Main (global frame). Words brighten in proportion to their length. */
export const Captions: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  // Convert cue frames if the SRT data was generated at a different fps than the composition.
  const k = fps / CAPTIONS_FPS;
  const f = frame - CAPTION_OFFSET_FRAMES;

  // If cues overlap, show the one that started most recently.
  let cue: (typeof cues)[number] | undefined;
  for (const c of cues) {
    if (f >= c.startFrame * k && f < c.endFrame * k) cue = c;
  }
  if (!cue) return null;

  const start = cue.startFrame * k;
  const len = Math.max(1, cue.endFrame * k - start);
  const local = f - start;
  const fade = Math.min(6, Math.floor(len / 3)); // short cues get a shorter fade (never a bad range)
  const opacity =
    fade < 1
      ? 1
      : interpolate(local, [0, fade, len - fade, len], [0, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });

  // Word timing weighted by character count (closer to real speech than equal slices).
  const words = splitWords(cue.text);
  const weights = words.map((w) => w.length + 1);
  const total = weights.reduce((a, b) => a + b, 0);
  const progress = Math.min(1, Math.max(0, local / (len * 0.92))) * total;
  let acc = 0;

  return (
    <div
      style={{
        position: 'absolute',
        left: safe.x,
        right: safe.x,
        bottom: safe.y,
        display: 'flex',
        justifyContent: 'center',
        opacity,
        transform: `translateY(${(1 - opacity) * 12}px)`,
      }}
    >
      <div
        style={{
          maxWidth: 1400,
          padding: '14px 32px',
          borderRadius: 18,
          background: colors.veil,
          backdropFilter: 'blur(10px)',
          border: `1px solid ${colors.panelLine}`,
          fontFamily: fonts.body,
          fontSize: 44,
          fontWeight: 600,
          lineHeight: 1.3,
          textAlign: 'center',
        }}
      >
        {words.map((w, i) => {
          const spoken = progress >= acc + weights[i] / 2;
          acc += weights[i];
          return (
            <span key={i} style={{color: spoken ? colors.text : colors.muted}}>
              {w}{noSpaces ? '' : ' '}
            </span>
          );
        })}
      </div>
    </div>
  );
};
