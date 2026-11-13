"""Datos oficiales de la serie «عمالقة وول ستريت» (Nabd Wall Street): para cada una de las 20 empresas, su último informe de resultados
en la SEC (8-K con el punto 2.02, o 10-Q/10-K si la empresa no publica 8-K de resultados, como Berkshire), el texto del comunicado (EX-99.1)
y las series trimestrales de sus estados financieros (XBRL, companyfacts). Más las próximas fechas de resultados (TradingView).
Corre en GitHub Actions (serie20-datos-Nabd.yml): el contenedor de Claude no llega a la SEC ni a TradingView.
uso: python3 datos_sec.py <carpeta de salida>   -> calendario.json y <TICKER>/sec.json, <TICKER>/comunicado-<fecha>.txt
Solo biblioteca estándar."""
import json, os, re, sys, time, html, gzip, datetime as dt, urllib.request

UA = {"User-Agent": "NabdWallStreet aiacciones-bot@users.noreply.github.com", "Accept-Encoding": "gzip"}
INICIO = os.environ.get("SERIE20_INICIO", "2026-10-01")   # «a partir de este trimestre» (Daniel, 13-nov-2026)
EMPRESAS = [  # ticker de la serie, ticker SEC, símbolo TradingView, CIK de respaldo
    ("NVDA", "NVDA", "NASDAQ:NVDA", 1045810), ("MSFT", "MSFT", "NASDAQ:MSFT", 789019), ("AAPL", "AAPL", "NASDAQ:AAPL", 320193),
    ("GOOGL", "GOOGL", "NASDAQ:GOOGL", 1652044), ("AMZN", "AMZN", "NASDAQ:AMZN", 1018724), ("META", "META", "NASDAQ:META", 1326801),
    ("AVGO", "AVGO", "NASDAQ:AVGO", 1730168), ("TSLA", "TSLA", "NASDAQ:TSLA", 1318605), ("BRK", "BRK-B", "NYSE:BRK.A", 1067983),
    ("JPM", "JPM", "NYSE:JPM", 19617), ("LLY", "LLY", "NYSE:LLY", 59478), ("WMT", "WMT", "NASDAQ:WMT", 104169),
    ("ORCL", "ORCL", "NYSE:ORCL", 1341439), ("V", "V", "NYSE:V", 1403161), ("MA", "MA", "NYSE:MA", 1141391),
    ("XOM", "XOM", "NYSE:XOM", 34088), ("NFLX", "NFLX", "NASDAQ:NFLX", 1065280), ("COST", "COST", "NASDAQ:COST", 909832),
    ("JNJ", "JNJ", "NYSE:JNJ", 200406), ("PLTR", "PLTR", "NASDAQ:PLTR", 1321655)]
DUR = {  # conceptos de duración (cuenta de resultados y flujos); el primero con datos más recientes gana
    "ingresos": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet"],
    "beneficio_bruto": ["GrossProfit"],
    "resultado_operativo": ["OperatingIncomeLoss"],
    "beneficio_neto": ["NetIncomeLoss", "ProfitLoss", "NetIncomeLossAvailableToCommonStockholdersBasic"],
    "flujo_operativo": ["NetCashProvidedByUsedInOperatingActivities"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
    "dividendos": ["PaymentsOfDividends", "PaymentsOfDividendsCommonStock"],
    "recompras": ["PaymentsForRepurchaseOfCommonStock"],
    "eps_diluido": ["EarningsPerShareDiluted"],
}
INST = {  # conceptos de saldo (balance)
    "caja": ["CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents", "CashAndDueFromBanks"],
    "inversiones_cp": ["ShortTermInvestments", "MarketableSecuritiesCurrent", "AvailableForSaleSecuritiesDebtSecuritiesCurrent"],
    "deuda_lp": ["LongTermDebtNoncurrent", "LongTermDebt"],
    "deuda_cp": ["LongTermDebtCurrent", "DebtCurrent"],
    "papel_comercial": ["CommercialPaper"],
    "activos": ["Assets"], "pasivos": ["Liabilities"],
    "patrimonio": ["StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"],
}


def get(url, tries=4):
    for i in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60); b = r.read()
            if r.headers.get("Content-Encoding") == "gzip": b = gzip.decompress(b)
            time.sleep(0.15); return b   # la SEC pide no pasar de 10 peticiones por segundo
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(2 ** i * 2)


D = lambda s: dt.date.fromisoformat(s)


