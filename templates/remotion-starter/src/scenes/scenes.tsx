import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import type {SceneData} from '../data/scenes';
import {KineticText} from '../components/KineticText';
import {MediaFrame} from '../components/MediaFrame';
import {SceneShell} from '../components/SceneShell';
import {Sfx, sceneNo} from '../components/Sfx';
import {colors, fonts} from '../styles/tokens';
import {easeOut, STAGGER, useReveal} from '../utils/motion';
import {chunks, dirSign, findNumber, formatNumber, isCasedLatin, rtl, sentences, shorten, tracking} from '../utils/text';

export type SceneProps = {scene: SceneData; isLast: boolean};

const Kicker: React.FC<{text: string; delay?: number; color?: string}> = ({text, delay = 0, color = colors.accent}) => {
  const p = useReveal(delay, 16);
  if (!text) return null; // chapter label is optional; write it in the video's language
  return (
    <div
      style={{
        fontFamily: fonts.body,
        fontSize: 30,
        fontWeight: 700,
        letterSpacing: tracking(6),
        textTransform: isCasedLatin ? 'uppercase' : 'none',
        color,
        opacity: p,
        transform: `translateX(${(1 - p) * -30 * dirSign}px)`,
        marginBottom: 28,
      }}
    >
      {text}
    </div>
  );
};

const Rule: React.FC<{delay?: number; width?: number; seed?: number}> = ({delay = 0, width = 220, seed = 0}) => {
  const p = useReveal(delay, 24);
  return <><Sfx name="draw" at={delay} seed={seed} volume={0.8} /><div style={{height: 6, width: width * p, borderRadius: 3, background: `linear-gradient(90deg, ${colors.accent}, ${colors.hero})`, marginTop: 36}} /></>;
};

const ringGrow = (frame: number, i: number): number =>
  interpolate(frame, [i * STAGGER, i * STAGGER + 30], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: easeOut});

const focusWords = (t: string) => t.split(/\s+/).filter((w) => w.length > 5).slice(0, 2);

/** HOOK: one bold line, accent rule, big push. Replace with a bespoke hero animation for best results. */
export const HookScene: React.FC<SceneProps> = ({scene, isLast}) => {
  const n = sceneNo(scene.id);
  return (
    <SceneShell seed={scene.id} fadeOut={isLast} transition="none">
      <Sfx name="riser" at={0} seed={n} /> {/* tension builds ... */}
      <Sfx name="hit" at={34} seed={n} /> {/* ... and lands with the headline */}
      <Kicker text={scene.label} />
      <KineticText text={scene.onScreenText || shorten(scene.narration, 8)} fontSize={130} highlight={focusWords(scene.onScreenText)} delay={8} sfxSeed={n} />
      <Rule delay={34} seed={n} />
    </SceneShell>
  );
};

/** CONCEPT: text left, reference media (or animated orbit diagram) right. */
export const ConceptScene: React.FC<SceneProps> = ({scene, isLast}) => {
  const frame = useCurrentFrame();
  const media = scene.assets[0];
  const spin = frame * 0.6;
  const n = sceneNo(scene.id);
  return (
    <SceneShell seed={scene.id} fadeOut={isLast}>
      <div style={{display: 'flex', alignItems: 'center', gap: 80}}>
        <div style={{flex: 1}}>
          <Kicker text={scene.label} />
          <KineticText text={scene.onScreenText || shorten(scene.narration, 6)} fontSize={96} maxWidth={820} highlight={focusWords(scene.onScreenText)} delay={6} sfxSeed={n} />
          <Rule delay={20} seed={n} />
        </div>
        <div style={{flex: 1, display: 'flex', justifyContent: 'center'}}>
          {!media && <Sfx name="swell" at={4} seed={n} />} {/* diagram rings grow under a soft pad */}
          {media ? (
            <MediaFrame file={media} delay={10} sfxSeed={n} />
          ) : (
            <svg width={620} height={620} viewBox="-310 -310 620 620">
              {[120, 200, 280].map((r, i) => (
                <circle key={r} r={r * ringGrow(frame, i)} fill="none" stroke={colors.accent} strokeOpacity={0.25 + i * 0.1} strokeWidth={3} />
              ))}
              {[0, 1, 2].map((i) => {
                const a = ((spin + i * 120) * Math.PI) / 180;
                const r = 120 + i * 80;
                return <circle key={i} cx={Math.cos(a) * r} cy={Math.sin(a) * r} r={16} fill={i === 0 ? colors.hero : colors.accent} />;
              })}
              <circle r={44} fill={colors.hero} />
            </svg>
          )}
        </div>
      </div>
    </SceneShell>
  );
};

