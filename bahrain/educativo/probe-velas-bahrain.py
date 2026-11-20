"""Temporary probe (5): Mubasher's classic site (english-old.mubasher.info) stock page of NBB: which chart files does it load?"""
import json, os, re, urllib.request
from playwright.sync_api import sync_playwright
out = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for code in ("NBB", "ALBH"):
        pg = br.new_page(viewport={"width": 1400, "height": 2000}); req = []
        pg.on("request", lambda r, req=req: req.append(r.url) if ("Charts" in r.url or ".csv" in r.url) else None)
        try:
            pg.goto(f"https://english-old.mubasher.info/markets/BB/stocks/{code}", wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(12000)
            h = pg.content(); out[code] = {"url": pg.url, "req": req, "html": sorted(set(re.findall(r"[^\"'\s]*(?:Charts_Dir)[^\"'\s]*", h)))[:20]}
        except Exception as e:
            out[code] = {"error": str(e)[:300], "req": req}
        pg.close()
    br.close()
for code, v in out.items():
    for u in [x for x in v.get("req", []) + v.get("html", []) if "Historical" in x and x.startswith("http")][:2]:
        try:
            b = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=40).read().decode()
            v.setdefault("csv", []).append({"url": u, "len": len(b), "head": b[:200], "tail": b[-200:]})
        except Exception as e:
            v.setdefault("csv", []).append({"url": u, "error": str(e)[:200]})
json.dump(out, open("/tmp/probe/probe-velas-bahrain.json", "w"), indent=1)
print(json.dumps(out, indent=1)[:4000])