def trimestral(facts):
    """Valores de 3 meses por fecha de cierre: el dato trimestral si existe; si no, acumulado del año menos el acumulado anterior
    (así salen los flujos de caja de los 10-Q y el 4.º trimestre de los 10-K). Devuelve {fin: (valor, form, presentado)}."""
    por = {}
    for f in facts:
        if "start" not in f or f.get("form") not in ("10-Q", "10-K", "10-Q/A", "10-K/A", "8-K"): continue
        k = (f["start"], f["end"])
        if k not in por or f["filed"] > por[k]["filed"]: por[k] = f
    out = {}
    for (s, e), f in por.items():
        dias = (D(e) - D(s)).days
        if 80 <= dias <= 100: out[e] = (f["val"], f["form"], f["filed"], "trimestre")
    for (s, e), f in sorted(por.items(), key=lambda x: x[0][1]):
        if e in out or (D(e) - D(s)).days < 150: continue
        prev = [(e2, g) for (s2, e2), g in por.items() if s2 == s and 80 <= (D(e) - D(e2)).days <= 100]
        if prev: out[e] = (f["val"] - prev[0][1]["val"], f["form"], f["filed"], "محسوب: المتراكم ناقص المتراكم السابق")
    return out


def series(cf):
    g = cf.get("facts", {}).get("us-gaap", {}); T, B, usado = {}, {}, {}
    for k, cands in DUR.items():
        mejor = None
        for c in cands:
            u = g.get(c, {}).get("units", {}); facts = u.get("USD/shares" if k == "eps_diluido" else "USD", [])
            q = trimestral(facts) if k != "eps_diluido" else {f["end"]: (f["val"], f["form"], f["filed"], "trimestre") for f in facts
                                                                  if "start" in f and 80 <= (D(f["end"]) - D(f["start"])).days <= 100}
            if q and (not mejor or max(q) > max(mejor[1])): mejor = (c, q)
        if mejor:
            usado[k] = mejor[0]
            for e, v in mejor[1].items(): T.setdefault(e, {})[k] = v[0]; T[e].setdefault("_nota", {})[k] = v[3]
    for k, cands in INST.items():
        mejor = None
        for c in cands:
            facts = g.get(c, {}).get("units", {}).get("USD", [])
            q = {}
            for f in facts:
                if "start" in f or f.get("form") not in ("10-Q", "10-K", "10-Q/A", "10-K/A"): continue
                if f["end"] not in q or f["filed"] > q[f["end"]][1]: q[f["end"]] = (f["val"], f["filed"])
            if q and (not mejor or max(q) > max(mejor[1])): mejor = (c, q)
        if mejor:
            usado[k] = mejor[0]
            for e, v in mejor[1].items(): B.setdefault(e, {})[k] = v[0]
    tri = [dict(fin=e, **{k: v for k, v in T[e].items()}) for e in sorted(T)[-12:]]
    for t in tri:
        if t.get("flujo_operativo") is not None and t.get("capex") is not None: t["flujo_libre"] = t["flujo_operativo"] - t["capex"]
    bal = [dict(fin=e, **B[e]) for e in sorted(B)[-6:]]
    return tri, bal, usado


def texto_html(b):
    s = b.decode("utf-8", "replace")
    s = re.sub(r"(?is)<(script|style).*?</\1>", " ", s)
    s = re.sub(r"(?i)</t[dh]>", " | ", s); s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s)).replace("\xa0", " ")
    s = re.sub(r"[ \t]+", " ", s); s = re.sub(r"( ?\| ?)+", " | ", s); s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()


def comunicado(cik, acc):
    base = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-', '')}"
    idx = json.loads(get(base + "/index.json"))["directory"]["item"]
    htm = [i["name"] for i in idx if i["name"].lower().endswith((".htm", ".html", ".txt")) and "index" not in i["name"].lower()]
    ex = [n for n in htm if re.search(r"ex-?99[-_.]?0?1|ex991|exhibit99|dex991|q\d.*(earn|result|release)|press", n.lower())]
    pref = ex or sorted(htm, key=lambda n: -int(next((i.get("size") or 0 for i in idx if i["name"] == n), 0) or 0))
    if not pref: return None, None
    url = f"{base}/{pref[0]}"
    return url, texto_html(get(url))[:200000]


