"""Indicadores de FTSE ADX General (FADGI) y DFM General (DFMGI) a partir de datos/mercado-<fecha>.json.
Lo usan make_video.py, make_short.py y gen_meta.py, y sirve para escribir el guion.
uso: python3 tecnico.py <mercado.json>  -> imprime JSON con cierre, medias, RSI, estocástico, niveles, volumen y valores."""
import json, sys, datetime as dt, numpy as np

TZ = dt.timezone(dt.timedelta(hours=4))  # hora de EAU (sin horario de verano)
INDICE = {"adx": "فوتسي سوق أبوظبي العام", "dfm": "مؤشر سوق دبي المالي العام"}
INDICE_CORTO = {"adx": "مؤشر أبوظبي", "dfm": "مؤشر دبي"}
MERCADO = {"ADX": "سوق أبوظبي", "DFM": "سوق دبي"}
MESES = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
DIAS = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
# Nombres en árabe de las cotizadas más negociadas (el video.json del día puede añadir más en "nombres").
NOMBRES = {"IHC": "العالمية القابضة", "ADNOCGAS": "أدنوك للغاز", "FAB": "بنك أبوظبي الأول", "ETISALAT": "إي آند", "ADCB": "بنك أبوظبي التجاري",
           "ADNOCDRILL": "أدنوك للحفر", "ADIB": "مصرف أبوظبي الإسلامي", "ALPHADHABI": "ألفا ظبي", "BOROUGE": "بروج", "2POINTZERO": "2 بوينت زيرو",
           "ALDAR": "الدار العقارية", "ADNOCLS": "أدنوك للإمداد والخدمات", "ADNOCDIST": "أدنوك للتوزيع", "TAQA": "طاقة", "PUREHEALTH": "بيورهيلث",
           "MODON": "مدن القابضة", "AGTHIA": "أغذية", "PRESIGHT": "بريسايت", "BURJEEL": "برجيل القابضة", "ESHRAQ": "إشراق للاستثمار",
           "INB": "بنك الاستثمار", "MANAZEL": "منازل", "WAHA": "وها كابيتال", "ASM": "السير البحرية", "SIB": "مصرف الشارقة الإسلامي",
           "EMIRATESNBD": "الإمارات دبي الوطني", "DEWA": "ديوا", "EMAAR": "إعمار العقارية", "MASQ": "بنك المشرق", "DU": "دو",
           "EMAARDEV": "إعمار للتطوير", "DIB": "بنك دبي الإسلامي", "SALIK": "سالك", "CBD": "بنك دبي التجاري", "TALABAT": "طلبات",
           "AIRARABIA": "العربية للطيران", "PARKIN": "باركن", "AMLAK": "أملاك للتمويل", "SALAMA": "سلامة للتأمين", "AMAN": "دبي الإسلامية للتأمين (أمان)",
           "GFH": "مجموعة جي إف إتش", "DSI": "دريك آند سكل", "ETIHADENERGY": "الاتحاد للطاقة", "DUBAIRESI": "دبي ريزيدنشال ريت", "EMPOWER": "إمباور",
           "AMANAT": "أمانات القابضة", "TECOM": "تيكوم", "DFM": "سوق دبي المالي", "UPP": "اتحاد العقارية", "DEYAAR": "ديار", "SHUAA": "شعاع كابيتال"}