/** STAT: counter animates to the first number in the narration. */
export const StatScene: React.FC<SceneProps> = ({scene, isLast}) => {
  const frame = useCurrentFrame();
  const num = findNumber(scene.narration);
  if (!num) return <ConceptScene scene={scene} isLast={isLast} />; // no number to count: fall back
  const isPct = num.percent;
  const target = num.value;
  const p = interpolate(frame, [6, 54], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: easeOut});
  const value = formatNumber(target * p, num.decimals, num.system); // keeps the narration's digit system
  const bars = 20;
  const n = sceneNo(scene.id);
  return (
    <SceneShell seed={scene.id} fadeOut={isLast}>
      {new Array(12).fill(0).map((_, i) => (
        <Sfx key={i} name="counter" at={6 + i * 4} seed={n + i} rate={0.85 + i * 0.06} /> // pitch climbs as the number climbs
      ))}
      <Sfx name="hit" at={54} seed={n} volume={0.7} />
      <Sfx name="sparkle" at={56} seed={n} volume={0.7} />
      <Kicker text={scene.label} />
      <div style={{fontFamily: fonts.heading, fontSize: 300, fontWeight: 900, lineHeight: 1, color: colors.text, letterSpacing: tracking(-8)}}>
        {value}
        {isPct ? <span style={{color: colors.hero}}>%</span> : null}
      </div>
      <div style={{display: 'flex', gap: 10, marginTop: 40}}>
        {new Array(bars).fill(0).map((_, i) => {
          // percentages fill proportionally; other numbers fill the whole meter as the count lands
          const on = i / bars < (isPct ? Math.min(1, target / 100) : 1) * p;
          return <div key={i} style={{width: 36, height: 14, borderRadius: 7, background: on ? colors.accent : colors.panelLine}} />;
        })}
      </div>
      <div style={{fontFamily: fonts.body, fontSize: 44, color: colors.muted, marginTop: 36, maxWidth: 1300}}>
        {shorten(scene.narration, 14)}
      </div>
    </SceneShell>
  );
};

/** STEPS: numbered nodes joined by a drawing line; the active step follows the scene time. */
export const StepsScene: React.FC<SceneProps> = ({scene, isLast}) => {
  const frame = useCurrentFrame();
  const {durationInFrames, fps} = useVideoConfig();
  const items = chunks(scene.narration, 4).map((s) => shorten(s, 7));
  const active = Math.min(items.length - 1, Math.floor((frame / durationInFrames) * items.length));
  const line = useReveal(6, 40);
  const n = sceneNo(scene.id);
  return (
    <SceneShell seed={scene.id} fadeOut={isLast}>
      <Sfx name="draw" at={6} seed={n} /> {/* the connecting line draws */}
      {items.map((_, i) => (
        <Sfx key={`p${i}`} name="pop" at={10 + i * STAGGER * 2} seed={n + i} /> // each step pops in with a different pop
      ))}
      {items.slice(1).map((_, k) => (
        <Sfx key={`t${k}`} name="tick" at={Math.round(((k + 1) * durationInFrames) / items.length)} seed={n + k} /> // highlight moves on
      ))}
      <Kicker text={scene.label} />
      <div style={{position: 'relative', display: 'flex', gap: 40, marginTop: 20}}>
        <div style={{position: 'absolute', top: 56, insetInlineStart: 56, height: 6, width: `calc((100% - 112px) * ${line})`, background: `linear-gradient(${rtl ? 270 : 90}deg, ${colors.accent}, ${colors.hero})`, borderRadius: 3}} />
        {items.map((it, i) => {
          const pop = spring({frame: frame - 10 - i * STAGGER * 2, fps, config: {damping: 14, stiffness: 140}});
          const on = i === active;
          return (
            <div key={i} style={{flex: 1, transform: `translateY(${(1 - pop) * 40}px) scale(${on ? 1.04 : 1})`, opacity: pop}}>
              <div style={{width: 112, height: 112, borderRadius: 56, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: fonts.heading, fontWeight: 800, fontSize: 52, background: on ? colors.accent : colors.bgAlt, color: on ? colors.bg : colors.text, border: `3px solid ${colors.accent}`, boxShadow: on ? `0 0 60px ${colors.glow}` : 'none', position: 'relative'}}>
                {i + 1}
              </div>
              <div style={{fontFamily: fonts.body, fontSize: 40, fontWeight: 600, marginTop: 28, color: on ? colors.text : colors.muted}}>{it}</div>
            </div>
          );
        })}
      </div>
    </SceneShell>
  );
};

