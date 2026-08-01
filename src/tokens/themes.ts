/**
 * THEME tokens — the semantic layer RESOLVED to concrete hex values, per theme.
 *
 * `css/variables.css` is the runtime source for web (CSS custom properties);
 * this module is the same light/dark resolution as a typed object, so NON-CSS
 * consumers (Android/Compose, iOS, watch) can be generated from one source
 * instead of hand-mirroring colours (which is how the Android app drifted to an
 * off-brand `#1E40AF`). Keep this in lockstep with `css/variables.css`
 * (`test/tokens.test.ts` asserts the key invariants against `palette`).
 *
 * Each theme maps the semantic names in `semantic.ts` to a resolved hex (or
 * rgba for overlays). Generators (e.g. `scripts/generate-android.mjs`) iterate
 * these to emit platform token files.
 */
import { palette } from "./palette";

const p = palette;

export const light = {
  bg: p.neutral[50],
  surface: p.neutral[0],
  surfaceRaised: p.neutral[0],
  surfaceSunken: p.neutral[100],
  overlay: "rgba(11, 19, 32, 0.45)",

  text: p.neutral[800],
  textMuted: p.neutral[500],
  textSubtle: p.neutral[400],
  textInverse: p.neutral[0],
  textOnAccent: p.neutral[0],

  border: p.neutral[200],
  borderStrong: p.neutral[300],
  focusRing: p.blue[400],

  primary: p.blue[800],
  primaryHover: p.blue[700],
  primaryActive: p.blue[900],
  primarySubtle: p.blue[50],
  accent: p.blue[500],

  success: p.green[500],
  successBg: p.green[50],
  successFg: p.green[700],
  warning: p.amber[500],
  warningBg: p.amber[50],
  warningFg: p.amber[700],
  danger: p.red[500],
  dangerBg: p.red[50],
  dangerFg: p.red[700],
  info: p.sky[500],
  infoBg: p.sky[50],
  infoFg: p.sky[700],
} as const;

export const dark = {
  bg: p.neutral[900],
  surface: "#111C2E",
  surfaceRaised: "#1B2840",
  surfaceSunken: "#0A1019",
  overlay: "rgba(0, 0, 0, 0.6)",

  text: "#E7ECF3",
  textMuted: p.neutral[400],
  textSubtle: p.neutral[500],
  textInverse: p.neutral[900],
  textOnAccent: p.neutral[0],

  border: "#2A3953",
  borderStrong: "#3A4D6E",
  focusRing: p.blue[400],

  primary: p.blue[400],
  primaryHover: p.blue[300],
  primaryActive: p.blue[500],
  primarySubtle: "#16263F",
  accent: p.blue[300],

  // Dark re-points only the feedback bg/fg; the base stays the primitive 500.
  success: p.green[500],
  successBg: "#0F2A1C",
  successFg: "#6EE7A8",
  warning: p.amber[500],
  warningBg: "#2A210A",
  warningFg: "#FBD38D",
  danger: p.red[500],
  dangerBg: "#2A1414",
  dangerFg: "#FCA5A5",
  info: p.sky[500],
  infoBg: "#0A2233",
  infoFg: "#7DD3FC",
} as const;

export const themes = { light, dark } as const;

export type ThemeColors = typeof light;
export type Themes = typeof themes;
