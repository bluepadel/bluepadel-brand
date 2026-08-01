// Generate the Android Compose token file from the brand tokens — so the Kotlin
// app shares ONE source of truth with web instead of hand-mirroring colours.
//
// Usage:  npm run gen:android        (runs `npm run build` first, then this)
//
// Reads the built tokens (palette + light/dark themes) and writes
// clients/BluePadel WearOS/mobile/.../ui/theme/BluePadelTokens.kt.

import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { dark, light, palette } from "../dist/index.js";

// Output path. The WearOS repo is the Windows P: copy that Android Studio opens
// (reached from WSL via /mnt/p); the brand repo lives separately in ~/. Override
// with BP_ANDROID_TOKENS_OUT for any other layout.
const DEFAULT_OUT =
  "/mnt/p/Claude/Projects/Internal/Padel/clients/BluePadel WearOS" +
  "/mobile/src/main/kotlin/za/co/bluepadel/ui/theme/BluePadelTokens.kt";
const OUT = process.env.BP_ANDROID_TOKENS_OUT || DEFAULT_OUT;

// Field order of the BpColors data class — must match themes.ts semantic keys.
const ORDER = [
  "bg", "surface", "surfaceRaised", "surfaceSunken", "overlay",
  "text", "textMuted", "textSubtle", "textInverse", "textOnAccent",
  "border", "borderStrong", "focusRing",
  "primary", "primaryHover", "primaryActive", "primarySubtle", "accent",
  "success", "successBg", "successFg",
  "warning", "warningBg", "warningFg",
  "danger", "dangerBg", "dangerFg",
  "info", "infoBg", "infoFg",
];

const hex2 = (n) => n.toString(16).toUpperCase().padStart(2, "0");

/** "#RRGGBB" → Color(0xFFRRGGBB); "rgba(r,g,b,a)" → Color(0xAARRGGBB). */
function colorLiteral(value) {
  if (value.startsWith("#")) {
    return `Color(0xFF${value.slice(1).toUpperCase()})`;
  }
  const m = value.match(/rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+)\s*)?\)/);
  if (!m) throw new Error(`Unrecognised colour: ${value}`);
  const [r, g, b] = [m[1], m[2], m[3]].map(Number);
  const a = m[4] === undefined ? 1 : Number(m[4]);
  return `Color(0x${hex2(Math.round(a * 255))}${hex2(r)}${hex2(g)}${hex2(b)})`;
}

function primitivesBlock() {
  const lines = [];
  for (const [group, scale] of Object.entries(palette)) {
    const cap = group.charAt(0).toUpperCase() + group.slice(1);
    for (const [step, value] of Object.entries(scale)) {
      lines.push(`    val ${cap}${step} = ${colorLiteral(value)}`);
    }
  }
  return lines.join("\n");
}

function colorsBlock(name, theme, isDark) {
  const fields = ORDER.map((k) => `    ${k} = ${colorLiteral(theme[k])},`).join("\n");
  return `val ${name} = BpColors(\n${fields}\n    isDark = ${isDark},\n)`;
}

const dataClass = `data class BpColors(\n${ORDER.map((k) => `    val ${k}: Color,`).join("\n")}\n    val isDark: Boolean,\n)`;

const file = `package za.co.bluepadel.ui.theme

import androidx.compose.ui.graphics.Color

// GENERATED from @bluepadel/bluepadel-brand (palette.ts + themes.ts).
// Do NOT edit by hand — run \`npm run gen:android\` in bluepadel-brand/.
// Single source of truth for BluePadel colours across web + Android (primary #1565C0).

/** Primitive palette — raw brand scale. UI code references the semantic
 *  [BpColors] sets (so dark mode resolves by swapping the set), not these. */
object Bp {
${primitivesBlock()}
}

/** Semantic colour set for one theme — intent-named aliases of [Bp]. */
${dataClass}

${colorsBlock("BluePadelLightColors", light, false)}

${colorsBlock("BluePadelDarkColors", dark, true)}
`;

mkdirSync(dirname(OUT), { recursive: true });
writeFileSync(OUT, file, "utf8");
console.log(`Wrote ${OUT}`);
