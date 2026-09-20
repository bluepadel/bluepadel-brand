# BluePadel logo/brand exploration — RESUME HERE (as at 2026-09-04)

State saved so a fresh Claude session can pick up exactly where we left off.

## The ask
A senior marketing exec called the current logo "clip-art / looks like a startup". Brief:
the brand must feel **creative + new** yet **stable, confident, mature, and above all
technically strong**. The exec **loved the slogan** — which is, and stays, verbatim:

> **Trust the score. Love the game.**  *(never change/paraphrase — see memory `bluepadel-slogan`)*

Current mark being replaced: `assets/logos/bluepadel-mark.svg` — a flat white padel racket on a
solid blue app tile.

## Where we landed (the live direction)
- **Round 1** (5 directions: racket / perf-P / trajectory / eye / wordmark) → **hard no on all**.
  Also used the WRONG slogan there. Kept for history: `bluepadel-mark-study.html`.
- **Territory chosen by Simon (AskUserQuestion): "Sports-tech performance"** — Hawk-Eye /
  TrackMan / WHOOP: precise, proven, athletic, dynamic-but-disciplined.
- **Round 2 "Tracked":** ball tracked in flight → the scored point. Simon: **likes the tracking
  idea AND the "BluePadel" Archivo wordmark/font.**
- **Round 3 "Pulse":** heart-rate / ECG line set to the height of the BluePadel wording, sitting
  just *left* of it. Simon's reaction: the ECG shouldn't be a separate glyph beside the name — make
  it **smaller and run through / over the actual "BluePadel" letters**, merged with the tracker idea.
- **Round 4 "Pulse through the wordmark" (CURRENT):** the mark is now an overlay drawn *on* the
  wordmark — an ECG/tracker baseline at the **foot of the letters** (with faint sampling ticks), that
  **spikes up through the letters and over the caps** to the ball-yellow point. No longer a bolt-on
  glyph; it's woven into the name. Three dials presented to react to:
  **A — Through & over** (loud; the hero), **B — Tracked arc** (a lobbed trajectory over the name,
  more ball-tracker), **C — Quiet beat** (small beat rising into the x-height, never over the caps).
  → File: **`bluepadel-pulse.html`** (this folder). Mark rendered by JS `through()/arc()/quiet()`
  + `icon()`; hosts carry `data-mark='{style,line,peak,ticks,sw}'`.
  → **Fonts are now embedded as base64 woff2** (Archivo/Inter/JetBrains Mono) via the `#fonts`
  `<style>` block — the Artifact CSP blocks font CDNs, so the old Google Fonts `<link>` was silently
  falling back. Rebuild with `build_fonts.mjs` in this session's scratchpad if weights change.
  → Published artifact (private): **https://claude.ai/code/artifact/96b40e7f-7dde-4091-b435-50490e67c207**
    (favicon 💓, keep stable).
- **Round 5 — horizontal lockup, letter-integrated (CURRENT, 2026-09-04):** Simon directed a specific
  treatment *on the horizontal lockup*: **start the ECG with a ball** (yellow, bottom-left), **drop the
  line a few px below the wording**, **use the two "l"s as the ECG spikes**, and put an **ECG murmur
  between the P and the a**. Built as a measured overlay (`drawLockup()`): it reads the real glyph
  boxes, the two **"l"s are recoloured blue** and the trace **sits *behind* the text** (`.wm-ov-back`,
  host is a stacking context) rising to the *foot* of each l so the blue letter *is* the spike — no
  doubling. Shown large in the "◆ Horizontal lockup" showcase section; also used in the system-row
  lockup + mono cells. (Hero + the A/B/C dial cards above still show Round-4 "through & over" — NOT yet
  propagated to this new treatment; do that once Simon locks it.)
- **App icon — Simon flagged the old ECG-in-a-tile "looks like a medical app."** New "◆ App icon"
  section offers three directions off the medical look (JS `ICONS{}`): **A ball + motion trail**,
  **B "BP" monogram + serve-dot** (⚠ flagged: "BP" can read as *blood pressure*), **C the padel ball**
  (seam + spin). Old medical icon kept in system row labelled "current ⚠".
- **Round 6 — "The B carries the ball" (CURRENT lead, 2026-09-04):** Simon liked an **OpenArt**-generated
  logo (a dynamic blue **B monogram with a padel ball in the lower bowl**) — screenshot saved at
  `~/projects/screenshots/branding-ideas/01.png`. He wants that **logo moved *into* the wordmark,
  replacing the "B" in "BluePadel"**, and the **B lifted out as the app icon / social avatar**. Built:
  the ball is seated into the lower bowl of the **real Archivo "B"** (kept on-brand-font, not a literal
  trace of the AI art) via `drawBMark()` measured overlay; the standalone icon is `iconB()` (white B +
  ball on the gradient tile). Shown in the "◆ The B carries the ball" section (wordmark + icon tile).
  B is `--sky`, "lue" muted, "Padel" bold — the wordmark treatment preserved. Ball sits ~centred in the
  counter (tuned). **This is now the front-runner over the pulse/ECG rounds.**
  ⚠ Simon also said he **likes the "sportifying"** of the OpenArt comp (the dark hero + phone-with-
  bounding-boxes marketing composition) — **PARKED, "for later"**: revisit as a marketing/landing
  treatment once the mark is locked. Do NOT act on it yet.
