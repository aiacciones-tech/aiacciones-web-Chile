"""Descarga los informes oficiales (PDF) de un capítulo de la serie fundamental de @AIStocksUAE y extrae su texto, para leer las cifras.
Corre en GitHub Actions (datos-fundamental-eau.yml): el contenedor de Claude no llega a dfm.ae, adx.ae, nasdaqdubai ni a las webs de las empresas.
video.json → "documentos": [{"id": "fs-2025", "url": "https://...pdf"}]. Deja <salida>/docs/<id>.txt (una página por bloque «=== página N»).
Si ya existen, no se vuelven a pedir.  uso: python3 docs_fundamental.py <video.json> <carpeta de salida>"""
import json, os, sys, urllib.request
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
VJ = json.load(open(sys.argv[1])); out = os.path.join(sys.argv[2], "docs"); os.makedirs(out, exist_ok=True)
for d in VJ.get("documentos", []):
    pdf, txt = os.path.join(out, d["id"] + ".pdf"), os.path.join(out, d["id"] + ".txt")
    if os.path.exists(txt): print("ya está:", d["id"]); continue
    try:
        data = urllib.request.urlopen(urllib.request.Request(d["url"], headers={"User-Agent": UA, "Accept": "application/pdf,*/*"}), timeout=90).read()
        if not data.startswith(b"%PDF"):   # página web: texto sin etiquetas
            import re, html
            t = re.sub(r"(?s)<(script|style).*?</\1>", " ", data.decode("utf-8", "ignore")); t = html.unescape(re.sub(r"<[^>]+>", " ", t))
            open(txt, "w").write(re.sub(r"\s*\n\s*", "\n", re.sub(r"[ \t]+", " ", t))); print(d["id"], "html", len(t)); continue
        open(pdf, "wb").write(data)
        from pypdf import PdfReader
        r = PdfReader(pdf)
        open(txt, "w").write("\n".join(f"=== página {i + 1}\n{p.extract_text() or ''}" for i, p in enumerate(r.pages)))
        print(d["id"], len(data), "bytes,", len(r.pages), "páginas")
        os.remove(pdf)   # en la rama solo se guarda el texto (los PDF pesan mucho)
    except Exception as e:
        print("ERROR", d["id"], d["url"], e); open(os.path.join(out, d["id"] + ".error"), "w").write(str(e))
