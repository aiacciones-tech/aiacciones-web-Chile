import urllib.request, json, re, sys
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36","Accept-Language":"en-US,en;q=0.9"}
def get(u):
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30); b=r.read().decode("utf-8","replace"); return r.status,b
    except Exception as e: return "ERR",str(e)
for sym in ["^IPSA","^IGPA","IGPA.SN","^SPIPSA","COLBUN.SN","SQM-B.SN"]:
    s,b=get("https://query1.finance.yahoo.com/v8/finance/chart/%s?range=1y&interval=1d"%urllib.parse.quote(sym))
    try:
        j=json.loads(b)["chart"]["result"][0]; m=j["meta"]; c=j["indicators"]["quote"][0]["close"]
        print("YAHOO",sym,m.get("regularMarketPrice"),m.get("chartPreviousClose"),m.get("regularMarketTime"),m.get("longName") or m.get("shortName"),"n=",len(c),"first",c[0])
    except Exception as e: print("YAHOO",sym,s,str(b)[:150])
s,b=get("https://stockanalysis.com/list/santiago-stock-exchange/")
print("SA list",s,len(b)); i=b.find("COLBUN"); print(b[i-300:i+400] if i>0 else b[:300])
s,b=get("https://stockanalysis.com/quote/snse/COLBUN/statistics/")
print("SA stats",s,len(b))
for k in ["peRatio","peForward","forwardPE","PE Ratio","Forward PE"]:
    i=b.find(k); print(k, b[i-100:i+250].replace("\n"," ") if i>0 else None)
s,b=get("https://worldperatio.com/area/chile/")
print("WPE",s,len(b)); 
for k in ["11.06","5-Year","10-Year","Average"]:
    i=b.find(k); print(k, re.sub(r"\s+"," ",re.sub("<[^>]+>"," ",b[i-200:i+300])) if i>0 else None)
s,b=get("https://en.wikipedia.org/wiki/S%26P_IPSA")
print("WIKI",s,len(b)); i=b.find("Constituents"); print(re.sub(r"\s+"," ",re.sub("<[^>]+>"," ",b[i:i+3000])) if i>0 else None)
