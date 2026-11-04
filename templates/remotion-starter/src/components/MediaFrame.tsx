import {Img, OffthreadVideo, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {easeOut} from '../utils/motion';
import {Sfx} from './Sfx';

const isVideo = (name: string) => /\.(mp4|mov|webm|m4v|mkv)$/i.test(name);

/**
 * Reference image/video presented as a rounded card with Ken Burns motion and soft shadow.
 * `file` is a name inside public/media/. Videos are muted (narration leads).
 */
export const MediaFrame: React.FC<{
  file: string;
  width?: number | string;
  height?: number | string;
  radius?: number;
  fullBleed?: boolean;
  delay?: number;
  sfxSeed?: number;
}> = ({file, width = 900, height = 620, radius = 28, fullBleed = false, delay = 0, sfxSeed = 0}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const enter = interpolate(frame, [delay, delay + 24], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: easeOut,
  });
  const zoom = interpolate(frame, [0, durationInFrames], [1.02, 1.1]);
  const panX = interpolate(frame, [0, durationInFrames], [0, -2.5]);
  const src = staticFile(`media/${file}`);
  const style: React.CSSProperties = {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
    transform: `scale(${zoom}) translateX(${panX}%)`,
  };

  return (
    <div
      style={{
        width: fullBleed ? '100%' : width,
        height: fullBleed ? '100%' : height,
        borderRadius: fullBleed ? 0 : radius,
        overflow: 'hidden',
        opacity: enter,
        transform: fullBleed ? undefined : `translateY(${(1 - enter) * 40}px) scale(${0.94 + enter * 0.06})`,
        boxShadow: fullBleed ? undefined : '0 40px 90px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.08)',
      }}
    >
      <Sfx name="sparkle" at={delay + 4} seed={sfxSeed} />
      {isVideo(file) ? <OffthreadVideo src={src} muted style={style} /> : <Img src={src} style={style} />}
    </div>
  );
};
