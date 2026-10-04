import urllib.request, re
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36","Accept-Language":"es-CL,es;q=0.9"}
def get(u):
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40); return r.status,r.read().decode("latin-1","replace")
    except Exception as e: return "ERR",str(e)
for u in ["https://www.cmfchile.cl/institucional/hechos/hechos_portada.php",
          "https://www.cmfchile.cl/institucional/hechos/hechos_portada.php?dias=7",
          "https://www.cmfchile.cl/portal/principal/613/w3-propertyvalue-18564.html"]:
    s,b=get(u); t=re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," | ",b))
    print("URL",u,s,len(b)); i=t.find("Colb"); print(t[:200]); print("...", t[max(0,i-1500):i+800] if i>0 else t[2000:5000])
    print("LINKS", re.findall(r'href="([^"]*(?:hecho|documento|aplic)[^"]*)"',b)[:15])
