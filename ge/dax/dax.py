"""Cifras del Short diario «DAX am Abend» a partir de dax-<fecha>.json (rama datos-dax-ge).
uso: python3 ge/dax/dax.py <dax.json>  -> imprime JSON: DAX (cierre, día, semana, año, máximo histórico, medias 20/50/200, RSI 14),
amplitud (cuántas de las 40 suben), ganadoras y perdedoras con volumen frente a su media de 10 sesiones, MDAX, TecDAX, Euro Stoxx 50,
EUR/USD y Bund a 10 años. Todo calculado de los datos de TradingView: en pantalla va como «(berechnet)» cuando es cálculo propio."""
import json, sys, datetime as dt, numpy as np

NOMBRES = {"ADS": "Adidas", "AIR": "Airbus", "ALV": "Allianz", "BAS": "BASF", "BAYN": "Bayer", "BEI": "Beiersdorf", "BMW": "BMW",
           "BNR": "Brenntag", "CBK": "Commerzbank", "CON": "Continental", "DB1": "Deutsche Börse", "DBK": "Deutsche Bank", "DHL": "DHL Group",
           "DTE": "Deutsche Telekom", "DTG": "Daimler Truck", "ENR": "Siemens Energy", "EOAN": "Eon", "FRE": "Fresenius", "G1A": "GEA",
           "HEI": "Heidelberg Materials", "HEN3": "Henkel", "HNR1": "Hannover Rück", "IFX": "Infineon", "MBG": "Mercedes-Benz", "MRK": "Merck KGaA",
           "MTX": "MTU Aero Engines", "MUV2": "Münchener Rück", "P911": "Porsche AG", "PAH3": "Porsche SE", "QIA": "Qiagen", "RHM": "Rheinmetall",
           "RWE": "RWE", "SAP": "SAP", "SHL": "Siemens Healthineers", "SIE": "Siemens", "SRT3": "Sartorius", "SY1": "Symrise", "VNA": "Vonovia",
           "VOW3": "Volkswagen", "ZAL": "Zalando", "1COV": "Covestro", "FME": "Fresenius Medical Care", "SHA0": "Schaeffler", "TKA": "Thyssenkrupp"}
CTX = [("XETR:MDAX", "MDAX"), ("XETR:TDXP", "TecDAX"), ("TVC:SX5E", "Euro Stoxx 50"), ("FX:EURUSD", "EUR/USD"), ("TVC:DE10Y", "Bund 10 J. (%)")]


def r(x, d=2):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), d)


def main():
    D = json.load(open(sys.argv[1]))
    V = D["dax_diario"]["velas"]
    c = np.array([v["c"] for v in V], float); h = np.array([v["h"] for v in V], float)
    fechas = [dt.datetime.fromtimestamp(v["t"], dt.timezone.utc).date() for v in V]
    sma = lambda n: c[-n:].mean() if len(c) >= n else None
    dd = np.diff(c); g = np.where(dd > 0, dd, 0); l = np.where(dd < 0, -dd, 0)
    ag, al = g[:14].mean(), l[:14].mean()
    for i in range(14, len(dd)): ag = (ag * 13 + g[i]) / 14; al = (al * 13 + l[i]) / 14
    rsi = 100 - 100 / (1 + ag / al) if al else 100
    ath_i = int(np.argmax(h)); hoy = fechas[-1]
    lunes = hoy - dt.timedelta(days=hoy.weekday())
    i_sem = max(i for i, f in enumerate(fechas) if f < lunes); i_ano = max(i for i, f in enumerate(fechas) if f.year < hoy.year)
    max52 = h[-252:].max(); min52 = np.array([v["l"] for v in V[-252:]]).min()
    out = {"sesion": hoy.isoformat(), "ultima_vela": hoy.isoformat(), "generado": D.get("generado"), "errores": D.get("errores"),
           "dax": {"cierre": r(c[-1]), "dia_pct": r((c[-1] / c[-2] - 1) * 100), "dia_pts": r(c[-1] - c[-2]),
                   "semana_pct": r((c[-1] / c[i_sem] - 1) * 100), "ano_pct": r((c[-1] / c[i_ano] - 1) * 100),
                   "max_historico": r(h[ath_i]), "fecha_max_historico": fechas[ath_i].isoformat(), "dist_max_pct": r((c[-1] / h[ath_i] - 1) * 100),
                   "max_52s": r(max52), "min_52s": r(min52),
                   "sma20": r(sma(20)), "sma50": r(sma(50)), "sma200": r(sma(200)),
                   "dist_sma200_pct": r((c[-1] / sma(200) - 1) * 100) if sma(200) else None, "rsi14": r(rsi, 1),
                   "sesiones_seguidas": None}}
    # racha: sesiones seguidas al alza o a la baja
    s = np.sign(np.diff(c)); n = 1
    while n < len(s) and s[-1 - n] == s[-1]: n += 1
    out["dax"]["sesiones_seguidas"] = int(n * s[-1])
    tv = D.get("tv", {})
    out["contexto"] = {nom: {"cierre": r((tv.get(sym) or {}).get("close"), 4 if "EUR" in nom else 2), "dia_pct": r((tv.get(sym) or {}).get("change")),
                             "dia_abs": r((tv.get(sym) or {}).get("change_abs"), 4 if "EUR" in nom else 3)} for sym, nom in CTX}
    A = []
    for sym, v in (D.get("acciones") or {}).items():
        if v.get("change") is None: continue
        t = sym.split(":")[1]
        rel = (v.get("volume") or 0) / v["average_volume_10d_calc"] if v.get("average_volume_10d_calc") else None
        A.append({"ticker": t, "nombre": NOMBRES.get(t, v.get("description")), "cierre": r(v.get("close")), "dia_pct": r(v.get("change")),
                  "vol_vs_media10": r(rel), "semana_pct": r(v.get("Perf.W")), "ano_pct": r(v.get("Perf.YTD")),
                  "cap_mm_eur": r((v.get("market_cap_basic") or 0) / 1e9, 1), "sector": v.get("sector")})
    A.sort(key=lambda x: x["dia_pct"], reverse=True)
    out["n_acciones"] = len(A); out["origen_acciones"] = D.get("acciones_origen")
    out["suben"] = sum(1 for a in A if a["dia_pct"] > 0); out["bajan"] = sum(1 for a in A if a["dia_pct"] < 0)
    out["ganadoras"] = A[:5]; out["perdedoras"] = A[::-1][:5]
    out["volumen_inusual"] = sorted([a for a in A if a["vol_vs_media10"]], key=lambda a: -a["vol_vs_media10"])[:5]
    out["mayores"] = sorted(A, key=lambda a: -(a["cap_mm_eur"] or 0))[:6]
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
