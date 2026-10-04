import urllib.request, json
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36","Origin":"https://www.tradingview.com","Referer":"https://www.tradingview.com/","Content-Type":"application/json"}
def post(u,d):
    try: return urllib.request.urlopen(urllib.request.Request(u,data=json.dumps(d).encode(),headers=UA),timeout=30).read().decode()
    except Exception as e: return "ERR "+str(e)
cols=["name","description","close","change","Perf.YTD","Perf.Y","time","type"]
print("IDX",post("https://scanner.tradingview.com/global/scan",{"symbols":{"tickers":["BCS:MXIPSAPC","BCS:MXIPSAGC","BCS:MXIGPAPC","BCS:MXIGPAGC","BCS:SPCLXIGPA","BCS:SPCLXIGL","BCS:IGPA","BCS:SPIPSA"]},"columns":cols}))
for t in ["IGPA index","MSCI IGPA","MSCI Chile"]:
    try:
        b=urllib.request.urlopen(urllib.request.Request("https://symbol-search.tradingview.com/symbol_search/v3/?text=%s&exchange=BCS&lang=en&search_type=index&domain=production"%urllib.parse.quote(t),headers=UA),timeout=30).read().decode()
        print("S",t,[(s["symbol"],s["description"]) for s in json.loads(b)["symbols"]][:20])
    except Exception as e: print("S",t,e)
c2=["name","close","market_cap_basic","price_earnings_ttm","earnings_per_share_forecast_next_fy","price_earnings_forward_fy","non_gaap_price_to_earnings_per_share_forecast_next_fy","earnings_per_share_diluted_ttm"]
r=post("https://scanner.tradingview.com/chile/scan",{"columns":c2,"index_filters":[{"name":"scanner_index","values":["BCS:MXIPSAPC"]}],"range":[0,60],"sort":{"sortBy":"market_cap_basic","sortOrder":"desc"}})
print("MEMBERS",r[:4000])
