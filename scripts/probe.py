import urllib.request, json, re
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36","Accept-Language":"en-US,en;q=0.9"}
def get(u,data=None,h=None):
    try:
        hh=dict(UA); hh.update(h or {})
        r=urllib.request.urlopen(urllib.request.Request(u,data=data,headers=hh),timeout=30); return r.status,r.read().decode("utf-8","replace")
    except Exception as e: return "ERR",str(e)
q={"symbols":{"tickers":["BCS:SP_IPSA","BCS:SP_IGPA","BCS:SPCLXIPSA","BCS:IPSA","BCS:IGPA","BCS:COLBUN","BCS:SQM_B"]},"columns":["name","description","close","change","change_abs","Perf.YTD","Perf.Y","price_earnings_ttm","price_earnings_forward_fy","market_cap_basic","time"]}
s,b=get("https://scanner.tradingview.com/chile/scan",json.dumps(q).encode(),{"Content-Type":"application/json"})
print("TV chile",s,b[:1500])
s,b=get("https://scanner.tradingview.com/global/scan",json.dumps(q).encode(),{"Content-Type":"application/json"})
print("TV global",s,b[:1500])
s,b=get("https://www.ishares.com/us/products/239618/ishares-msci-chile-capped-etf/1467271812596.ajax?fileType=csv&fileName=ECH_holdings&dataType=fund")
print("ISH",s,len(b)); print(b[:1800])
s,b=get("https://worldperatio.com/area/chile/")
t=re.sub(r"\s+"," ",re.sub("<[^>]+>"," ",b))
for k in ["5Y","10Y","5-Y","10-Y","5 Y","10 Y","20Y"]:
    for m in re.finditer(re.escape(k),t): print(k,"|",t[max(0,m.start()-120):m.start()+160]); break
