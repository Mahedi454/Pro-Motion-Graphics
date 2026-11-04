import {Audio, Sequence, staticFile, useVideoConfig} from 'remotion';
import {SFX, type SfxName} from '../audio/sfx.generated';
import {SFX_ENABLED, SFX_VOLUME} from '../audio/config';

/** Stable pseudo-random number in [0,1) from a string, so renders are identical every time. */
const hash01 = (s: string): number => {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return ((h >>> 0) % 10000) / 10000;
};

/** Scene number from an id like "S07" (used to make neighbouring scenes sound different). */
export const sceneNo = (id: string): number => parseInt(id.replace(/\D/g, ''), 10) || 0;

/**
 * Plays one sound effect at a scene-local frame.
 *  - `seed` (number): rotates through the sound's variants, so repeated animations never sound the same.
 *  - `variant`: force a specific variant (e.g. ascending chime notes).
 *  - `rate`: playback speed, i.e. pitch. A small deterministic jitter is added unless `rate` is given.
 *  - `volume`: relative to the sound's default level; the master SFX_VOLUME is applied on top.
 */
export const Sfx: React.FC<{
  name: SfxName;
  at?: number;
  seed?: number;
  variant?: number;
  rate?: number;
  volume?: number;
}> = ({name, at = 0, seed = 0, variant, rate, volume = 1}) => {
  const {fps} = useVideoConfig();
  if (!SFX_ENABLED) return null;
  const def = SFX[name];
  const v = (variant ?? seed) % def.files.length;
  const playbackRate = rate ?? 0.94 + hash01(`${name}-${seed}-${at}`) * 0.12; // +-6 % pitch variation
  const frames = Math.ceil((def.durations[v] / playbackRate) * fps) + 2;
  return (
    <Sequence from={Math.max(0, Math.round(at))} durationInFrames={frames} layout="none" name={`sfx:${name}`}>
      <Audio
        src={staticFile(`audio/sfx/${def.files[v]}`)}
        volume={Math.min(1, def.volume * volume * SFX_VOLUME)}
        playbackRate={playbackRate}
      />
    </Sequence>
  );
};