MIN_VALOR = 1e6  # solo valores con más de 1 millón de dírhams negociados en la sesión (evita saltos de valores sin liquidez)


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
    ex = k.upper(); acc = [v for v in D.get("acciones", {}).values() if v.get("exchange") == ex and de_hoy(D, v)]
    if not np.isnan(vol[-1]) and np.isfinite(vol[-11:-1]).all():
        vr = vol[-1] / vol[-11:-1].mean() * 100 - 100; vfuente = "índice"
    else:
        hoy = sum(v["volume"] or 0 for v in acc); med = sum(v["average_volume_10d_calc"] or 0 for v in acc)
        vr = hoy / med * 100 - 100 if med else None; vfuente = "suma de acciones"
    sem = [i for i, d in enumerate(dates) if d <= dates[-1] - dt.timedelta(days=dates[-1].weekday() + 1)]
    ult_bajo = max([i for i in range(len(c) - 1) if c[i] <= c[-1]], default=None)
    ult_alto = max([i for i in range(len(c) - 1) if c[i] >= c[-1]], default=None)
    # panel técnico: rendimiento, cruce de medias, posición en el rango de 52 semanas y distancia a los niveles (calculado)
    def perf(dias):
        j = max([i for i, d in enumerate(dates) if d <= dates[-1] - dt.timedelta(days=dias)], default=None)
        return None if j is None else round(float(c[-1] / c[j] * 100 - 100), 2)
    jy = max([i for i, d in enumerate(dates) if d.year < dates[-1].year], default=None)
    dif = S50 - S200; cr = [i for i in range(1, len(c)) if np.isfinite(dif[i - 1]) and np.sign(dif[i]) != np.sign(dif[i - 1]) and dif[i] != 0]
    cruce = None if not cr else {"tipo": "dorado" if dif[cr[-1]] > 0 else "muerte", "fecha": dates[cr[-1]].isoformat()}
    res = [l["valor"] for l in niveles if l["tipo"] == "res"]; sop = [l["valor"] for l in niveles if l["tipo"] == "sop"]
    extra = dict(perf_1m=perf(30), perf_3m=perf(91), perf_ytd=None if jy is None else round(float(c[-1] / c[jy] * 100 - 100), 2),
                 sma50_sobre_sma200=bool(dif[-1] > 0), cruce=cruce,
                 pos_52s_pct=round(float((c[-1] - lo[i_lo]) / (hi[i_hi] - lo[i_lo]) * 100), 1),
                 dist_max_52s_pct=round(float(c[-1] / hi[i_hi] * 100 - 100), 2), dist_min_52s_pct=round(float(c[-1] / lo[i_lo] * 100 - 100), 2),
                 res_cercana=min(res) if res else None, dist_res_pct=round(float(min(res) / c[-1] * 100 - 100), 2) if res else None,
                 sop_cercano=max(sop) if sop else None, dist_sop_pct=round(float(max(sop) / c[-1] * 100 - 100), 2) if sop else None,
                 rsi_zona="sobrecompra" if RSI[-1] >= 70 else "sobreventa" if RSI[-1] <= 30 else "neutral",
                 estoc_zona="sobrecompra" if K[-1] >= 80 else "sobreventa" if K[-1] <= 20 else "neutral",
                 estoc_cruce="K>D" if K[-1] > Dl[-1] else "K<D")
    return dict(**extra, fecha=dates[-1].isoformat(), cierre=round(float(c[-1]), 2), anterior=round(float(c[-2]), 2),
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
                valor_negociado_aed=round(sum(v.get("Value.Traded") or 0 for v in acc)),
                suben=sum(1 for v in acc if (v.get("change") or 0) > 0), bajan=sum(1 for v in acc if (v.get("change") or 0) < 0),
                sin_cambio=sum(1 for v in acc if v.get("change") == 0), niveles=niveles), \
        dict(dates=dates, o=o, hi=hi, lo=lo, c=c, vol=vol, S50=S50, S200=S200, RSI=RSI, K=K, D=Dl)


def de_hoy(D, v):
    """True si la cotización es de la sesión del día (los valores sin negociación conservan la variación de su último día)."""
    if not v.get("time") or not D.get("sesion"):
        return True
    return dt.datetime.fromtimestamp(v["time"], TZ).date().isoformat() == D["sesion"]


def movers(D, extra=None):
    nom = dict(NOMBRES, **(extra or {}))
    L = sorted([(v["change"], k.split(":")[1], v["exchange"]) for k, v in D.get("acciones", {}).items()
                if v.get("change") is not None and (v.get("Value.Traded") or 0) >= MIN_VALOR and de_hoy(D, v)])
    f = lambda x: {"ticker": x[1], "mercado": x[2], "nombre": nom.get(x[1], x[1]), "cambio": round(x[0], 2)}
    return [f(x) for x in L[::-1][:5]], [f(x) for x in L[:5]]


def calc(D, extra=None):
    R = {k: calc_indice(D, k) for k in ("adx", "dfm")}
    A = {k: R[k][1] for k in R}; R = {k: R[k][0] for k in R}
    R["mejores"], R["peores"] = movers(D, extra)
    R["fecha"] = R["adx"]["fecha"]
    R["contexto"] = {k: {"close": v.get("close"), "change": None if v.get("change") is None else round(v["change"], 2)} for k, v in D.get("tv", {}).items()}
    return R, A


if __name__ == "__main__":
    r, _ = calc(json.load(open(sys.argv[1])))
    print(json.dumps(r, ensure_ascii=False, indent=1))
