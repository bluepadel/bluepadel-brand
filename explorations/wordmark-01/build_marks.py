#!/usr/bin/env python3
"""Hand-built BluePadel wordmark-led logo concepts: padel racket = tech scope,
ball locked in the reticle (trust the score). Precise SVG, brand font Inter."""
import subprocess, pathlib
from PIL import ImageFont

BLUE="#1565C0"; INK="#0B1320"; MUT="#6B7280"; SKY="#42A5F5"
OUT=pathlib.Path(__file__).parent; OUT.mkdir(exist_ok=True)
FONT="/home/wardsi/.fonts/Inter-700.ttf"
WM_SIZE=132
wmfont=ImageFont.truetype(FONT, WM_SIZE)
slfont=ImageFont.truetype("/home/wardsi/.fonts/Inter-500.ttf", 34)
def tw(s,f=wmfont): return f.getlength(s)

# ---- the racket-scope icon, drawn around centre (cx, cy), head radius R ----
def racket_scope(cx, cy, R, sw=13, players=False, accent=BLUE):
    p=[]
    # scope ticks (N,E,S,W) crossing the rim
    for dx,dy in [(0,-1),(0,1),(-1,0),(1,0)]:
        x1,y1=cx+dx*(R-6), cy+dy*(R-6); x2,y2=cx+dx*(R+18), cy+dy*(R+18)
        p.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{BLUE}" stroke-width="{sw}" stroke-linecap="round"/>')
    # racket rim / scope ring
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{BLUE}" stroke-width="{sw}"/>')
    # throat (two converging lines) + handle
    ht=cy+R+6; hb=cy+R+70
    p.append(f'<line x1="{cx-R*0.42:.1f}" y1="{cy+R*0.86:.1f}" x2="{cx-7}" y2="{ht+18}" stroke="{BLUE}" stroke-width="{sw}" stroke-linecap="round"/>')
    p.append(f'<line x1="{cx+R*0.42:.1f}" y1="{cy+R*0.86:.1f}" x2="{cx+7}" y2="{ht+18}" stroke="{BLUE}" stroke-width="{sw}" stroke-linecap="round"/>')
    p.append(f'<rect x="{cx-8}" y="{ht+16}" width="16" height="{hb-ht-16:.0f}" rx="7" fill="{BLUE}"/>')
    # centre ball locked in the reticle
    if players:
        p.append(f'<circle cx="{cx-R*0.42:.0f}" cy="{cy}" r="7" fill="{SKY}"/>')
        p.append(f'<circle cx="{cx+R*0.42:.0f}" cy="{cy}" r="7" fill="{SKY}"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{R*0.19:.1f}" fill="{accent}"/>')
    return "\n".join(p)

def lockup_svg(icon_svg, path, two_tone=True, slogan=True):
    ix=170                      # icon centre x
    tx=310                      # wordmark left
    baseline=250
    blue_w=tw("Blue")
    wm=(f'<text x="{tx}" y="{baseline}" font-family="Inter" font-weight="700" '
        f'font-size="{WM_SIZE}" fill="{BLUE}">Blue</text>'
        f'<text x="{tx+blue_w:.1f}" y="{baseline}" font-family="Inter" font-weight="700" '
        f'font-size="{WM_SIZE}" fill="{INK if two_tone else BLUE}">Padel</text>')
    sl=(f'<text x="{tx+3}" y="{baseline+56}" font-family="Inter" font-weight="500" '
        f'font-size="34" fill="{MUT}" letter-spacing="1.5">Trust the score.  Love the game.</text>') if slogan else ""
    total_w=tx+tw("Blue")+tw("Padel")+60
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w:.0f}" height="360" viewBox="0 0 {total_w:.0f} 360">'
         f'<rect width="100%" height="100%" fill="white"/>'
         f'<g transform="translate({ix-170},20)">{icon_svg}</g>{wm}{sl}</svg>')
    pathlib.Path(path).write_text(svg)
    subprocess.run(["cairosvg", path, "-o", path.replace(".svg","_v.png")], check=True)

# Concept A — racket-scope, clean
iconA=racket_scope(170,150,92)
lockup_svg(iconA, str(OUT/"A_scope.svg"))
# Concept A2 — with two player dots on the reticle line
iconA2=racket_scope(170,150,92, players=True)
lockup_svg(iconA2, str(OUT/"A2_players.svg"))
# Concept C — accent ball (lighter blue centre) for a subtle two-tone
iconC=racket_scope(170,150,92, accent=SKY)
lockup_svg(iconC, str(OUT/"C_accent.svg"))
print("built A, A2, C")
