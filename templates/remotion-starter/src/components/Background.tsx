import {AbsoluteFill, interpolate, random, useCurrentFrame, useVideoConfig} from 'remotion';
import {alpha, colors} from '../styles/tokens';

/**
 * Ambient 3-layer background: drifting gradient, parallax grid, deterministic particles.
 * Low contrast on purpose: it keeps frames alive without competing with the lesson.
 */
export const Background: React.FC<{seed?: string; intensity?: number}> = ({seed = 'bg', intensity = 1}) => {
  const frame = useCurrentFrame();
  const {durationInFrames, width, height} = useVideoConfig();
  const t = frame / Math.max(1, durationInFrames);
  const gx = interpolate(t, [0, 1], [25, 75]);
  const gy = interpolate(t, [0, 1], [30, 60]);

  return (
    <AbsoluteFill style={{backgroundColor: colors.bg, overflow: 'hidden'}}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(900px circle at ${gx}% ${gy}%, ${colors.glow}, transparent 60%),
                       radial-gradient(1200px circle at ${100 - gx}% 90%, ${colors.bgAlt}, transparent 70%)`,
        }}
      />
      <AbsoluteFill
        style={{
          backgroundImage: `linear-gradient(${colors.grid} 1px, transparent 1px), linear-gradient(90deg, ${colors.grid} 1px, transparent 1px)`,
          backgroundSize: '96px 96px',
          backgroundPosition: `${-frame * 0.35}px ${-frame * 0.2}px`,
          opacity: 0.5 * intensity,
          maskImage: 'radial-gradient(ellipse at center, black 30%, transparent 80%)',
          WebkitMaskImage: 'radial-gradient(ellipse at center, black 30%, transparent 80%)',
        }}
      />
      {new Array(22).fill(0).map((_, i) => {
        const x = random(`${seed}-x-${i}`) * width;
        const y0 = random(`${seed}-y-${i}`) * height;
        const speed = 0.15 + random(`${seed}-s-${i}`) * 0.5;
        const size = 2 + random(`${seed}-z-${i}`) * 4;
        const y = (((y0 - frame * speed) % height) + height) % height;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x,
              top: y,
              width: size,
              height: size,
              borderRadius: '50%',
              background: colors.accent,
              opacity: (0.12 + random(`${seed}-o-${i}`) * 0.25) * intensity,
              filter: 'blur(0.5px)',
            }}
          />
        );
      })}
      <AbsoluteFill style={{background: `radial-gradient(ellipse at center, transparent 55%, ${alpha(colors.bg, 0.65)})`}} />
    </AbsoluteFill>
  );
};