def evento(sub, hoy):
    """Último informe de resultados desde INICIO: 8-K con punto 2.02; si la empresa no publica 8-K de resultados en 120 días, su 10-Q/10-K."""
    r = sub["filings"]["recent"]; filas = [dict(zip(r.keys(), v)) for v in zip(*r.values())]
    k8 = [f for f in filas if f["form"] == "8-K" and "2.02" in (f.get("items") or "")]
    q = [f for f in filas if f["form"] in ("10-Q", "10-K")]
    reciente = [f for f in k8 if (hoy - D(f["filingDate"])).days <= 120]
    if reciente:
        f = max(reciente, key=lambda f: f["filingDate"]); tipo = "8-K 2.02"
    elif q:
        f = max(q, key=lambda f: f["filingDate"]); tipo = f["form"]
    else:
        return None
    if f["filingDate"] < INICIO: return None
    informe = [x for x in q if x["filingDate"] >= f["filingDate"]]
    informe = min(informe, key=lambda x: x["filingDate"]) if informe else None
    return {"tipo": tipo, "fecha": f["filingDate"], "aceptado": f.get("acceptanceDateTime"), "accession": f["accessionNumber"],
            "periodo": (informe or {}).get("reportDate") or f.get("reportDate"), "documento": f.get("primaryDocument"),
            "informe_10q_10k": {"form": informe["form"], "fecha": informe["filingDate"], "accession": informe["accessionNumber"],
                                "periodo": informe["reportDate"]} if informe else None}


def proximas():
    cols = ["earnings_release_next_date", "earnings_release_date", "market_cap_basic", "close", "description"]
    body = json.dumps({"symbols": {"tickers": [e[2] for e in EMPRESAS]}, "columns": cols}).encode()
    try:
        r = urllib.request.urlopen(urllib.request.Request("https://scanner.tradingview.com/america/scan", body,
                                                          {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}), timeout=60)
        return {x["s"]: dict(zip(cols, x["d"])) for x in json.loads(r.read())["data"]}
    except Exception as ex:
        print("TradingView:", ex); return {}


def fecha_ts(v):
    try: return dt.datetime.fromtimestamp(v, dt.timezone.utc).isoformat(timespec="minutes") if v else None
    except Exception: return None


def main():
    out = sys.argv[1]; os.makedirs(out, exist_ok=True); hoy = dt.date.today()
    try:
        tick = {v["ticker"]: v["cik_str"] for v in json.loads(get("https://www.sec.gov/files/company_tickers.json")).values()}
    except Exception:
        tick = {}
    tv = proximas(); cal = {"generado": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "inicio": INICIO, "empresas": [], "errores": []}
    for t, tsec, stv, cik0 in EMPRESAS:
        cik = tick.get(tsec, cik0); fila = {"ticker": t, "cik": cik, "tv": stv}
        x = tv.get(stv, {}); fila.update(proxima=fecha_ts(x.get("earnings_release_next_date")), ultima_tv=fecha_ts(x.get("earnings_release_date")),
                                         cap=x.get("market_cap_basic"), precio=x.get("close"))
        try:
            sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")); fila["nombre_sec"] = sub.get("name")
            ev = evento(sub, hoy); fila["evento"] = ev
            cf = json.loads(get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"))
            tri, bal, usado = series(cf)
            d = os.path.join(out, t); os.makedirs(d, exist_ok=True)
            sec = {"ticker": t, "cik": cik, "nombre": sub.get("name"), "evento": ev, "trimestres": tri, "balance": bal, "conceptos": usado,
                   "fuente": f"SEC EDGAR XBRL companyfacts CIK{cik:010d} (https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json)",
                   "cap_mercado": x.get("market_cap_basic"), "precio": x.get("close"), "cap_fuente": "TradingView", "cap_fecha": cal["generado"]}
            if ev and ev["tipo"] == "8-K 2.02":
                cp = os.path.join(d, f"comunicado-{ev['fecha']}.txt")
                if not os.path.exists(cp):
                    url, txt = comunicado(cik, ev["accession"])
                    if txt: open(cp, "w").write(f"FUENTE: {url}\n\n{txt}")
                    sec["comunicado_url"] = url
                else:
                    sec["comunicado_url"] = open(cp).readline().replace("FUENTE:", "").strip()
                sec["comunicado"] = os.path.basename(cp) if os.path.exists(cp) else None
            json.dump(sec, open(os.path.join(d, "sec.json"), "w"), ensure_ascii=False, indent=1)
            print(t, cik, ev and (ev["tipo"], ev["fecha"], ev["periodo"]), "trimestres", len(tri), tri[-1]["fin"] if tri else None, "próxima", fila["proxima"])
        except Exception as ex:
            cal["errores"].append(f"{t}: {ex}"); print("ERROR", t, ex)
        cal["empresas"].append(fila)
    json.dump(cal, open(os.path.join(out, "calendario.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
