import {loadFont as inter} from '@remotion/google-fonts/Inter';
import {loadFont as arabic} from '@remotion/google-fonts/NotoSansArabic';
import {loadFont as armenian} from '@remotion/google-fonts/NotoSansArmenian';
import {loadFont as bengali} from '@remotion/google-fonts/NotoSansBengali';
import {loadFont as devanagari} from '@remotion/google-fonts/NotoSansDevanagari';
import {loadFont as ethiopic} from '@remotion/google-fonts/NotoSansEthiopic';
import {loadFont as georgian} from '@remotion/google-fonts/NotoSansGeorgian';
import {loadFont as gujarati} from '@remotion/google-fonts/NotoSansGujarati';
import {loadFont as gurmukhi} from '@remotion/google-fonts/NotoSansGurmukhi';
import {loadFont as hebrew} from '@remotion/google-fonts/NotoSansHebrew';
import {loadFont as japanese} from '@remotion/google-fonts/NotoSansJP';
import {loadFont as kannada} from '@remotion/google-fonts/NotoSansKannada';
import {loadFont as khmer} from '@remotion/google-fonts/NotoSansKhmer';
import {loadFont as korean} from '@remotion/google-fonts/NotoSansKR';
import {loadFont as lao} from '@remotion/google-fonts/NotoSansLao';
import {loadFont as malayalam} from '@remotion/google-fonts/NotoSansMalayalam';
import {loadFont as myanmar} from '@remotion/google-fonts/NotoSansMyanmar';
import {loadFont as oriya} from '@remotion/google-fonts/NotoSansOriya';
import {loadFont as chineseSimplified} from '@remotion/google-fonts/NotoSansSC';
import {loadFont as sinhala} from '@remotion/google-fonts/NotoSansSinhala';
import {loadFont as tamil} from '@remotion/google-fonts/NotoSansTamil';
import {loadFont as chineseTraditional} from '@remotion/google-fonts/NotoSansTC';
import {loadFont as telugu} from '@remotion/google-fonts/NotoSansTelugu';
import {loadFont as thai} from '@remotion/google-fonts/NotoSansThai';
import {LANG} from '../data/language';

/**
 * Loads the right font for the video's writing system (from the SRT). Fonts come from Google Fonts
 * through @remotion/google-fonts, so the FIRST render needs an internet connection.
 * Offline? Put a font file in public/fonts/ and use @font-face instead (see README-RENDER.md).
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Loader = (style?: any, options?: any) => {fontFamily: string};
const loaders: Record<string, Loader> = {
  latin: inter, cyrillic: inter, greek: inter,
  arabic, armenian, bengali, devanagari, ethiopic, georgian, gujarati, gurmukhi, hebrew,
  kana: japanese, hangul: korean, han: LANG.code === 'zh-TW' || LANG.code === 'zh-HK' ? chineseTraditional : chineseSimplified,
  kannada, khmer, lao, malayalam, myanmar, oriya, sinhala, tamil, telugu, thai,
};

const WEIGHTS = ['400', '600', '700', '800'];
const load = (loader: Loader) => {
  try {
    return loader('normal', {weights: WEIGHTS}).fontFamily;
  } catch {
    return loader('normal').fontFamily; // font lacks one of the weights: take its defaults
  }
};

const latin = load(inter);
const primary = LANG.script in loaders && loaders[LANG.script] !== inter ? load(loaders[LANG.script]) : latin;

// Primary script font first, Inter for any Latin words mixed in, then system fallbacks.
export const fontStack = `"${primary}", "${latin}", system-ui, sans-serif`;
