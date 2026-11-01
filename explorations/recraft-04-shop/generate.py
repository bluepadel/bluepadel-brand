#!/usr/bin/env python3
"""Shop imagery for the BluePadel apparel shop redesign (padel-cloud epic #1431) via Recraft v3.

python generate.py prompts.json out/   (reads the key from ~/.recraft_key; skips files already made)
"""
import json, pathlib, sys, urllib.error, urllib.request

KEY = pathlib.Path("~/.recraft_key").expanduser().read_text().strip()
API = "https://external.api.recraft.ai/v1/images/generations"
BLUE, NAVY, WHITE = [21, 101, 192], [13, 71, 161], [255, 255, 255]
NAMED = {"blue": BLUE, "navy": NAVY, "white": WHITE, "court": [25, 118, 210], "sky": [227, 242, 253]}


def gen(c: dict, out: pathlib.Path) -> str:
    controls = {"colors": [{"rgb": NAMED[n]} for n in c.get("colors", ["blue", "navy", "white"])]}
    if c.get("bg"):
        controls["background_color"] = {"rgb": NAMED[c["bg"]]}
    body = {"prompt": c["prompt"], "model": "recraftv3", "style": c.get("style", "realistic_image"),
            "size": c.get("size", "1024x1024"), "n": 1, "response_format": "url", "controls": controls}
    req = urllib.request.Request(API, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=240) as r:
        url = json.load(r)["data"][0]["url"]
    data = urllib.request.urlopen(url, timeout=120).read()
    ext = "svg" if b"<svg" in data[:500] else ("webp" if data[8:12] == b"WEBP" else "png")
    p = out / f"{c['id']}.{ext}"
    p.write_bytes(data)
    return str(p)


if __name__ == "__main__":
    prompts = json.loads(pathlib.Path(sys.argv[1]).read_text())
    out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    for c in prompts:
        if list(out.glob(f"{c['id']}.*")):
            print("SKIP", c["id"]); continue
        try:
            print("OK  ", gen(c, out), flush=True)
        except urllib.error.HTTPError as e:
            print("FAIL", c["id"], e.code, e.read().decode()[:300], flush=True)
        except Exception as e:  # noqa: BLE001
            print("FAIL", c["id"], repr(e), flush=True)
