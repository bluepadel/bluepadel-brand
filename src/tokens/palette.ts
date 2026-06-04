/**
 * PRIMITIVE colour tokens — the raw BluePadel palette.
 *
 * These are the only place hex values live. Nothing in a consuming app should
 * reference a hex directly; reference the SEMANTIC tokens (see `semantic.ts` /
 * `css/variables.css`), which alias these primitives. Sourced from the approved
 * brand spec (docs/06-cloud/padel_scoring_brand_b3_package.md), primary `#1565C0`.
 */
export const palette = {
  blue: {
    50: "#E3F2FD",
    100: "#BBDEFB",
    200: "#90CAF9",
    300: "#64B5F6",
    400: "#42A5F5",
    500: "#2196F3",
    600: "#1E88E5",
    700: "#1976D2", // primary action / hover
    800: "#1565C0", // brand primary
    900: "#0D47A1", // primary active / pressed
  },
  neutral: {
    0: "#FFFFFF",
    50: "#FAFBFC",
    100: "#F1F3F5",
    200: "#E1E5EA",
    300: "#C7CDD3",
    400: "#9DA5AD",
    500: "#6B7280", // muted text
    600: "#4B5563",
    700: "#374151",
    800: "#1F2937", // body text
    900: "#0B1320", // dark app background
  },
  // Feedback primitives — each with a tint (bg) + base + strong/fg step.
  green: { 50: "#ECFDF3", 100: "#D1FADF", 500: "#16A34A", 700: "#15803D" },
  amber: { 50: "#FFFBEB", 100: "#FEF0C7", 500: "#F59E0B", 700: "#B45309" },
  red: { 50: "#FEF3F2", 100: "#FEE4E2", 500: "#DC2626", 700: "#B42318" },
  sky: { 50: "#F0F9FF", 100: "#E0F2FE", 500: "#0284C7", 700: "#0369A1" },
} as const;

export type Palette = typeof palette;
