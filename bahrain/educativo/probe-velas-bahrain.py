"""Temporary probe (4): open Mubasher's classic site for NBB (button «Switch to Classic Site») and record the chart files it loads."""
import json, os, re
from playwright.sync_api import sync_playwright
out = {"req": [], "html": []}
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={"width": 1400, "height": 2000})
    pg.on("request", lambda r: out["req"].append(r.url) if ("static.mubasher" in r.url or "Charts" in r.url or ".csv" in r.url) else None)
    try:
        pg.goto("https://english.mubasher.info/markets/BB/stocks/NBB", wait_until="networkidle", timeout=60000)
        try: pg.get_by_text("Switch to Classic Site").first.click(timeout=5000); pg.wait_for_load_state("networkidle", timeout=60000)
        except Exception as e: out["click"] = str(e)[:200]
        out["url_after"] = pg.url
        if "stocks/NBB" not in pg.url:
            pg.goto("https://english.mubasher.info/markets/BB/stocks/NBB", wait_until="networkidle", timeout=60000)
        pg.wait_for_timeout(6000); out["url_final"] = pg.url
        h = pg.content(); out["html"] = sorted(set(re.findall(r"[^\"'\s]*(?:Charts_Dir|MubasherCharts)[^\"'\s]*", h)))[:40]; out["len"] = len(h)
        pg.screenshot(path="/tmp/probe/classic.png")
    except Exception as e:
        out["error"] = str(e)[:300]
    br.close()
json.dump(out, open("/tmp/probe/probe-velas-bahrain.json", "w"), indent=1)
print(json.dumps(out, indent=1)[:3000])
