# Recraft exploration 01 — BluePadel logo (from scratch)

First pass via the Recraft API (recraftv3, style `vector_illustration` → SVG),
brand palette fed in (primary #1565C0, navy #0D47A1, ink #0B1320) on white.
Ignores prior explorations by request. These are raw generations, not final marks.

- `c1_ball_arc` … `c6_pulse_score` — the six SVGs
- `contact_sheet.png` — overview
- `prompts.json` — the exact prompts + per-concept colour constraints
- `generate.py` — regenerate: `python generate.py <out_dir> prompts.json`
  (reads API key from ~/.recraft_key)