- **Open next (Round 6):** tune the B/ball (more dynamic/italic à la OpenArt? ball size/position?), and — if Simon
  confirms — propagate the ball-in-B across the hero, scoreboard and seal (they still show Round-4 ECG).
- **Round 7 — "Wordmark-led, minimal, mature" (CURRENT, 2026-09-06):** Simon was **unhappy with all the
  earlier logo recommendations** and asked for a fresh, tool-led attempt at a genuinely mature mark.
  Decisions via AskUserQuestion: **Direction = "Fresh, reference-led"** (NOT the pulse/ECG or B-ball
  rounds), **Feel = "Wordmark-led, minimal"** (the name is the logo; the mark is one small precise
  detail). Calibrated to Hawk-Eye / TrackMan / Genius Sports / WHOOP / Stripe / Linear. Four cuts to
  react to, all monochrome-first with a single ball-yellow spark:
  **A — Unified** (one weight, "Blue" muted + "Padel" solid, a single ball-yellow point closing the word;
  Stripe/Linear register — strongest/most mature), **B — Apex** (a disciplined hairline trajectory arc
  as a diacritic over the word, yellow apex dot), **C — Counter-point** (the ball seated in the bowl of
  the "P"; weakest concept — fights the letterform), **D — Instrument** (wordmark + a JetBrains-Mono
  "Auto Scoring" tag off a ball-yellow rule; reads like lab/TrackMan equipment — strong).
  → File: **`bluepadel-wordmark.html`** (this folder; `<title>` + reused `#fonts` block + `content.html`).
  → Published artifact (private): **https://claude.ai/code/artifact/8665b48a-e87b-4d50-973f-9d9ed77a939c**
    (favicon 🎾, keep stable).
  → **Awaiting Simon's reaction:** which cut (A–D), or which details to combine. Then refine the winner
    across sizes + light/dark + app icon, and write the identity-designer brief.
- **⚡ NEW TOOLING (2026-09-06) — the sighted design loop.** Author SVG/HTML → screenshot headless →
  *look at it* → critique → refine. This caught a real dark-on-dark render bug in v1 (a truncated
  `#fonts` partial swallowed the `:root` vars). Playwright JS pkg installed under the session scratchpad
  `pw/` (`npm i playwright`; browsers already cached at `~/.cache/ms-playwright/chromium-1234`). Launch
  Playwright with `executablePath` pointing at that cached chrome (the pinned pkg wants a newer build).
  Helper `pw/shot.mjs <html> <out.png> [w] [h] [scale] [selector]` waits for `document.fonts.ready`
  before capture (essential for wordmark work — else you screenshot a fallback font) and can clip a
  single selector. To assemble a local full-doc for screenshotting: `<!doctype html>` + `fonts.html`
  (the extracted `#fonts` block — extract the WHOLE block, it spans >1 line: `awk '/<style id="fonts">/{f=1} f{print} /<\/style>/{if(f)exit}'`) + `content.html`.
  There is **no AI image generator** available — hand-authored vector + this loop is the path.

## Design constants (do not drift)
- Wordmark: **Archivo** (Blue = 600 weight muted, Padel = 900). Keep it — Simon likes it.
- Palette: Navy #0A2A72 · Blue #1565C0 · Sky #2196F3 · **Ball-yellow #FFC21F** (the spark/accent).
- Type system in decks: Archivo (display/wordmark), Inter (UI), JetBrains Mono (scores/data).

## Open dials Simon may pick next (last message offered these)
1. **Which cut** — A (through & over), B (tracked arc), or C (quiet beat). Then tune within it:
   spike position (currently over the "Pa"), colour (line white/blue + peak ball-yellow; could go
   whole-line yellow), tick density, whether the ball sits over the caps or lower.
2. If Simon says "this is the one" → **write an identity-designer brief** (positioning, must/mustn't,
   locked slogan + palette, the pulse concept, clear-space/min-size/motion spec, on-court artwork)
   and hand off to a real designer for final vector artwork. That was the agreed end-state — these
   are directions to react to, NOT final artwork.

## How to resume editing
- Edit `bluepadel-pulse.html` here, then **re-publish to the SAME artifact URL** by passing
  `url: https://claude.ai/code/artifact/96b40e7f-7dde-4091-b435-50490e67c207` to the Artifact tool
  (read it first per the update flow). Do NOT publish without the url or you'll fork a new artifact.
- To screenshot-verify: headless chromium is at
  `~/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome`; playwright is resolvable from a
  scratch dir where `npm i playwright` was run. `_screenshot.mjs` is a template — update its OUT
  path (it points at the old session scratchpad) before running.

## The pulse mark (so it can be rebuilt from scratch if needed)
An ECG polyline laid across the svg viewBox width at vertical centre: flat lead-in → small P bump →
QRS spike (down, tall up = the R peak, down) → T bump → flat out. The R-peak carries a ball-yellow
filled dot (the point that counts). See the `pulse()` JS function in `bluepadel-pulse.html`.
