import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {scenes} from './data/scenes';
import {Captions} from './components/Captions';
import {
  CompareScene,
  ConceptScene,
  HookScene,
  MediaScene,
  RecapScene,
  StatScene,
  StepsScene,
  type SceneProps,
} from './scenes/scenes';
import {colors} from './styles/tokens';
import {LANG} from './data/language';
import {OVERLAP} from './utils/motion';

// kind -> scene template. Register bespoke scenes by id in `custom` to override a template.
const byKind: Record<string, React.FC<SceneProps>> = {
  hook: HookScene,
  question: HookScene,
  stat: StatScene,
  steps: StepsScene,
  compare: CompareScene,
  recap: RecapScene,
  media: MediaScene,
  definition: ConceptScene,
  quote: ConceptScene,
  concept: ConceptScene,
};
const custom: Record<string, React.FC<SceneProps>> = {};

// Set to e.g. 'audio/narration/main.mp3' once the narration file exists in public/.
const NARRATION: string | null = null;

export const Main: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: colors.bg}} dir={LANG.rtl ? 'rtl' : 'ltr'} lang={LANG.code}>
    {scenes.map((s, i) => {
      const Comp = custom[s.id] ?? byKind[s.kind] ?? ConceptScene;
      const isLast = i === scenes.length - 1;
      // Non-final scenes run OVERLAP frames longer so the next one fades in over them.
      return (
        <Sequence key={s.id} from={s.startFrame} durationInFrames={s.durationFrames + (isLast ? 0 : OVERLAP)} name={s.id}>
          <Comp scene={s} isLast={isLast} />
        </Sequence>
      );
    })}
    <Captions />
    {NARRATION ? <Audio src={staticFile(NARRATION)} /> : null}
  </AbsoluteFill>
);
