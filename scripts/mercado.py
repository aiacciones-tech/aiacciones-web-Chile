"""Datos de mercado para aiacciones.cl (corre en GitHub Actions, que tiene internet).
uso: python3 scripts/mercado.py fetch   -> web/assets/mercado.json
Fuentes: TradingView (precios de cierre, índices MSCI IPSA/IGPA, utilidad estimada)
y worldperatio.com (P/E del mercado chileno y promedios de 5 y 10 años, base MSCI Chile)."""
import json, re, sys, os, datetime, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "web", "assets", "mercado.json")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
      "Origin": "https://www.tradingview.com", "Referer": "https://www.tradingview.com/", "Content-Type": "application/json"}
# id de ficha -> ticker de la Bolsa de Santiago (las que no cotizan no van)
FICHAS = {"andina-a": "ANDINA-A", "ccu": "CCU", "ltm": "LTM", "conchatoro": "CONCHATORO", "aguas-a": "AGUAS-A", "bci": "BCI", "besalco": "BESALCO", "bsantander": "BSANTANDER", "cap": "CAP",
          "cencomalls": "CENCOMALLS", "cencosud": "CENCOSUD", "cge": "CGE", "chile": "CHILE", "cmpc": "CMPC",
          "colbun": "COLBUN", "copec": "COPEC", "ecl": "ECL", "enelchile": "ENELCHILE", "enelgxch": "ENELGXCH",
          "falabella": "FALABELLA", "habitat": "HABITAT", "iam": "IAM", "itau": "ITAUCL", "mallplaza": "MALLPLAZA",
          "parauco": "PARAUCO", "pehuenche": "PEHUENCHE", "planvital": "PLANVITAL", "provida": "PROVIDA", "quinenco": "QUINENCO",
          "ripley": "RIPLEY", "schwager": "SCHWAGER", "sk": "SK", "sqm-b": "SQM-B", "vapores": "VAPORES"}
INDICES = [("ipsa", "IPSA", "BCS:MXIPSAGC", "MSCI IPSA (con dividendos)"),
           ("igpa", "IGPA", "BCS:MXIGPAGC", "MSCI IGPA (con dividendos)")]
COLS = ["name", "description", "close", "change", "Perf.YTD", "Perf.Y", "time", "market_cap_basic",
        "price_earnings_ttm", "earnings_per_share_forecast_next_fy", "country", "type"]


def post(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=UA)
    return json.loads(urllib.request.urlopen(req, timeout=40).read().decode())


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA["User-Agent"]})
    return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")


def rows(resp):
    return {r["s"]: dict(zip(COLS, r["d"])) for r in resp.get("data", [])}


def chile_date(ts):
    return (datetime.datetime.utcfromtimestamp(ts) - datetime.timedelta(hours=3)).date().isoformat() if ts else None


