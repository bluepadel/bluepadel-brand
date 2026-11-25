"""Rebuild print-clean logo files for suppliers (FABI etc.).

The traced logo SVGs in assets/logos/print/vector-SVG carry 27 semi-transparent
fringe paths (anti-alias residue from tracing) and a full-artboard clip rectangle.
In CorelDRAW/Illustrator these import as a halo/border the printer cannot remove.

This drops faint fringe paths (opacity < 0.5), makes the rest solid, drops the hidden traced-text paths outside the clip, removes the clip wrapper and the empty
background rect, and writes SVG + PDF + EPS
into assets/logos/print/clean/. Solid fills only: no transparency, no images.

Then welds the traced pieces into one shape per colour (one-colour files: a single
shape, white highlights cut out as holes).

Run:  uv run --no-project --with cairosvg --with skia-pathops --with fonttools \\
          python scripts/clean_print_logos.py
"""

import re
from pathlib import Path

import cairosvg
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from pathops import Path as SkPath
from pathops import PathOp, op

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets/logos/print/vector-SVG"
OUT = ROOT / "assets/logos/print/clean"
KEEP_ABOVE = 0.5  # opacity at or above this is part of the figure, below is fringe


def _bbox_inside(d: str, t: tuple[float, float, float], clip: tuple[float, ...]) -> bool:
    if re.search(r"[a-df-z]", d):  # traced paths use absolute commands only
        raise ValueError("relative path command")
    tx, ty, sc = t
    cx, cy, cw, ch = clip
    n = [float(v) for v in re.findall(r"-?\d+\.?\d*", d)]
    xs = [tx + sc * v for v in n[0::2]]
    ys = [ty + sc * v for v in n[1::2]]
    return min(xs) >= cx - 0.5 and max(xs) <= cx + cw + 0.5 and min(ys) >= cy - 0.5 and max(ys) <= cy + ch + 0.5


def clean(svg: str) -> str:
    svg = svg.replace('<rect width="100%" height="100%" fill="none"/>', "")
    clip = tuple(map(float, re.search(
        r'<clipPath[^>]*><rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"', svg).groups()))
    grp = re.search(
        r'<g clip-path="[^"]*"><g transform="translate\(([-\d.]+),([-\d.]+)\) scale\(([\d.]+)\)">(.*?)</g></g>',
        svg, re.S)
    t = tuple(map(float, grp.groups()[:3]))
    # The trace holds the whole lockup; the clip shows only the figure. Keep the paths
    # inside the clip (none straddle it), drop the hidden traced text, then lose the clip.
    kept = "".join(p for p in re.findall(r"<path[^>]*/>", grp.group(4))
                   if _bbox_inside(re.search(r' d="([^"]+)"', p).group(1), t, clip))
    svg = svg[:grp.start()] + f'<g transform="translate({t[0]},{t[1]}) scale({t[2]})">{kept}</g>' + svg[grp.end():]
    svg = re.sub(r"<clipPath[^>]*>.*?</clipPath>", "", svg, flags=re.S)

    def fix(m: re.Match) -> str:
        path, alpha = m.group(0), float(m.group(1))
        if alpha < KEEP_ABOVE:
            return ""  # faint anti-alias fringe: drop
        return re.sub(r' (?:fill-)?opacity="[^"]*"', "", path)  # body: make solid

    return re.sub(r'<path[^>]*?(?:fill-)?opacity="([0-9.]+)"[^>]*/>', fix, svg)


def _sk(d: str, t: tuple[float, float, float]) -> SkPath:
    p = SkPath()
    parse_path(d, TransformPen(p.getPen(), (t[2], 0, 0, t[2], t[0], t[1])))
    return p


def weld(svg: str, one_colour: bool) -> str:
    """Replace the traced pieces with one welded, non-overlapping shape per colour.

    Paint order is honoured: each piece is clipped by everything painted after it, so
    no hidden geometry survives. In one-colour files the white highlight pieces become
    holes (the fabric shows through) instead of white ink.
    """
    g = re.search(r'<g transform="translate\(([-\d.]+),([-\d.]+)\) scale\(([\d.]+)\)">(.*?)</g>', svg, re.S)
    t = tuple(map(float, g.groups()[:3]))
    pieces = [(c.upper().replace("WHITE", "#FFFFFF"), _sk(d, t))
              for c, d in re.findall(r'<path fill="([^"]+)" d="([^"]+)"/>', g.group(4))]
    ink = None if not one_colour else next(c for c, _ in pieces if c != "#FFFFFF" or
                                          all(x == "#FFFFFF" for x, _ in pieces))
    layers: dict[str, SkPath] = {}
    for i, (colour, piece) in enumerate(pieces):
        later = SkPath()
        for _, q in pieces[i + 1:]:
            later = op(later, q, PathOp.UNION)
        visible = op(piece, later, PathOp.DIFFERENCE)
        if one_colour and colour != ink:
            continue  # highlight: leave it as a hole
        key = ink if one_colour else colour
        layers[key] = op(layers.get(key, SkPath()), visible, PathOp.UNION)
    out = []
    for colour, path in layers.items():
        path.simplify()
        pen = SVGPathPen(None)
        path.draw(pen)
        out.append(f'<path fill="{colour}" fill-rule="nonzero" d="{pen.getCommands()}"/>')
    return svg[:g.start()] + "".join(out) + svg[g.end():]


def main() -> None:
    for sub in ("SVG", "PDF", "EPS"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)
    for src in sorted(SRC.glob("*.svg")):
        svg = weld(clean(src.read_text()), one_colour="one-colour" in src.stem)
        assert "opacity" not in svg and "clip" not in svg and "<image" not in svg, src
        stem = src.stem
        (OUT / "SVG" / f"{stem}.svg").write_text(svg)
        data = svg.encode()
        cairosvg.svg2pdf(bytestring=data, write_to=str(OUT / "PDF" / f"{stem}.pdf"))
        cairosvg.svg2eps(bytestring=data, write_to=str(OUT / "EPS" / f"{stem}.eps"))
        print("ok", stem)


if __name__ == "__main__":
    main()
