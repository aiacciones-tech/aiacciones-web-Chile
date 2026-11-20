"""Temporary probe (2): find the public daily price history of a Bahrain Bourse stock (NBB) that the Mubasher stock page and the
Bahrain Bourse website show, by loading both pages in a browser and recording the responses that carry dated prices."""
import json, os, re
from playwright.sync_api import sync_playwright
out = {}
with sync_playwright() as p:
    br = p.chromium.launch()
    for k, u in {"mubasher": "https://english.mubasher.info/markets/BB/stocks/NBB", "bourse": "https://www.bahrainbourse.com/en/market-data/historical-data"}.items():
        pg = br.new_page(viewport={"width": 1400, "height": 2400}); hits = []
        def resp(r, hits=hits):
            try:
                ct = r.headers.get("content-type", "")
                if any(s in ct for s in ("json", "csv", "text/plain")):
                    t = r.text()
                    if len(re.findall(r"20(?:24|25|26)[-/]\d\d[-/]\d\d|1[67]\d{8}", t)) > 30: hits.append({"url": r.url, "len": len(t), "head": t[:600]})
            except Exception: pass
        pg.on("response", resp)
        try:
            pg.goto(u, wait_until="networkidle", timeout=60000)
            for _ in range(3): pg.mouse.wheel(0, 600); pg.wait_for_timeout(3000)
            pg.screenshot(path=f"/tmp/probe/{k}.png")
        except Exception as e:
            hits.append({"error": str(e)[:300]})
        out[k] = hits; pg.close()
    br.close()
json.dump(out, open("/tmp/probe/probe-velas-bahrain.json", "w"), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in out.items()})
