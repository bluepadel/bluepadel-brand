#!/usr/bin/env python3
"""Generate BluePadel logo concepts via the Recraft API (SVG vector output)."""
import json, os, sys, urllib.request, pathlib

KEY = pathlib.Path(os.path.expanduser("~/.recraft_key")).read_text().strip()
API = "https://external.api.recraft.ai/v1/images/generations"
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(".")
OUT.mkdir(parents=True, exist_ok=True)

# BluePadel brand palette (RGB) — brand blue #1565C0, hover #1976D2, active #0D47A1,
# near-black navy #0B1320.  White background.
BLUE   = [21, 101, 192]
BLUE_H = [25, 118, 210]
NAVY   = [13, 71, 161]
INK    = [11, 19, 32]

def rgb(*cs): return [{"rgb": c} for c in cs]

# concepts: fresh directions for an automatic padel-scoring brand
CONCEPTS = json.loads(pathlib.Path(sys.argv[2]).read_text()) if len(sys.argv) > 2 else []

def gen(concept):
    body = {
        "prompt": concept["prompt"],
        "model": "recraftv3",
        "style": concept.get("style", "vector_illustration"),
        "n": concept.get("n", 1),
        "size": "1024x1024",
        "response_format": "url",
        "controls": {
            "colors": rgb(*concept.get("colors", [BLUE, NAVY, INK])),
            "background_color": {"rgb": [255, 255, 255]},
        },
    }
    req = urllib.request.Request(
        API, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        method="POST")
    with urllib.request.urlopen(req, timeout=180) as r:
        res = json.load(r)
    urls = [d["url"] for d in res["data"]]
    saved = []
    for i, u in enumerate(urls):
        data = urllib.request.urlopen(u, timeout=120).read()
        is_svg = b"<svg" in data[:500]
        ext = "svg" if is_svg else "png"
        p = OUT / f"{concept['id']}{'' if len(urls)==1 else f'-{i+1}'}.{ext}"
        p.write_bytes(data)
        saved.append(str(p))
    return saved

if __name__ == "__main__":
    for c in CONCEPTS:
        try:
            for s in gen(c):
                print("OK  ", s)
        except urllib.error.HTTPError as e:
            print("FAIL", c["id"], e.code, e.read().decode()[:300])
        except Exception as e:
            print("FAIL", c["id"], repr(e))
