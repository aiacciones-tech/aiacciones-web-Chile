"""Temporary probe: load the Mubasher pages of NBB and ALBH in a real browser and record the network requests (looking for the chart CSV)."""
import json, os
from playwright.sync_api import sync_playwright
out = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for k, u in {"nbb": "https://english.mubasher.info/markets/BB/stocks/NBB", "albh": "https://english.mubasher.info/markets/BB/stocks/ALBH",
                 "idx": "https://english.mubasher.info/markets/BB/"}.items():
        pg = b.new_page(); req = []
        pg.on("request", lambda r: req.append(r.url))
        try:
            pg.goto(u, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(5000)
            pg.mouse.wheel(0, 1500); pg.wait_for_timeout(4000)
        except Exception as e:
            req.append("ERROR " + str(e)[:200])
        out[k] = [x for x in req if not any(s in x for s in (".png", ".jpg", ".svg", ".woff", "google", "doubleclick", "facebook", ".css"))]
        pg.close()
    b.close()
os.makedirs("/tmp/probe", exist_ok=True)
json.dump(out, open("/tmp/probe/probe-red-bahrain.json", "w"), indent=1)
for k, v in out.items(): print(k, len(v), [x for x in v if "csv" in x.lower() or "chart" in x.lower()][:20])
