import {interpolate, useCurrentFrame} from 'remotion';
import {colors, fonts} from '../styles/tokens';
import {easeOut, STAGGER} from '../utils/motion';
import {noSpaces, tracking, words as splitWords} from '../utils/text';
import {Sfx} from './Sfx';

/** Word-by-word masked reveal. Words listed in `highlight` take the accent colour. */
export const KineticText: React.FC<{
  text: string;
  delay?: number;
  fontSize?: number;
  weight?: number;
  highlight?: string[];
  align?: 'left' | 'center';
  maxWidth?: number;
  color?: string;
  sfx?: boolean; // soft click per word (different pitch each time)
  sfxSeed?: number;
}> = ({text, delay = 0, fontSize = 96, weight = 800, highlight = [], align = 'left', maxWidth = 1500, color = colors.text, sfx = true, sfxSeed = 0}) => {
  const frame = useCurrentFrame();
  const words = splitWords(text);
  const norm = (s: string) => s.toLowerCase().replace(/[^\p{L}\p{M}\p{N}%]/gu, ''); // keep combining marks
  const hl = highlight.map(norm);

  return (
    <div
      style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: `0 ${noSpaces ? 0 : fontSize * 0.28}px`,
        justifyContent: align === 'center' ? 'center' : 'flex-start', // flex-start follows text direction (right edge in RTL)
        maxWidth,
        fontFamily: fonts.heading,
        fontSize,
        fontWeight: weight,
        lineHeight: 1.12,
        letterSpacing: tracking(-fontSize * 0.01),
        color,
      }}
    >
      {sfx && words.slice(0, 8).map((_, i) => (
        <Sfx key={`s${i}`} name="click" at={delay + i * STAGGER + 2} seed={sfxSeed + i} rate={0.9 + ((i * 37) % 11) / 40} volume={0.8} />
      ))}
      {words.map((w, i) => {
        const p = interpolate(frame, [delay + i * STAGGER, delay + i * STAGGER + 20], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: easeOut,
        });
        const isHl = hl.includes(norm(w));
        return (
          <span key={i} style={{display: 'inline-block', overflow: 'hidden', paddingBottom: fontSize * 0.1}}>
            <span
              style={{
                display: 'inline-block',
                transform: `translateY(${(1 - p) * 110}%)`,
                opacity: p,
                filter: `blur(${(1 - p) * 6}px)`,
                color: isHl ? colors.hero : undefined,
              }}
            >
              {w}
            </span>
          </span>
        );
      })}
    </div>
  );
};
