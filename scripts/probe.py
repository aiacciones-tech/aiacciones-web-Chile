import urllib.request, re
UA={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"}
r=urllib.request.urlopen(urllib.request.Request("https://www.cmfchile.cl/institucional/hechos/hechos_portada.php",headers=UA),timeout=40)
print(r.headers.get("Content-Type")); b=r.read()
s=b.decode("utf-8","replace"); i=s.find("PLAZA S.A."); print(s[i-1500:i+700])
print("ROWS", len(re.findall(r"ver_sgd\.php",s)))