/** COMPARE: two panels slide in from opposite sides around a drawing divider. */
export const CompareScene: React.FC<SceneProps> = ({scene, isLast}) => {
  const parts = scene.narration.split(/\b(?:vs\.?|versus|whereas|while|unlike|compared (?:to|with))\b/i).map((s) => s.trim()).filter(Boolean);
  const [a, b] = parts.length >= 2 ? [parts[0], parts[1]] : [sentences(scene.narration)[0] ?? '', sentences(scene.narration)[1] ?? scene.onScreenText];
  const p = useReveal(4, 26);
  const n = sceneNo(scene.id);
  const panel = (text: string, dir: number, color: string, label: string) => (
    <div style={{flex: 1, padding: 48, borderRadius: 28, background: colors.panel, border: `2px solid ${color}`, transform: `translateX(${(1 - p) * dir * 160 * dirSign}px)`, opacity: p}}>
      <div style={{fontFamily: fonts.body, fontSize: 28, fontWeight: 800, letterSpacing: tracking(5), color}}>{label}</div>
      <div style={{fontFamily: fonts.heading, fontSize: 56, fontWeight: 700, marginTop: 20, lineHeight: 1.15}}>{shorten(text, 12)}</div>
    </div>
  );
  return (
    <SceneShell seed={scene.id} fadeOut={isLast}>
      <Sfx name="swipe" at={4} variant={n % 4} /> {/* panel A slides in */}
      <Sfx name="swipe" at={8} variant={(n + 2) % 4} rate={1.12} /> {/* panel B slides in: different variant and pitch */}
      <Sfx name="hit" at={28} seed={n} volume={0.5} /> {/* the divider settles */}
      <Kicker text={scene.label} />
      <div style={{display: 'flex', gap: 56, alignItems: 'stretch'}}>
        {panel(a, -1, colors.accent, 'A')}
        <div style={{width: 4, background: colors.muted, transform: `scaleY(${p})`, opacity: 0.6}} />
        {panel(b, 1, colors.hero, 'B')}
      </div>
    </SceneShell>
  );
};

/** RECAP: takeaways stack and get checked off in sequence. */
export const RecapScene: React.FC<SceneProps> = ({scene, isLast}) => {
  const frame = useCurrentFrame();
  const items = sentences(scene.narration).slice(0, 3).map((s) => shorten(s, 9));
  return (
    <SceneShell seed={scene.id} fadeOut={isLast}>
      {items.map((_, i) => (
        <Sfx key={i} name="chime" at={8 + i * 22 + 8} variant={i} /> // ascending notes: each check sounds higher
      ))}
      <Sfx name="sparkle" at={8 + items.length * 22 + 4} seed={sceneNo(scene.id)} volume={0.8} />
      <Kicker text={scene.label} />
      {items.map((it, i) => {
        const p = interpolate(frame, [8 + i * 22, 8 + i * 22 + 18], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: easeOut});
        return (
          <div key={i} style={{display: 'flex', alignItems: 'center', gap: 32, marginBottom: 36, opacity: p, transform: `translateX(${(1 - p) * 60 * dirSign}px)`}}>
            <div style={{width: 64, height: 64, borderRadius: 32, background: colors.good, color: colors.bg, fontSize: 40, fontWeight: 900, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${0.6 + p * 0.4})`}}>✓</div>
            <div style={{fontFamily: fonts.heading, fontSize: 64, fontWeight: 700}}>{it}</div>
          </div>
        );
      })}
    </SceneShell>
  );
};

/** MEDIA: full-bleed reference image/video with scrim and lower-third text. */
export const MediaScene: React.FC<SceneProps> = ({scene, isLast}) => {
  const media = scene.assets[0];
  const p = useReveal(10, 20);
  return (
    <SceneShell seed={scene.id} fadeOut={isLast} padded={false}>
      {media ? <MediaFrame file={media} fullBleed /> : null}
      <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(to top, rgba(5,8,16,0.85), rgba(5,8,16,0) 55%)'}} />
      <div style={{position: 'absolute', insetInlineStart: 120, bottom: 220, opacity: p, transform: `translateY(${(1 - p) * 30}px)`}}>
        <Kicker text={scene.label} color="rgba(255,255,255,0.8)" />
        {/* the scrim is always dark, so text here is always light regardless of theme */}
        <div style={{fontFamily: fonts.heading, fontSize: 84, fontWeight: 800, maxWidth: 1400, color: '#FFFFFF'}}>{scene.onScreenText}</div>
      </div>
    </SceneShell>
  );
};
