"""Temporary probe: which public sources give daily and intraday candles of the Bahrain All Share Index from GitHub Actions
(TradingView charts of Bahrain need a paid data package). Writes data/probe-bahrain.json."""
import json, os, re, urllib.request
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
U = {
 "mub_hist": "https://static.mubasher.info/File.MubasherCharts/File.Historical_Index_Charts_Dir/33182be0c5cdcd5072bb1864cdee4d3d6e.csv",
 "mub_intra": "https://static.mubasher.info/File.MubasherCharts/File.Delay_Index_Intraday_Charts_Dir/33182be0c5cdcd5072bb1864cdee4d3d6e.csv",
 "cnbc_5d": "https://ts-api.cnbc.com/harmony/app/charts/5D.json?symbol=.BAX",
 "mub_prices": "https://english.mubasher.info/api/1/stocks/prices/all?country=bh",
 "mub_listed": "https://english.mubasher.info/api/1/listed-companies?country=bh&size=100&start=0",
 "mub_market": "https://english.mubasher.info/api/1/market/bh/summary",
 "webapi": "https://webapi.bahrainbourse.com/",
 "bb_home": "https://www.bahrainbourse.com/en",
 "mub_page": "https://english.mubasher.info/markets/BB/",
 "mub_stocks": "https://english.mubasher.info/countries/bh/stock-prices",
}
CTX = {"bb_home": r"webapi[^\s]{0,200}|https?://[^\"']*webapi[^\"']*", "mub_page": r"(?:gainers|losers|api/1/[^\"']+)[^<]{0,120}", "mub_stocks": r"api/1/[^\"']+|window\.midata[^;]{0,500}"}
out = {}
for k, u in U.items():
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA, "Accept": "*/*", "domain-id": "www"}), timeout=30)
        b = r.read().decode("utf-8", "replace")
        apis = sorted(set(re.findall(r'["\'](https?://[^"\']*(?:api|chart|json|ajax|history|Hist)[^"\']*)["\']', b, re.I)))[:40]
        out[k] = {"status": r.status, "len": len(b), "head": b[:3000] if k not in ("mub_hist", "mub_intra") else b[:600] + " ... " + b[-1500:], "apis": apis,
                  "ctx": sorted(set(re.findall(CTX[k], b, re.I)))[:60] if k in CTX else None}
    except Exception as e:
        out[k] = {"error": str(e)[:300]}
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"), exist_ok=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "probe-bahrain.json"), "w"), ensure_ascii=False, indent=1)
print({k: v.get("status", v.get("error", "")[:80]) for k, v in out.items()})
