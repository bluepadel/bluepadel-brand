#!/usr/bin/env python3
"""Put the official BluePadel mark on the Recraft v2 images (shop redesign, padel-cloud #1431).

Erases the generator's stray fake marks (OpenCV inpaint), recolours black trim to deep blue (no
black on BP apparel) and pastes the official mark (white on blue kit, brand blue on white kit;
from assets/logos/bluepadel-appicon.svg) plus a reversed-wordmark court banner. Output: final/.

uv run --with opencv-python-headless --with pillow python compose.py
"""
import pathlib
import cv2
import numpy as np
from PIL import Image, ImageFilter

SRC, OUT = pathlib.Path("out-v2"), pathlib.Path("final")
OUT.mkdir(exist_ok=True)
NAVY = np.array([13, 71, 161], dtype=np.float32)


def load_logo(name):
    im = Image.open(f"logos/{name}.png").convert("RGBA")
    return im.crop(im.getbbox())


MARK = {"white": load_logo("mark-white"), "blue": load_logo("mark-blue")}
WORD = load_logo("wordmark-reversed")


def inpaint(img, boxes):
    a = np.array(img)
    mask = np.zeros(a.shape[:2], np.uint8)
    for x0, y0, x1, y1 in boxes:
        mask[y0:y1, x0:x1] = 255
    return Image.fromarray(cv2.inpaint(a, mask, 7, cv2.INPAINT_TELEA))


def denavy(img, box, thresh=80, lo=0.55, span=0.6):
    a = np.array(img).astype(np.float32)
    x0, y0, x1, y1 = box
    r = a[y0:y1, x0:x1]
    lum = r.max(axis=2)
    dark = lum < thresh
    t = (lum / thresh)[..., None]
    r[dark] = (NAVY * (lo + span * t))[dark]
    a[y0:y1, x0:x1] = r
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def paste_mark(img, colour, cx, cy, h, opacity=0.95, rotate=0):
    m = MARK[colour]
    m = m.resize((round(m.width * h / m.height), h), Image.LANCZOS)
    if rotate:
        m = m.rotate(rotate, expand=True, resample=Image.BICUBIC)
    alpha = m.getchannel("A").point(lambda v: round(v * opacity))
    m.putalpha(alpha.filter(ImageFilter.GaussianBlur(0.4)))
    base = img.convert("RGBA")
    base.alpha_composite(m, (round(cx - m.width / 2), round(cy - m.height / 2)))
    return base.convert("RGB")


def banner(img, x, y, w, pad=0.12):
    word = WORD.resize((round(w * (1 - 2 * pad)), round(WORD.height * w * (1 - 2 * pad) / WORD.width)), Image.LANCZOS)
    h = round(word.height + w * pad)
    board = Image.new("RGBA", (w, h), (21, 101, 192, 255))
    board.alpha_composite(word, (round(w * pad), round(w * pad / 2)))
    base = img.convert("RGBA")
    base.alpha_composite(board, (x, y))
    return base.convert("RGB")


JOBS = {
    "hero-home": lambda im: banner(paste_mark(inpaint(denavy(denavy(im, (540, 690, 640, 740), 60), (1405, 630, 1620, 790), 75, 0.3, 0.45),
                                                     [(1394, 445, 1418, 498), (1414, 710, 1442, 736)]),
                                              "white", 1470, 455, 52), 592, 466, 176),
    "hero-away": lambda im: paste_mark(paste_mark(inpaint(im, [(592, 445, 622, 475), (1298, 474, 1328, 504), (1335, 970, 1372, 996)]),
                                                  "blue", 607, 460, 44), "blue", 1313, 490, 44),
    "prod-home-mens": lambda im: paste_mark(inpaint(denavy(im, (395, 90, 605, 215)), [(518, 288, 562, 322), (760, 330, 805, 372)]),
                                            "white", 540, 318, 72),
    "prod-away-mens": lambda im: paste_mark(inpaint(im, [(512, 318, 568, 348)]), "blue", 540, 335, 72),
    "prod-home-ladies": lambda im: paste_mark(inpaint(denavy(im, (355, 70, 655, 265)), [(558, 188, 602, 217)]),
                                              "white", 580, 212, 62),
    "prod-away-vest": lambda im: paste_mark(inpaint(im, [(503, 288, 557, 332)]), "blue", 530, 312, 66),
    "prod-cap-blue": lambda im: paste_mark(im, "white", 439, 340, 105),
    "prod-cap-white": lambda im: paste_mark(im, "blue", 512, 390, 110),
    "prod-shorts": lambda im: paste_mark(inpaint(im, [(882, 695, 922, 765)]), "white", 244, 731, 60),
    "lifestyle-cap": lambda im: im,
}

for name, job in JOBS.items():
    im = Image.open(SRC / f"{name}.webp").convert("RGB")
    job(im).save(OUT / f"{name}.webp", "WEBP", quality=90)
    print("OK", name)
