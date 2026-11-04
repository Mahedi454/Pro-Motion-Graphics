// Placeholder. Regenerate from storyboard.csv with scripts/storyboard_to_scenes.py
export type SceneData = {
  id: string; title: string; label: string; visual: string; narration: string; onScreenText: string;
  kind: string; assets: string[]; startFrame: number; durationFrames: number;
};
export const FPS = 30;
export const TOTAL_FRAMES = 300;
export const scenes: SceneData[] = [
  {id: 'S01', title: 'Hook', label: '', visual: '', narration: 'What really happens inside a black hole?', onScreenText: 'What really happens inside?', kind: 'hook', assets: [], startFrame: 0, durationFrames: 150},
  {id: 'S02', title: 'Concept', label: '', visual: '', narration: 'Gravity bends space itself.', onScreenText: 'Gravity bends space', kind: 'concept', assets: [], startFrame: 150, durationFrames: 150},
];
