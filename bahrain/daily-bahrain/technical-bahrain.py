"""Indicators of the Bahrain All Share Index (BAHRAIN:BHBX) from data/market-<date>-bahrain.json.
Used by make-video-bahrain.py, make-short-bahrain.py and make-meta-bahrain.py, and to write the script.
usage: python3 technical-bahrain.py <market.json>  -> prints JSON with close, averages, RSI, stochastic, levels, volume, movers and context."""
import json, sys, datetime as dt, numpy as np

TZ = dt.timezone(dt.timedelta(hours=3))  # Manama time (no DST)
INDICE = {"bax": "مؤشر البحرين العام"}
INDICE_CORTO = {"bax": "المؤشر العام"}
BHD_USD = 0.376  # official peg: 1 US dollar = 0.376 Bahraini dinar (for stocks quoted in USD)
MESES = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
DIAS = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
# Arabic names of Bahrain Bourse listed companies by ticker (the day's video-bahrain.json can add more under "nombres").
NOMBRES = {"ALBH": "ألمنيوم البحرين (ألبا)", "NBB": "بنك البحرين الوطني", "BBK": "بنك البحرين والكويت", "BEYON": "بيون", "GFH": "مجموعة جي إف إتش المالية",
           "SALAM": "مصرف السلام", "ABC": "بنك ABC", "ITHMR": "بنك إثمار", "BARKA": "مجموعة البركة", "KHCB": "بيت التمويل الخليجي",
           "BISB": "بنك البحرين الإسلامي", "INOVEST": "إنوفست", "ESTERAD": "استيراد", "BMB": "البحرين لمطاحن الدقيق", "BKIC": "البحرين الكويتية للتأمين",
           "SEEF": "عقارات السيف", "APMTB": "إيه بي إم ترمينالز البحرين", "BCFC": "البحرين للسينما", "NASS": "مجموعة ناس", "ZAINBH": "زين البحرين",
           "SOLID": "سوليدرتي البحرين", "TAKAFUL": "تكافل الدولية", "BNH": "البحرين الوطنية القابضة", "BTC": "البحرين للتسهيلات التجارية",
           "BFC": "مجموعة بي إف سي", "DUTYF": "البحرين للأسواق الحرة", "TRAFCO": "مجموعة ترافكو", "DELMON": "دلمون للدواجن", "POLTRY": "دلمون للدواجن",
           "BMMI": "بي إم إم آي", "GHG": "مجموعة الخليج الفندقية", "BANADER": "بنادر للفنادق", "NHOTEL": "الفنادق الوطنية", "BSPC": "البحرين للسياحة",
           "CPARK": "البحرين لمواقف السيارات", "SICO": "سيكو", "ARIG": "المجموعة العربية للتأمين", "KFH": "بيت التمويل الكويتي", "AUB": "البنك الأهلي المتحد",
           "BBKSC": "بنك البحرين والكويت", "UGB": "بنك الخليج المتحد", "NIH": "الوطنية للتأمين", "BMBOR": "البحرين لمطاحن الدقيق", "ALSALAM": "مصرف السلام",
           "IIB": "بنك إثمار", "GIC": "الخليجية للاستثمار", "BBPB": "البحرين للتسهيلات التجارية", "MHHP": "مركز مطار البحرين"}
MIN_VALOR = 5000  # only stocks with more than 5,000 Bahraini dinars traded in the session (avoids jumps in illiquid stocks)


def fecha_ar(d, dia=True):
    return (DIAS[d.weekday()] + " " if dia else "") + f"{d.day} {MESES[d.month - 1]} {d.year}"


def velas(D, k):
    V = D[f"{k}_diario"]["velas"]
    dates = [dt.datetime.fromtimestamp(v["t"], TZ).date() for v in V]
    o, hi, lo, c = (np.array([v[x] for v in V], float) for x in "ohlc")
    vol = np.array([v["v"] if v.get("v") is not None else np.nan for v in V], float)
    return dates, o, hi, lo, c, vol


