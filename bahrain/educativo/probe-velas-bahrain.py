"""Temporary probe: where to get ~2 years of daily candles of a Bahrain Bourse stock (NBB, ALBH) from GitHub Actions.
TradingView charts of Bahrain are paid; the index CSV comes from Mubasher, so look for the stock CSV on Mubasher pages."""
import json, os, re, sys, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "daily-bahrain"))
import importlib.util
spec = importlib.util.spec_from_file_location("md", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "daily-bahrain", "market-data-bahrain.py"))
md = importlib.util.module_from_spec(spec); spec.loader.exec_module(md)
UA = md.UA
out = {}
def fetch(u, extra=None):
    h = {"User-Agent": UA, "Accept": "*/*"}; h.update(extra or {})
    r = urllib.request.urlopen(urllib.request.Request(u, headers=h), timeout=30)
    return r.status, r.read().decode("utf-8", "replace")
for s in ["BAHRAIN:NBB", "BAHRAIN:ALBH"]:
    try:
        v = md.tv_velas(s, "1D", 520)["velas"]; out["tv_" + s] = {"n": len(v), "first": v[0], "last": v[-1]}
    except Exception as e:
        out["tv_" + s] = {"error": str(e)[:300]}
hashes = set()
for k, u in {"mub_nbb": "https://english.mubasher.info/markets/BB/stocks/NBB", "mub_nbb_ar": "https://www.mubasher.info/markets/BB/stocks/NBB",
             "mub_albh": "https://english.mubasher.info/markets/BB/stocks/ALBH", "mub_idx": "https://english.mubasher.info/markets/BB/",
             "mub_api_nbb": "https://english.mubasher.info/api/1/stocks/NBB?country=bh", "mub_api_nbb2": "https://english.mubasher.info/api/1/stocks/BB/NBB",
             "mub_chart_api": "https://english.mubasher.info/api/1/stocks/NBB/chart?period=2y&country=bh"}.items():
    try:
        st, b = fetch(u)
        hs = set(re.findall(r"[0-9a-f]{32,34}", b)); hashes |= hs
        out[k] = {"status": st, "len": len(b), "charts": sorted(set(re.findall(r"[^\"'\s]{0,80}(?:Charts?_Dir|MubasherCharts|\.csv)[^\"'\s]{0,120}", b)))[:40],
                  "hashes": sorted(hs)[:40], "apis": sorted(set(re.findall(r"api/1/[^\"'\s<]{0,120}", b)))[:40],
                  "ctx": [b[max(0, m.start() - 200):m.end() + 200] for m in re.finditer(r"33182be0c5|chart", b, re.I)][:6], "head": b[:800]}
    except Exception as e:
        out[k] = {"error": str(e)[:300]}
base = "https://static.mubasher.info/File.MubasherCharts/File.{}_Charts_Dir/{}.csv"
for h in sorted(hashes)[:30]:
    for d in ["Historical_Stock", "Historical_Index", "Historical"]:
        u = base.format(d, h)
        try:
            st, b = fetch(u); out["csv_" + d + "_" + h] = {"status": st, "len": len(b), "head": b[:200], "tail": b[-200:]}
        except Exception as e:
            pass
os.makedirs("/tmp/probe", exist_ok=True)
json.dump(out, open("/tmp/probe/probe-velas-bahrain.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v.get("error") or v.get("status") or v.get("n")) for k, v in out.items()}, indent=1))