def fetch():
    cands = {fid: ["BCS:" + t.replace("-", "_"), "BCS:" + t.replace("-", ""), "BCS:" + t] for fid, t in FICHAS.items()}
    tickers = sorted({c for v in cands.values() for c in v} | {s for _, _, s, _ in INDICES})
    data = rows(post("https://scanner.tradingview.com/global/scan", {"symbols": {"tickers": tickers}, "columns": COLS}))
    acc = {}
    for fid, cs in cands.items():
        s = next((c for c in cs if c in data and data[c]["close"]), None)
        if not s:
            print("SIN DATOS", fid, cs)
            continue
        d = data[s]
        acc[fid] = {"t": FICHAS[fid], "px": d["close"], "d1": d["change"], "y1": d["Perf.Y"], "ytd": d["Perf.YTD"],
                    "fecha": chile_date(d["time"])}
    idx = {}
    for key, name, s, full in INDICES:
        d = data.get(s)
        if not d:
            print("SIN INDICE", s)
            continue
        idx[key] = {"n": name, "full": full, "v": d["close"], "d1": d["change"], "ytd": d["Perf.YTD"],
                    "y1": d["Perf.Y"], "fecha": chile_date(d["time"])}
    # Forward P/E estimado: 30 mayores empresas chilenas que cotizan en Santiago (aprox. IPSA)
    fwd = {"v": None}
    try:
        scan = post("https://scanner.tradingview.com/chile/scan", {"columns": COLS, "range": [0, 400],
                    "filter": [{"left": "type", "operation": "equal", "right": "stock"}],
                    "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"}})
        big = []
        for r in scan.get("data", []):
            d = dict(zip(COLS, r["d"]))
            if d.get("country") != "Chile" or not d.get("market_cap_basic"):
                continue
            if any(b["desc"] == d["description"] for b in big):
                continue
            big.append({"s": r["s"], "desc": d["description"], "cap": d["market_cap_basic"], "close": d["close"],
                        "eps_f": d["earnings_per_share_forecast_next_fy"]})
            if len(big) == 30:
                break
        num = den = cov = 0.0
        tot = sum(b["cap"] for b in big)
        for b in big:
            if b["eps_f"] and b["eps_f"] > 0:
                fpe = b["close"] / b["eps_f"]
                if 2 <= fpe <= 80:
                    num += b["cap"]; den += b["cap"] / fpe; cov += b["cap"]
        fwd = {"v": round(num / den, 2) if den else None, "cobertura": round(cov / tot * 100) if tot else None,
               "empresas": len(big), "fecha": idx.get("ipsa", {}).get("fecha")}
        print("TOP30", [(b["s"], round(b["close"] / b["eps_f"], 1) if b["eps_f"] else None) for b in big])
    except Exception as e:
        print("forward falló:", e)
    # P/E del mercado chileno y promedios (worldperatio, base MSCI Chile vía ETF ECH)
    wpe = {}
    try:
        t = re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", get("https://worldperatio.com/area/chile/")))
        m = re.search(r"(\d{1,2} \w+ \d{4}) · P/E Ratio: ([\d.]+)", t)
        a5 = re.search(r"5Y Average: ([\d.]+)", t)
        a10 = re.search(r"10Y Average: ([\d.]+)", t)
        if m and a5 and a10:
            wpe = {"pe": float(m.group(2)), "avg5": float(a5.group(1)), "avg10": float(a10.group(1)),
                   "fecha": datetime.datetime.strptime(m.group(1), "%d %B %Y").date().isoformat(),
                   "fuente": "worldperatio.com (MSCI Chile, ETF ECH)"}
    except Exception as e:
        print("worldperatio falló:", e)
    old = json.load(open(OUT)) if os.path.exists(OUT) else {}
    out = {"actualizado": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ"),
           "acciones": acc or old.get("acciones", {}), "indices": idx or old.get("indices", {}),
           "fwd": fwd if fwd.get("v") else old.get("fwd"), "wpe": wpe or old.get("wpe")}
    json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: out[k] for k in ("indices", "fwd", "wpe")}, ensure_ascii=False))
    print(len(out["acciones"]), "acciones")