def calc_indice(D, k):
    dates, o, hi, lo, c, vol = velas(D, k)
    sma = lambda n: np.array([c[max(0, i - n + 1):i + 1].mean() if i >= n - 1 else np.nan for i in range(len(c))])
    S50, S200 = sma(50), sma(200)
    dd = np.diff(c); g = np.where(dd > 0, dd, 0); ls = np.where(dd < 0, -dd, 0); RSI = [np.nan] * 15
    ag, al = g[:14].mean(), ls[:14].mean()
    for i in range(14, len(dd)):
        ag = (ag * 13 + g[i]) / 14; al = (al * 13 + ls[i]) / 14; RSI.append(100 - 100 / (1 + ag / al) if al else 100.0)
    RSI = np.array(RSI[:len(c)])
    fk = np.array([np.nan] * 13 + [(c[i] - lo[i - 13:i + 1].min()) / (hi[i - 13:i + 1].max() - lo[i - 13:i + 1].min()) * 100 for i in range(13, len(c))])
    roll = lambda a, n: np.array([np.mean(a[i - n + 1:i + 1]) if i >= n - 1 and not np.isnan(a[i - n + 1:i + 1]).any() else np.nan for i in range(len(a))])
    K = roll(fk, 3); Dl = roll(K, 3)
    y1 = [i for i, d in enumerate(dates) if d > dates[-1] - dt.timedelta(days=365)]
    i_hi = y1[0] + int(np.argmax(hi[y1])); i_lo = y1[0] + int(np.argmin(lo[y1]))
    # niveles: máximos y mínimos de las últimas 5 y 30 sesiones y de 52 semanas (por encima = resistencia, por debajo = soporte)
    lv = []
    for n in (5, 30):
        j = len(c) - n + int(np.argmax(hi[-n:])); lv.append(("res", float(hi[j]), dates[j]))
        j = len(c) - n + int(np.argmin(lo[-n:])); lv.append(("sop", float(lo[j]), dates[j]))
    lv += [("res", float(hi[i_hi]), dates[i_hi]), ("sop", float(lo[i_lo]), dates[i_lo])]
    seen, niveles = set(), []
    for t, v, d in lv:
        if round(v) in seen or (t == "res" and v <= c[-1]) or (t == "sop" and v >= c[-1]): continue
        seen.add(round(v)); niveles.append({"tipo": t, "valor": round(v, 2), "fecha": d.isoformat()})
    # volumen: el de la vela del índice si lo hay (ADX); si no (DFM), la suma de las acciones del mercado (calculado)
    acc = acciones(D, k, dates[-1])
    if not np.isnan(vol[-1]) and np.isfinite(vol[-11:-1]).all():
        vr = vol[-1] / vol[-11:-1].mean() * 100 - 100; vfuente = "índice"
    else:
        hoy = sum(v["volume"] or 0 for v in acc); med = sum(v["average_volume_10d_calc"] or 0 for v in acc)
        vr = hoy / med * 100 - 100 if med else None; vfuente = "suma de acciones"
    sem = [i for i, d in enumerate(dates) if d <= dates[-1] - dt.timedelta(days=(dates[-1].weekday() + 1) % 7 + 1)]  # Bahrain Bourse week: Sunday to Thursday
    ult_bajo = max([i for i in range(len(c) - 1) if c[i] <= c[-1]], default=None)
    ult_alto = max([i for i in range(len(c) - 1) if c[i] >= c[-1]], default=None)
    return dict(fecha=dates[-1].isoformat(), cierre=round(float(c[-1]), 2), anterior=round(float(c[-2]), 2),
                var_pct=round(float(c[-1] / c[-2] * 100 - 100), 2), var_pts=round(float(c[-1] - c[-2]), 2),
                semana_pct=round(float(c[-1] / c[sem[-1]] * 100 - 100), 2) if sem else None, cierre_semana_anterior=round(float(c[sem[-1]]), 2) if sem else None,
                max_dia=round(float(hi[-1]), 2), min_dia=round(float(lo[-1]), 2),
                sma50=round(float(S50[-1]), 2), sma200=round(float(S200[-1]), 2),
                dist_sma50_pct=round(float(c[-1] / S50[-1] * 100 - 100), 2), dist_sma200_pct=round(float(c[-1] / S200[-1] * 100 - 100), 2),
                rsi14=round(float(RSI[-1]), 1), estoc_k=round(float(K[-1]), 1), estoc_d=round(float(Dl[-1]), 1),
                estoc_k_prev=round(float(K[-2]), 1), estoc_d_prev=round(float(Dl[-2]), 1),
                max_52s=round(float(hi[i_hi]), 2), max_52s_fecha=dates[i_hi].isoformat(), min_52s=round(float(lo[i_lo]), 2), min_52s_fecha=dates[i_lo].isoformat(),
                cierre_mas_bajo_desde=dates[ult_bajo].isoformat() if ult_bajo is not None else None,
                cierre_mas_alto_desde=dates[ult_alto].isoformat() if ult_alto is not None else None,
                volumen_vs_media10_pct=None if vr is None else round(float(vr), 1), volumen_fuente=vfuente,
                valor_negociado_bhd=round(sum(valor_bhd(v) for v in acc)), negociadas=len(acc),
                suben=sum(1 for v in acc if (v.get("change") or 0) > 0), bajan=sum(1 for v in acc if (v.get("change") or 0) < 0),
                sin_cambio=sum(1 for v in acc if v.get("change") == 0), niveles=niveles), \
        dict(dates=dates, o=o, hi=hi, lo=lo, c=c, S50=S50, S200=S200, RSI=RSI, K=K, D=Dl)


