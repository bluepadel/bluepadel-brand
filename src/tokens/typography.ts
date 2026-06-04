/**
 * PRIMITIVE typography tokens. `display-*` steps are oversized for the
 * courtside scoreboard (10m visibility); the rest are the standard web ramp.
 */
export const typography = {
  fontFamily: {
    base: ['"Inter"', '"Helvetica Neue"', "Arial", "sans-serif"],
    display: ['"Inter"', '"Helvetica Neue"', "Arial", "sans-serif"],
    mono: ['"JetBrains Mono"', '"Consolas"', "monospace"],
  },
  fontWeight: {
    regular: "400",
    medium: "500",
    semibold: "600",
    bold: "700",
  },
  fontSize: {
    xs: ["0.75rem", { lineHeight: "1rem" }],
    sm: ["0.875rem", { lineHeight: "1.25rem" }],
    base: ["1rem", { lineHeight: "1.5rem" }],
    lg: ["1.125rem", { lineHeight: "1.75rem" }],
    xl: ["1.25rem", { lineHeight: "1.75rem" }],
    "2xl": ["1.5rem", { lineHeight: "2rem" }],
    "3xl": ["1.875rem", { lineHeight: "2.25rem" }],
    "4xl": ["2.25rem", { lineHeight: "2.5rem" }],
    "5xl": ["3rem", { lineHeight: "1" }],
    // Courtside scoreboard display steps.
    "display-md": ["4rem", { lineHeight: "1" }],
    "display-lg": ["6rem", { lineHeight: "1" }],
    "display-xl": ["8rem", { lineHeight: "1" }],
  },
} as const;

export type Typography = typeof typography;
