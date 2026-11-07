"""Temporary probe: which public sources give daily and intraday candles of the Bahrain All Share Index from GitHub Actions
(TradingView charts of Bahrain need a paid data package). Writes data/probe-bahrain.json."""
import json, os, re, urllib.request
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
U = {
 "cnbc_1y": "https://ts-api.cnbc.com/harmony/app/charts/1Y.json?symbol=.BAX",
 "cnbc_1d": "https://ts-api.cnbc.com/harmony/app/charts/1D.json?symbol=.BAX",
 "cnbc_q": "https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol?symbols=.BAX&requestMethod=itv&noform=1&partnerId=2&fund=1&exthrs=1&output=json&events=1",
 "cnbc_1y_bhseasi": "https://ts-api.cnbc.com/harmony/app/charts/1Y.json?symbol=.BHSEASI",
 "inv_search": "https://api.investing.com/api/search/v2/search?q=bahrain%20all%20share",
 "inv_search2": "https://api.investing.com/api/search/v2/search?q=BAX",
 "mubasher_page": "https://english.mubasher.info/markets/BB/",
 "bb_home": "https://www.bahrainbourse.com/en",
 "bb_indices": "https://www.bahrainbourse.com/en/market-data/indices",
 "mw": "https://www.marketwatch.com/investing/index/bhseasi?countrycode=bh",
 "asharq": "https://asharqbusiness.com/stocks/security/BHSEASI:IND/",
 "yahoo_search": "https://query2.finance.yahoo.com/v1/finance/search?q=bahrain%20all%20share",
 "stooq": "https://stooq.com/q/d/l/?s=^bax&i=d",
}
out = {}
for k, u in U.items():
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA, "Accept": "*/*", "domain-id": "www"}), timeout=30)
        b = r.read().decode("utf-8", "replace")
        apis = sorted(set(re.findall(r'["\'](https?://[^"\']*(?:api|chart|json|ajax|history|Hist)[^"\']*)["\']', b, re.I)))[:40]
        out[k] = {"status": r.status, "len": len(b), "head": b[:1500], "apis": apis}
    except Exception as e:
        out[k] = {"error": str(e)[:300]}
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"), exist_ok=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "probe-bahrain.json"), "w"), ensure_ascii=False, indent=1)
print({k: v.get("status", v.get("error", "")[:80]) for k, v in out.items()})
