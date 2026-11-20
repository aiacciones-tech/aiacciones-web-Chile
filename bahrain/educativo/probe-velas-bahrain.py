"""Temporary probe (6): NBB's historical chart file on Mubasher stops in January 2026. Look at its intraday file and the classic
historical-prices page of NBB (recording the data responses) to find the rest of 2026."""
import json, os, re, urllib.request
from playwright.sync_api import sync_playwright
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=40).read().decode("utf-8", "replace")
out = {}
try:
    b = get("https://english-old.mubasher.info/mubasherFileServer/File.MubasherCharts/File.Delay_Stock_Intraday_Charts_Dir/220ec8ce6abb3e952a85b8551ba726a1227.csv")
    out["intra"] = {"len": len(b), "head": b[:200], "tail": b[-200:]}
except Exception as e: out["intra"] = str(e)[:200]
with sync_playwright() as p:
    br = p.chromium.launch()
    for k, u in {"hist": "https://english-old.mubasher.info/markets/BB/stocks/NBB/historical-prices", "nbb": "https://english-old.mubasher.info/markets/BB/stocks/NBB"}.items():
        pg = br.new_page(viewport={"width": 1400, "height": 2000}); hits = []
        def resp(r, hits=hits):
            try:
                if r.request.resource_type in ("xhr", "fetch") or "csv" in r.url:
                    t = r.text(); hits.append({"url": r.url, "len": len(t), "head": t[:400]})
            except Exception: pass
        pg.on("response", resp)
        try:
            pg.goto(u, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(12000)
            h = pg.content()
            out[k] = {"url": pg.url, "hits": hits[:40], "links": sorted(set(re.findall(r"(?:href|src|data-url)=\"([^\"]*(?:histor|Charts|csv|api)[^\"]*)\"", h, re.I)))[:40],
                      "dates": re.findall(r"\b20\d\d-\d\d-\d\d\b|\b\d\d/\d\d/20\d\d\b", h)[:20]}
            pg.screenshot(path=f"/tmp/probe/{k}.png")
        except Exception as e:
            out[k] = {"error": str(e)[:300], "hits": hits[:20]}
        pg.close()
    br.close()
json.dump(out, open("/tmp/probe/probe-velas-bahrain.json", "w"), indent=1)
print(json.dumps(out, indent=1)[:4000])
