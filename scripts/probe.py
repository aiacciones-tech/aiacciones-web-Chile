import urllib.request, json, re
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36","Accept-Language":"en-US,en;q=0.9","Origin":"https://www.tradingview.com","Referer":"https://www.tradingview.com/"}
def get(u,data=None,h=None):
    try:
        hh=dict(UA); hh.update(h or {})
        r=urllib.request.urlopen(urllib.request.Request(u,data=data,headers=hh),timeout=30); return r.status,r.read().decode("utf-8","replace")
    except Exception as e: return "ERR",str(e)
for t in ["IPSA","IGPA","SP IPSA"]:
    s,b=get("https://symbol-search.tradingview.com/symbol_search/v3/?text=%s&hl=0&exchange=BCS&lang=en&search_type=&domain=production"%urllib.parse.quote(t))
    print("SEARCH",t,s,b[:900])
cols=["name","description","close","change","Perf.YTD","Perf.Y","time","type"]
for tk in [["BCS:SP_IPSA","BCS:SP_IGPA"],["BCS:IPSA","BCS:IGPA"]]:
    for mk in ["global","chile","cfd"]:
        s,b=get("https://scanner.tradingview.com/%s/scan"%mk,json.dumps({"symbols":{"tickers":tk},"columns":cols}).encode(),{"Content-Type":"application/json"})
        print("SCAN",mk,tk,s,b[:400])
s,b=get("https://worldperatio.com/area/chile/")
for k in ["10.03","13.05","Rolling 5Y","avg5","Avg5","5Y Avg"]:
    i=b.find(k); print("WPE",k, b[max(0,i-300):i+300].replace("\n"," ") if i>=0 else None)
