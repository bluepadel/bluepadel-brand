import type { Config } from "tailwindcss";

import { radius } from "./tokens/radius";
import { shadow } from "./tokens/shadow";
import { spacing } from "./tokens/spacing";
import { typography } from "./tokens/typography";

/**
 * BluePadel Tailwind preset. Consumers extend it with one line:
 *
 *   import bluepadel from "@bluepadel/bluepadel-brand/tailwind.preset";
 *   export default { presets: [bluepadel], content: [...] } satisfies Config;
 *
 * Colour utilities are bound to the SEMANTIC CSS variables (var(--bp-color-*)),
 * so `bg-surface` / `text-muted` / `border-default` follow the active theme with
 * zero per-component changes. The raw `bp-blue-*` / `bp-neutral-*` ramps are
 * exposed too for the rare case a primitive is genuinely needed.
 */
const sem = (name: string) => `var(--bp-color-${name})`;

const bluepadelPreset = {
  theme: {
    extend: {
      colors: {
        // Semantic, themeable (preferred).
        bg: sem("bg"),
        surface: sem("surface"),
        "surface-raised": sem("surface-raised"),
        "surface-sunken": sem("surface-sunken"),
        overlay: sem("overlay"),
        text: { DEFAULT: sem("text"), muted: sem("text-muted"), subtle: sem("text-subtle"), inverse: sem("text-inverse"), "on-accent": sem("text-on-accent") },
        border: { DEFAULT: sem("border"), strong: sem("border-strong") },
        ring: sem("focus-ring"),
        primary: { DEFAULT: sem("primary"), hover: sem("primary-hover"), active: sem("primary-active"), subtle: sem("primary-subtle") },
        accent: sem("accent"),
        success: { DEFAULT: sem("success"), bg: sem("success-bg"), fg: sem("success-fg") },
        warning: { DEFAULT: sem("warning"), bg: sem("warning-bg"), fg: sem("warning-fg") },
        danger: { DEFAULT: sem("danger"), bg: sem("danger-bg"), fg: sem("danger-fg") },
        info: { DEFAULT: sem("info"), bg: sem("info-bg"), fg: sem("info-fg") },
        // Raw primitive ramps (escape hatch).
        "bp-blue": {
          50: "var(--bp-blue-50)", 100: "var(--bp-blue-100)", 200: "var(--bp-blue-200)",
          300: "var(--bp-blue-300)", 400: "var(--bp-blue-400)", 500: "var(--bp-blue-500)",
          600: "var(--bp-blue-600)", 700: "var(--bp-blue-700)", 800: "var(--bp-blue-800)",
          900: "var(--bp-blue-900)",
        },
        "bp-neutral": {
          0: "var(--bp-neutral-0)", 50: "var(--bp-neutral-50)", 100: "var(--bp-neutral-100)",
          200: "var(--bp-neutral-200)", 300: "var(--bp-neutral-300)", 400: "var(--bp-neutral-400)",
          500: "var(--bp-neutral-500)", 600: "var(--bp-neutral-600)", 700: "var(--bp-neutral-700)",
          800: "var(--bp-neutral-800)", 900: "var(--bp-neutral-900)",
        },
      },
      fontFamily: {
        sans: ["var(--bp-font-base)"],
        display: ["var(--bp-font-display)"],
        mono: ["var(--bp-font-mono)"],
      },
      fontSize: typography.fontSize as unknown as Record<string, [string, { lineHeight: string }]>,
      spacing,
      borderRadius: radius,
      boxShadow: {
        sm: "var(--bp-shadow-sm)",
        DEFAULT: "var(--bp-shadow-md)",
        md: "var(--bp-shadow-md)",
        lg: "var(--bp-shadow-lg)",
        xl: "var(--bp-shadow-xl)",
        none: shadow.none,
      },
    },
  },
} satisfies Partial<Config>;

export default bluepadelPreset;
