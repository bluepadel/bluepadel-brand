# Hero AI overlay — ready to drop onto real footage

When a real professional padel-court photo/footage arrives:
1. Put it in `padel-marketing/src/assets/hero-court.jpg`.
2. Re-use the overlay: a `<svg class="hero-ai">` with the **neural-network mesh**
   (cyan nodes on court reference points + edges) + the **200 km/h smash track**
   (dots → BOUNCE ring → ball bounding-box) + the `SMASH · 200 km/h` tag.
   Node/trajectory coordinates are tuned per image (viewBox 0..100, % of the image).
3. Keep the `.score-card` (6-4 / 4-3 LIVE) and `.latency-badge` (< 1s) HTML overlays.

`court_premium_renderer.py` — the geometrically-exact fallback court, drawn from
`padel_court/dimensions.py` (correct lines/net). Premium "digital-twin" styling.
Use only if we never get real footage.

Verdict (2026-09-09): geometry render is *correct* but not the professional look
Simon wants; waiting for a real stock/real-world image, then this overlay drops on.
