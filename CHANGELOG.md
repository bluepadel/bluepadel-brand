# Changelog

## 0.1.0 — unreleased

First release. Tokens-only (no React components).

- Three-layer design tokens: primitives → semantic → (consumer) component.
- Palette (Material-blue family, brand primary `#1565C0`), neutral ramp,
  feedback colours; typography scale incl. courtside display steps; spacing,
  radius, shadow scales.
- CSS custom properties (`variables.css`) with light theme + dark-ready theme
  (`[data-theme="dark"]`); minimal `reset.css`.
- Tailwind v3 preset binding utilities to the semantic CSS variables.
- Logo / paddle-mark assets (SVG + PNG 64–1024).
