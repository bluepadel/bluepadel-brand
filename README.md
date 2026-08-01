# @bluepadel/bluepadel-brand

Single source of truth for the **BluePadel** visual identity — design tokens,
a Tailwind preset, and logo assets. v0.1.0 is **tokens-only** (no React
components); component libraries consume these tokens.

## Token architecture (three layers)

1. **Primitives** — raw palette/type/spacing/radius/shadow (`src/tokens/*`,
   `--bp-blue-800`, …). The only place hex values live.
2. **Semantic** — intent aliases of the primitives (`--bp-color-surface`,
   `--bp-color-text-muted`, …) in `src/css/variables.css`. **Apps reference these.**
3. **Component** — per-component tokens, defined in each consuming app, that
   reference the semantic layer.

Theme = re-point the semantic aliases. Dark theme ships as `[data-theme="dark"]`
(architecture proven; light-only is the current shipped theme).

## Install

Published to the public npm registry — no auth required.

```bash
npm install @bluepadel/bluepadel-brand
```

## Use

```ts
// 1. tokens / Tailwind preset
import bluepadel from "@bluepadel/bluepadel-brand/tailwind.preset";
// tailwind.config.ts:  export default { presets: [bluepadel], content: [...] }
```

```ts
// 2. the CSS variables + reset (e.g. in main.tsx)
import "@bluepadel/bluepadel-brand/variables.css";
import "@bluepadel/bluepadel-brand/reset.css";
```

```ts
// 3. raw tokens in TS when needed
import { palette, semantic } from "@bluepadel/bluepadel-brand";
```

After importing, prefer themeable utilities: `bg-surface`, `text-muted`,
`border`, `bg-primary text-on-accent`, `text-danger-fg bg-danger-bg`, etc.

## Develop

```bash
npm install
npm run ci   # lint + typecheck + build (tsup → dist) + test
```

Publish is automated: push a `vX.Y.Z` tag (or run the `publish` workflow
manually) → builds + publishes to the public npm registry. Requires the
`NPM_TOKEN` repo secret (an npmjs **Automation** token for the `@bluepadel` org).