# Hechos esenciales (CMF): portada con los recibidos en los últimos 7 días; se acumulan en hechos.json
EMISORES = {"andina-a": ["EMBOTELLADORA ANDINA S.A."], "bci": ["BANCO DE CREDITO E INVERSIONES"],
            "besalco": ["BESALCO S.A."], "bsantander": ["BANCO SANTANDER-CHILE", "BANCO SANTANDER CHILE"],
            "cap": ["CAP S.A."], "cencomalls": ["CENCOSUD SHOPPING S.A."], "cencosud": ["CENCOSUD S.A."],
            "cge": ["CGE S.A.", "COMPANIA GENERAL DE ELECTRICIDAD S.A."], "chile": ["BANCO DE CHILE"],
            "cmpc": ["EMPRESAS CMPC S.A."], "colbun": ["COLBUN S.A."], "copec": ["EMPRESAS COPEC S.A."],
            "ecl": ["ENGIE ENERGIA CHILE S.A."], "enelchile": ["ENEL CHILE S.A."],
            "enelgxch": ["ENEL GENERACION CHILE S.A."], "falabella": ["FALABELLA S.A."],
            "habitat": ["ADMINISTRADORA DE FONDOS DE PENSIONES HABITAT S.A.", "AFP HABITAT S.A."],
            "iam": ["INVERSIONES AGUAS METROPOLITANAS S.A."], "aguas-a": ["AGUAS ANDINAS S.A."], "itau": ["BANCO ITAU CHILE", "ITAU CORPBANCA"],
            "mallplaza": ["PLAZA S.A."], "parauco": ["PARQUE ARAUCO S.A."], "planvital": ["AFP PLANVITAL S.A."],
            "provida": ["AFP PROVIDA S.A.", "ADMINISTRADORA DE FONDOS DE PENSIONES PROVIDA S.A."],
            "quinenco": ["QUINENCO S.A."], "ripley": ["RIPLEY CORP S.A."], "schwager": ["SCHWAGER S.A."],
            "sk": ["SIGDO KOPPERS S.A."], "sqm-b": ["SOCIEDAD QUIMICA Y MINERA DE CHILE S.A."],
            "vapores": ["COMPANIA SUD AMERICANA DE VAPORES S.A."], "aes-andes": ["AES ANDES S.A."],
            "afpcapital": ["AFP CAPITAL S.A.", "ADMINISTRADORA DE FONDOS DE PENSIONES CAPITAL S.A."]}
HOUT = os.path.join(ROOT, "web", "assets", "hechos.json")


def norm(t):
    import unicodedata
    t = unicodedata.normalize("NFD", t.upper())
    return re.sub(r"\s+", " ", "".join(c for c in t if unicodedata.category(c) != "Mn")).strip()


def hechos():
    import html as H
    idx = {norm(n): fid for fid, ns in EMISORES.items() for n in ns}
    old = json.load(open(HOUT)) if os.path.exists(HOUT) else {"items": []}
    items = {i["num"]: i for i in old["items"]}
    b = get("https://www.cmfchile.cl/institucional/hechos/hechos_portada.php")
    n = 0
    for tr in re.findall(r"<tr>(.*?)</tr>", b, re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        a = re.search(r'href="([^"]*ver_sgd\.php[^"]*)"[^>]*>\s*(\d+)', tr)
        if len(tds) < 4 or not a:
            continue
        ent = H.unescape(re.sub("<[^>]+>", " ", tds[2])).strip()
        fid = idx.get(norm(ent))
        if not fid:
            continue
        f = re.match(r"(\d\d)/(\d\d)/(\d{4}) (\d\d:\d\d)", re.sub("<[^>]+>", "", tds[0]).strip())
        mat = [H.unescape(x).strip() for x in re.split(r"<br\s*/?>|\n", " | ".join(tds[3:])) if x.strip()]
        mat = [m.strip(" |") for m in " | ".join(mat).split(" | ") if m.strip(" |")]
        items[a.group(2)] = {"num": a.group(2), "id": fid, "ent": ent, "fecha": f"{f.group(3)}-{f.group(2)}-{f.group(1)} {f.group(4)}" if f else "",
                             "materias": mat, "url": "https://www.cmfchile.cl" + H.unescape(a.group(1))}
        n += 1
    keep = sorted(items.values(), key=lambda i: i["fecha"], reverse=True)
    corte = (datetime.date.today() - datetime.timedelta(days=400)).isoformat()
    keep = [i for i in keep if i["fecha"] >= corte]
    json.dump({"actualizado": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ"), "items": keep},
              open(HOUT, "w"), ensure_ascii=False, indent=1)
    print("hechos esenciales:", n, "nuevos/vistos hoy,", len(keep), "guardados")


if __name__ == "__main__":
    if sys.argv[1:] == ["fetch"]:
        fetch()
        try:
            hechos()
        except Exception as e:
            print("hechos falló:", e)
    else:
        print(__doc__)