def valor_bhd(v):
    """Traded value in Bahraini dinars (stocks quoted in US dollars are converted at the peg)."""
    x = v.get("Value.Traded") or 0
    return x * BHD_USD if v.get("currency") == "USD" else x


def acciones(D, k="bax", fecha=None):
    """Common stocks of the Bahrain All Share Index (TradingView field indexes). With fecha, only those that traded that day."""
    en_idx = lambda v: any(i.get("proname") == "BAHRAIN:BHBX" for i in (v.get("indexes") or []))
    comun = lambda v: v.get("typespecs") in (None, [], ["common"]) or "common" in (v.get("typespecs") or [])
    hoy = lambda v: fecha is None or (v.get("time") and dt.datetime.fromtimestamp(v["time"], TZ).date() == fecha)
    return [dict(v, ticker=t.split(":")[1]) for t, v in D.get("acciones", {}).items() if comun(v) and en_idx(v) and hoy(v)]


def movers(D, fecha, extra=None):
    """5 biggest gainers and 5 biggest losers of the All Share Index that traded that day with more than MIN_VALOR dinars."""
    nom = dict(NOMBRES, **(extra or {}))
    L = sorted([(v["change"], v["ticker"], v.get("description")) for v in acciones(D, "bax", fecha)
                if v.get("change") is not None and valor_bhd(v) >= MIN_VALOR])
    f = lambda x: {"ticker": x[1], "nombre": nom.get(x[1], x[2]), "nombre_en": x[2], "cambio": round(x[0], 2)}
    up = [f(x) for x in L[::-1] if x[0] > 0][:5]; dn = [f(x) for x in L if x[0] < 0][:5]
    return up, dn


# Context: Gulf and Asian markets on the same day; Wall Street, Europe, Brent and gold with their last close before Bahrain Bourse
# closes (the previous day's), which is the one that reaches the Bahrain session.
MISMO_DIA = {"ADX:FADGI", "DFM:DFMGI", "QSE:GNRI", "TADAWUL:TASI", "TVC:NI225", "TVC:HSI", "TVC:KOSPI", "SSE:000001", "KSE:BKP", "MSM:MSX30"}


def contexto(D, fecha):
    out = {}
    for sym, V in D.get("ctx_velas", {}).items():
        rows = [(dt.datetime.fromtimestamp(v["t"], dt.timezone.utc).date(), v["c"]) for v in V]
        idx = [i for i, (d, _) in enumerate(rows) if (d == fecha if sym in MISMO_DIA else d < fecha)]
        if not idx or idx[-1] == 0: continue
        i = idx[-1]; out[sym] = {"fecha": rows[i][0].isoformat(), "close": rows[i][1], "change": round(rows[i][1] / rows[i - 1][1] * 100 - 100, 2)}
    return out


def calc(D, extra=None):
    R = {"bax": calc_indice(D, "bax")}
    A = {k: R[k][1] for k in R}; R = {k: R[k][0] for k in R}
    R["fecha"] = R["bax"]["fecha"]; f = dt.date.fromisoformat(R["fecha"])
    R["mejores"], R["peores"] = movers(D, f, extra)
    R["activos"] = [{"ticker": v["ticker"], "nombre": dict(NOMBRES, **(extra or {})).get(v["ticker"], v.get("description")), "valor_bhd": round(valor_bhd(v)),
                     "cambio": round(v.get("change") or 0, 2)} for v in sorted(acciones(D, "bax", f), key=valor_bhd, reverse=True)[:5]]
    R["contexto"] = contexto(D, f)
    return R, A


if __name__ == "__main__":
    r, _ = calc(json.load(open(sys.argv[1])))
    print(json.dumps(r, ensure_ascii=False, indent=1))
