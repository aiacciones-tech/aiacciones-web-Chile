"""Temporary probe (3): the Mubasher stock list for Bahrain carries a chartFileUrl per stock; fetch NBB's and ALBH's chart files."""
import json, os, urllib.request
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=40).read().decode("utf-8", "replace")
out = {}
try:
    L = json.loads(get("https://english.mubasher.info/api/v1/stock-prices/daily?countryCode=bh&sort=turnover&desc=true&page=0&size=200"))["data"]["content"]
    out["lista"] = [{k: x.get(k) for k in ("exchange", "name", "code", "value", "chartFileUrl", "updatedAt", "url")} for x in L]
except Exception as e:
    out["lista_error"] = str(e)[:300]
for x in out.get("lista", []):
    if x["code"] in ("NBB", "ALBH") and x.get("chartFileUrl"):
        u = x["chartFileUrl"]; u = u if u.startswith("http") else "https://static.mubasher.info/" + u.lstrip("/")
        for d in (u, u.replace("Delay_Stock_Intraday", "Historical_Stock").replace("Intraday", "Historical")):
            try:
                b = get(d); out["csv_" + x["code"] + "_" + d[-60:]] = {"url": d, "len": len(b), "head": b[:300], "tail": b[-300:]}
            except Exception as e:
                out["csv_" + x["code"] + "_" + d[-60:]] = {"url": d, "error": str(e)[:200]}
os.makedirs("/tmp/probe", exist_ok=True)
json.dump(out, open("/tmp/probe/probe-velas-bahrain.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v if k != "lista" else len(v) for k, v in out.items()}, ensure_ascii=False)[:3000])
