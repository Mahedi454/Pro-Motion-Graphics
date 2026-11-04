import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {colors, fonts, safe} from '../styles/tokens';
import {Background} from './Background';
import {easeInOut, OVERLAP} from '../utils/motion';
import {rtl} from '../utils/text';
import {Sfx, sceneNo} from './Sfx';

/**
 * Wraps every scene: ambient background, slow camera push, accent wipe on entry,
 * fade-in over the previous scene (cross-transition) and optional fade-out at the end.
 */
export const SceneShell: React.FC<{
  seed: string;
  children: React.ReactNode;
  fadeOut?: boolean;
  padded?: boolean;
  /** transition sound: 'auto' alternates whoosh/swipe scene by scene, 'none' = the scene adds its own */
  transition?: 'auto' | 'whoosh' | 'swipe' | 'none';
}> = ({seed, children, fadeOut = false, padded = true, transition = 'auto'}) => {
  const frame = useCurrentFrame();
  const {durationInFrames, width} = useVideoConfig();

  const fadeIn = interpolate(frame, [0, OVERLAP], [0, 1], {extrapolateRight: 'clamp'});
  const out = fadeOut ? interpolate(frame, [durationInFrames - 20, durationInFrames], [1, 0], {extrapolateLeft: 'clamp'}) : 1;
  const push = interpolate(frame, [0, durationInFrames], [1, 1.035], {easing: easeInOut});
  const wipe = interpolate(frame, [0, OVERLAP + 6], [0, 1], {extrapolateRight: 'clamp', easing: easeInOut});

  return (
    <AbsoluteFill style={{opacity: Math.min(fadeIn, out)}}>
      {transition !== 'none' && (
        <Sfx
          name={transition === 'auto' ? (sceneNo(seed) % 2 === 0 ? 'whoosh' : 'swipe') : transition}
          at={0}
          seed={sceneNo(seed)}
          volume={0.9}
        />
      )}
      <Background seed={seed} />
      <AbsoluteFill
        style={{
          color: colors.text,
          fontFamily: fonts.body,
          transform: `scale(${push})`,
          padding: padded ? `${safe.y}px ${safe.x}px ${safe.y + 120}px` : 0,
          justifyContent: 'center',
        }}
      >
        {children}
      </AbsoluteFill>
      {/* accent sweep: a thin light bar crossing the frame as the scene arrives */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          bottom: 0,
          left: rtl ? width - (wipe * (width + 400) - 400) - 6 : wipe * (width + 400) - 400, // sweeps in reading direction
          width: 6,
          background: `linear-gradient(to bottom, transparent, ${colors.accent}, transparent)`,
          opacity: wipe < 1 ? 0.7 : 0,
          filter: 'blur(2px)',
        }}
      />
    </AbsoluteFill>
  );
};
