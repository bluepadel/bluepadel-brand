/**
 * SEMANTIC tokens — intent-named aliases of the primitives. Consumers should
 * reference THESE, never raw palette values, so themes (light/dark/high-contrast)
 * resolve by swapping the alias targets. The runtime values live in
 * `css/variables.css` (CSS custom properties); this map mirrors the names for
 * TypeScript consumers that need to reference a token programmatically.
 */
export const semantic = {
  color: {
    // Surfaces
    bg: "var(--bp-color-bg)",
    surface: "var(--bp-color-surface)",
    surfaceRaised: "var(--bp-color-surface-raised)",
    surfaceSunken: "var(--bp-color-surface-sunken)",
    overlay: "var(--bp-color-overlay)",
    // Text
    text: "var(--bp-color-text)",
    textMuted: "var(--bp-color-text-muted)",
    textSubtle: "var(--bp-color-text-subtle)",
    textInverse: "var(--bp-color-text-inverse)",
    textOnAccent: "var(--bp-color-text-on-accent)",
    // Borders
    border: "var(--bp-color-border)",
    borderStrong: "var(--bp-color-border-strong)",
    focusRing: "var(--bp-color-focus-ring)",
    // Brand / primary action
    primary: "var(--bp-color-primary)",
    primaryHover: "var(--bp-color-primary-hover)",
    primaryActive: "var(--bp-color-primary-active)",
    primarySubtle: "var(--bp-color-primary-subtle)",
    accent: "var(--bp-color-accent)",
    // Feedback (each: base / subtle bg / strong fg)
    success: "var(--bp-color-success)",
    successBg: "var(--bp-color-success-bg)",
    successFg: "var(--bp-color-success-fg)",
    warning: "var(--bp-color-warning)",
    warningBg: "var(--bp-color-warning-bg)",
    warningFg: "var(--bp-color-warning-fg)",
    danger: "var(--bp-color-danger)",
    dangerBg: "var(--bp-color-danger-bg)",
    dangerFg: "var(--bp-color-danger-fg)",
    info: "var(--bp-color-info)",
    infoBg: "var(--bp-color-info-bg)",
    infoFg: "var(--bp-color-info-fg)",
  },
} as const;

export type Semantic = typeof semantic;
