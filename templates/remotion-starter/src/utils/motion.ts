import {Easing, interpolate, useCurrentFrame} from 'remotion';

/** Expo-out style curve: fast start, long soft settle. Premium default for entrances. */
export const easeOut = Easing.bezier(0.16, 1, 0.3, 1);
export const easeInOut = Easing.bezier(0.65, 0, 0.35, 1);

/** 0 -> 1 progress between `delay` and `delay + duration` (scene-local frames). */
export const useReveal = (delay = 0, duration = 18, easing = easeOut): number => {
  const frame = useCurrentFrame();
  return interpolate(frame, [delay, delay + duration], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing,
  });
};

/** Constant stagger between items in a group (frames at 30 fps). */
export const STAGGER = 6;
/** Frames that consecutive scenes overlap for cross-transitions. */
export const OVERLAP = 14;
