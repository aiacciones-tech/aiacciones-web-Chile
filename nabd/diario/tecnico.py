"""Indicadores de Wall Street (S&P 500 como índice principal; Nasdaq Composite, Dow Jones y Russell 2000 como acompañantes)
a partir de datos/mercado-<fecha>.json. Lo usan make_video.py, make_short.py y gen_meta.py, y sirve para escribir el guion.
uso: python3 tecnico.py <mercado.json>  -> imprime JSON con cierres, medias, RSI, estocástico, niveles, volumen, valores y contexto."""
import json, re, sys, datetime as dt, numpy as np
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")
RIAD = dt.timezone(dt.timedelta(hours=3))  # hora del Golfo (Riad, Kuwait, Doha, Manama); Dubái y Mascate son una hora más
TZ = RIAD
CLAVES = ("spx", "ndq", "dji", "rut", "ndx")
INDICE = {"spx": "مؤشر إس آند بي 500", "ndq": "مؤشر ناسداك المركب", "dji": "مؤشر داو جونز الصناعي", "rut": "مؤشر راسل 2000", "ndx": "مؤشر ناسداك 100"}
INDICE_CORTO = {"spx": "إس آند بي 500", "ndq": "ناسداك", "dji": "داو جونز", "rut": "راسل 2000", "ndx": "ناسداك 100"}
SIMBOLO = {"spx": "SP:SPX", "ndq": "NASDAQ:IXIC", "dji": "DJ:DJI", "rut": "TVC:RUT", "ndx": "NASDAQ:NDX"}
# ETF sectoriales SPDR del manual de producción (10-nov-2026)
SECTORES = {"AMEX:XLK": "التكنولوجيا", "AMEX:XLF": "المال", "AMEX:XLE": "الطاقة", "AMEX:XLV": "الرعاية الصحية",
            "AMEX:XLY": "السلع الاستهلاكية الكمالية", "AMEX:XLI": "الصناعة"}
# Indicadores macro del manual: (símbolo, nombre, unidad); el bono va en rendimiento (%) y su cambio en puntos básicos
MACRO = [("TVC:US10Y", "عائد 10 سنوات", "%"), ("TVC:DXY", "الدولار DXY", ""), ("TVC:VIX", "التقلب VIX", ""),
         ("TVC:USOIL", "النفط WTI", "دولار"), ("TVC:GOLD", "الذهب", "دولار")]
MESES = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
DIAS = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
# Nombres en árabe de las grandes empresas del S&P 500 por ticker (el video.json del día puede añadir más en "nombres").
NOMBRES = {"AAPL": "أبل", "NVDA": "إنفيديا", "MSFT": "مايكروسوفت", "GOOGL": "ألفابت (غوغل)", "GOOG": "ألفابت (غوغل)", "AMZN": "أمازون",
           "META": "ميتا", "TSLA": "تسلا", "AVGO": "برودكوم", "LLY": "إيلي ليلي", "WMT": "وولمارت", "JPM": "جي بي مورغان", "V": "فيزا",
           "MU": "مايكرون", "AMD": "إيه إم دي", "XOM": "إكسون موبيل", "JNJ": "جونسون آند جونسون", "MA": "ماستركارد", "ABBV": "آبفي",
           "COST": "كوستكو", "CVX": "شيفرون", "KO": "كوكاكولا", "PLTR": "بالانتير", "PG": "بروكتر آند غامبل", "CSCO": "سيسكو", "MRK": "ميرك",
           "UNH": "يونايتد هيلث", "ORCL": "أوراكل", "HD": "هوم ديبوت", "BAC": "بنك أوف أمريكا", "GE": "جنرال إلكتريك للطيران",
           "PM": "فيليب موريس", "INTC": "إنتل", "MS": "مورغان ستانلي", "AMAT": "أبلايد ماتيريالز", "NFLX": "نتفليكس", "TMO": "ثيرمو فيشر",
           "PANW": "بالو ألتو نتوركس", "CAT": "كاتربيلر", "RTX": "آر تي إكس", "TXN": "تكساس إنسترومنتس", "WFC": "ويلز فارغو",
           "LRCX": "لام ريسيرش", "GS": "غولدمان ساكس", "AMGN": "أمجن", "LIN": "ليندي", "IBM": "آي بي إم", "CRWD": "كراودسترايك",
           "ANET": "أريستا نتوركس", "AXP": "أمريكان إكسبريس", "DELL": "ديل", "GILD": "جلعاد", "GEV": "جي إي فيرنوفا", "DIS": "ديزني",
           "C": "سيتي غروب", "MCD": "ماكدونالدز", "PEP": "بيبسيكو", "BLK": "بلاك روك", "ABT": "أبوت", "VZ": "فيرايزون", "APH": "أمفينول",
           "NEE": "نكست إيرا إنرجي", "DE": "دير", "KLAC": "كيه إل إيه", "QCOM": "كوالكوم", "ADI": "أنالوج ديفايسز", "CRM": "سيلزفورس",
           "UNP": "يونيون باسيفيك", "TMUS": "تي موبايل", "PFE": "فايزر", "BA": "بوينغ", "NKE": "نايكي", "SBUX": "ستاربكس", "UBER": "أوبر",
           "ABNB": "إير بي إن بي", "APP": "آب لوفين", "VST": "فيسترا", "COHR": "كوهيرنت", "AXON": "أكسون", "MCHP": "مايكروتشيب",
           "CHTR": "تشارتر", "PODD": "إنسوليت", "DXCM": "ديكسكوم", "SMCI": "سوبر مايكرو", "ADBE": "أدوبي", "NOW": "سيرفس ناو",
           "INTU": "إنتويت", "PYPL": "باي بال", "SCHW": "تشارلز شواب", "COIN": "كوينبيس", "HOOD": "روبن هود", "SPGI": "إس آند بي غلوبال",
           "HON": "هانيويل", "TRV": "ترافلرز", "SHW": "شيروين ويليامز", "MMM": "ثري إم", "MPWR": "مونوليثيك باور", "TER": "تيرادين",
           "FSLR": "فيرست سولار", "TTWO": "تيك-تو", "AKAM": "أكاماي", "SPCX": "سبيس إكس"}
SECTOR_AR = {"Electronic Technology": "التكنولوجيا الإلكترونية", "Technology Services": "خدمات التكنولوجيا", "Finance": "المال",
             "Health Technology": "التكنولوجيا الصحية", "Retail Trade": "التجزئة", "Consumer Non-Durables": "السلع الاستهلاكية غير المعمرة",
             "Producer Manufacturing": "التصنيع", "Energy Minerals": "الطاقة", "Consumer Services": "الخدمات الاستهلاكية", "Consumer Durables": "السلع المعمرة",
             "Utilities": "المرافق", "Non-Energy Minerals": "المعادن", "Industrial Services": "الخدمات الصناعية", "Transportation": "النقل",
             "Commercial Services": "الخدمات التجارية", "Process Industries": "الصناعات التحويلية", "Communications": "الاتصالات",
             "Health Services": "الخدمات الصحية", "Distribution Services": "التوزيع", "Miscellaneous": "متنوع"}
MIN_VALOR = 50e6  # solo valores con más de 50 millones de dólares negociados en la sesión


def fecha_ar(d, dia=True):
    return (DIAS[d.weekday()] + " " if dia else "") + f"{d.day} {MESES[d.month - 1]} {d.year}"


def fecha_vela(t):
    """Fecha de la sesión de una vela diaria. +6 h: las velas de futuros (petróleo, oro, dólar) empiezan a las 22:00-23:00 UTC del día anterior
    (18:00 en Nueva York) y son de la sesión del día siguiente; las de acciones e índices (13:30-14:30 UTC) y las de 00:00 UTC no cambian de día."""
    return (dt.datetime.fromtimestamp(t, dt.timezone.utc) + dt.timedelta(hours=6)).date()


def nombre_en(desc):
    """'Apple Inc.' -> 'Apple'; 'Alphabet Inc. Class A' -> 'Alphabet'."""
    s = re.sub(r"\s+(Class [A-Z]|Common Stock|Ordinary Shares).*$", "", desc or "")
    s = re.sub(r",?\s+(Inc\.?|Incorporated|Corporation|Corp\.?|Company|Co\.|Holdings|Group|plc|Ltd\.?|N\.V\.|& Co\.?)$", "", s)
    s = re.sub(r",?\s+(Inc\.?|Incorporated|Corporation|Corp\.?|Company|Holdings|plc)$", "", s)
    return s.strip()


def velas(D, k):
    V = D[f"{k}_diario"]["velas"]
    dates = [fecha_vela(v["t"]) for v in V]
    o, hi, lo, c = (np.array([v[x] for v in V], float) for x in "ohlc")
    vol = np.array([v["v"] if v.get("v") is not None else np.nan for v in V], float)
    return dates, o, hi, lo, c, vol


def calc_indice(D, k):
    dates, o, hi, lo, c, vol = velas(D, k)
    sma = lambda n: np.array([c[max(0, i - n + 1):i + 1].mean() if i >= n - 1 else np.nan for i in range(len(c))])
    S20, S50, S200 = sma(20), sma(50), sma(200)
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
    vr = vol[-1] / vol[-11:-1].mean() * 100 - 100 if not np.isnan(vol[-1]) and np.isfinite(vol[-11:-1]).all() else None
    lunes = dates[-1] - dt.timedelta(days=dates[-1].weekday())
    sem = [i for i, d in enumerate(dates) if d < lunes]  # semana de Nueva York: lunes a viernes
    ult_bajo = max([i for i in range(len(c) - 1) if c[i] <= c[-1]], default=None)
    ult_alto = max([i for i in range(len(c) - 1) if c[i] >= c[-1]], default=None)
    ano = [i for i, d in enumerate(dates) if d.year < dates[-1].year]
    r = dict(fecha=dates[-1].isoformat(), cierre=round(float(c[-1]), 2), anterior=round(float(c[-2]), 2),
             var_pct=round(float(c[-1] / c[-2] * 100 - 100), 2), var_pts=round(float(c[-1] - c[-2]), 2),
             semana_pct=round(float(c[-1] / c[sem[-1]] * 100 - 100), 2) if sem else None, cierre_semana_anterior=round(float(c[sem[-1]]), 2) if sem else None,
             ano_pct=round(float(c[-1] / c[ano[-1]] * 100 - 100), 2) if ano else None,
             max_dia=round(float(hi[-1]), 2), min_dia=round(float(lo[-1]), 2),
             sma50=round(float(S50[-1]), 2), sma200=round(float(S200[-1]), 2),
             dist_sma50_pct=round(float(c[-1] / S50[-1] * 100 - 100), 2), dist_sma200_pct=round(float(c[-1] / S200[-1] * 100 - 100), 2),
             rsi14=round(float(RSI[-1]), 1), estoc_k=round(float(K[-1]), 1), estoc_d=round(float(Dl[-1]), 1),
             estoc_k_prev=round(float(K[-2]), 1), estoc_d_prev=round(float(Dl[-2]), 1),
             max_52s=round(float(hi[i_hi]), 2), max_52s_fecha=dates[i_hi].isoformat(), min_52s=round(float(lo[i_lo]), 2), min_52s_fecha=dates[i_lo].isoformat(),
             dist_max_52s_pct=round(float(c[-1] / hi[i_hi] * 100 - 100), 2),
             cierre_mas_bajo_desde=dates[ult_bajo].isoformat() if ult_bajo is not None else None,
             cierre_mas_alto_desde=dates[ult_alto].isoformat() if ult_alto is not None else None,
             volumen_vs_media10_pct=None if vr is None else round(float(vr), 1), niveles=niveles,
             sma20=round(float(S20[-1]), 2), dist_sma20_pct=round(float(c[-1] / S20[-1] * 100 - 100), 2),
             volumen=None if np.isnan(vol[-1]) else float(vol[-1]), sesiones=len(c), historia_desde=dates[0].isoformat())
    i_ath = int(np.argmax(hi))  # máximo de toda la historia descargada (desde historia_desde)
    r.update(max_hist=round(float(hi[i_ath]), 2), max_hist_fecha=dates[i_ath].isoformat(), dist_max_hist_pct=round(float(c[-1] / hi[i_ath] * 100 - 100), 2),
             # Es el máximo histórico si los datos empiezan antes de 2007, o si supera en más de un 50% el máximo del primer año de datos
             # (para los índices de EE. UU., cuyos máximos anteriores a 2016 quedan muy por debajo de los actuales).
             max_hist_es_historico=bool(dates[0] <= dt.date(2007, 1, 1) or hi[i_ath] > 1.5 * hi[:250].max()))
    r["tendencia"] = tendencia(r)
    r["escenarios"] = escenarios(r)
    if k == "spx":
        acc = acciones(D)
        r.update(suben=sum(1 for v in acc if (v.get("change") or 0) > 0), bajan=sum(1 for v in acc if (v.get("change") or 0) < 0),
                 sin_cambio=sum(1 for v in acc if v.get("change") == 0), valor_negociado_usd=round(sum(v.get("Value.Traded") or 0 for v in acc)))
    return r, dict(dates=dates, o=o, hi=hi, lo=lo, c=c, vol=vol, S20=S20, S50=S50, S200=S200, RSI=RSI, K=K, D=Dl)


def tendencia(r):
    """Tendencia general por la posición del cierre frente a las medias (cálculo propio, no una previsión)."""
    c, a, b, d = r["cierre"], r["sma20"], r["sma50"], r["sma200"]
    if c > b > d: return "صاعد" if c > a else "صاعد مع تراجع"
    if c < b < d: return "هابط" if c < a else "هابط مع ارتداد"
    return "عرضي" if c >= d else "دون متوسط 200"


def escenarios(r):
    """Tres escenarios con niveles calculados (máximos/mínimos recientes y de 52 semanas, y medias de 20, 50 y 200 sesiones):
    alcista = cierres por encima de la primera y la segunda resistencia; neutral = rango entre el primer soporte y la primera resistencia;
    bajista = cierres por debajo del primer y el segundo soporte. Son condiciones, no previsiones."""
    c = r["cierre"]
    L = [(l["valor"], {"res": "قمة", "sop": "قاع"}[l["tipo"]] + " " + l["fecha"]) for l in r["niveles"]]
    L += [(r["sma20"], "متوسط 20 جلسة"), (r["sma50"], "متوسط 50 جلسة"), (r["sma200"], "متوسط 200 جلسة")]
    if r.get("max_52s"): L.append((r["max_52s"], "أعلى مستوى في 52 أسبوعًا"))
    if r.get("min_52s"): L.append((r["min_52s"], "أدنى مستوى في 52 أسبوعًا"))
    arriba = sorted({round(v, 2): e for v, e in L if v > c * 1.001}.items())
    abajo = sorted({round(v, 2): e for v, e in L if v < c * 0.999}.items(), reverse=True)
    # niveles separados al menos un 0,4% entre sí, para que el escenario tenga dos escalones distintos
    sep = lambda X: [x for i, x in enumerate(X) if i == 0 or abs(x[0] / X[i - 1][0] - 1) > 0.004]
    arriba, abajo = sep(arriba)[:2], sep(abajo)[:2]
    f = lambda x: {"valor": x[0], "et": x[1], "dist_pct": round(x[0] / c * 100 - 100, 2)}
    return {"alcista": [f(x) for x in arriba], "bajista": [f(x) for x in abajo],
            "neutral": [f(abajo[0]), f(arriba[0])] if arriba and abajo else []}


def sectores(D):
    """ETF sectoriales: cambio del día y de la semana (TradingView), ordenados de mejor a peor."""
    out = []
    for sym, nom in SECTORES.items():
        v = (D.get("tv") or {}).get(sym)
        if not v or v.get("change") is None: continue
        out.append({"simbolo": sym.split(":")[1], "nombre": nom, "cierre": round(v["close"], 2), "cambio": round(v["change"], 2),
                    "semana": None if v.get("Perf.W") is None else round(v["Perf.W"], 2), "mes": None if v.get("Perf.1M") is None else round(v["Perf.1M"], 2)})
    return sorted(out, key=lambda x: -x["cambio"])


def macro(D, fecha):
    """Bono a 10 años, DXY, VIX, WTI y oro: cierre, cambio del día (el bono en puntos básicos) y las últimas 15 sesiones para el gráfico."""
    out = []
    for sym, nom, uni in MACRO:
        V = [v for v in (D.get("ctx_velas") or {}).get(sym, []) if fecha_vela(v["t"]) <= fecha]
        if len(V) < 2: continue
        c, p = V[-1]["c"], V[-2]["c"]
        out.append({"simbolo": sym, "nombre": nom, "unidad": uni, "cierre": round(c, 3 if sym.endswith("10Y") else 2), "fecha": fecha_vela(V[-1]["t"]).isoformat(),
                    "cambio_pct": round(c / p * 100 - 100, 2), "cambio_pb": round((c - p) * 100, 1) if sym.endswith("10Y") else None,
                    "serie": [round(v["c"], 3) for v in V[-15:]], "mismo_dia": fecha_vela(V[-1]["t"]) == fecha})
    return out


def dow_aportes(D, R):
    """Aportación en puntos de cada valor al Dow Jones (índice ponderado por precio): cambio en dólares / divisor.
    El divisor se deduce del propio día: suma de los cambios en dólares / cambio del índice en puntos (محسوب)."""
    en = lambda v: any(i.get("proname") == "DJ:DJI" for i in (v.get("indexes") or []))
    M_ = [dict(v, ticker=t.split(":")[1]) for t, v in D.get("acciones", {}).items() if en(v) and v.get("change_abs") is not None]
    if "dji" not in R or len(M_) < 28 or not R["dji"]["var_pts"]: return None
    div = sum(v["change_abs"] for v in M_) / R["dji"]["var_pts"]
    if not (0.05 < div < 0.5): return None   # faltan valores o el cambio es casi cero: no se puede deducir
    L = sorted(({"ticker": v["ticker"], "nombre": NOMBRES.get(v["ticker"], nombre_en(v.get("description"))), "puntos": round(v["change_abs"] / div, 1),
                 "cambio": round(v["change"], 2), "sector": v.get("sector")} for v in M_), key=lambda x: -x["puntos"])
    sec = {}
    for x in L: x["sector"] = SECTOR_AR.get(x["sector"], x["sector"]); sec[x["sector"]] = round(sec.get(x["sector"], 0) + x["puntos"], 1)
    return {"divisor": round(div, 5), "valores": L, "sectores": sorted(sec.items(), key=lambda x: -x[1])}


def candidatas(D, extra=None, n=12):
    """Acciones del S&P 500 para elegir las cinco protagonistas: cambio, cierre, volumen, volumen frente a su media de 10 sesiones,
    valor negociado y si hay velas para su gráfico. Ordenadas por |cambio| x volumen relativo; el guion elige las 5 con noticia que lo explique."""
    nom = dict(NOMBRES, **(extra or {})); VV = D.get("acciones_velas") or {}
    out = []
    for v in acciones(D):
        if v.get("change") is None or (v.get("Value.Traded") or 0) < MIN_VALOR: continue
        rel = (v.get("volume") or 0) / v["average_volume_10d_calc"] if v.get("average_volume_10d_calc") else None
        key = next((k for k in VV if k.split(":")[1] == v["ticker"]), None)
        out.append({"ticker": v["ticker"], "nombre": nom.get(v["ticker"], nombre_en(v.get("description"))), "nombre_en": nombre_en(v.get("description")),
                    "cierre": round(v["close"], 2), "cambio": round(v["change"], 2), "volumen": v.get("volume"), "vol_rel": None if rel is None else round(rel, 2),
                    "valor_usd": round(v.get("Value.Traded") or 0), "sector": v.get("sector"), "velas": key is not None,
                    "puntuacion": round(abs(v["change"]) * (rel or 1), 2)})
    return sorted(out, key=lambda x: -x["puntuacion"])[:n]


def accion(D, ticker, extra=None):
    """Datos de una acción del S&P 500 por ticker, con sus velas diarias si se descargaron."""
    nom = dict(NOMBRES, **(extra or {}))
    for t, v in D.get("acciones", {}).items():
        if t.split(":")[1] != ticker: continue
        rel = (v.get("volume") or 0) / v["average_volume_10d_calc"] if v.get("average_volume_10d_calc") else None
        return {"ticker": ticker, "simbolo": t, "nombre": nom.get(ticker, nombre_en(v.get("description"))), "nombre_en": nombre_en(v.get("description")),
                "cierre": round(v["close"], 2), "cambio": round(v["change"], 2), "cambio_abs": round(v.get("change_abs") or 0, 2), "volumen": v.get("volume"),
                "vol_rel": None if rel is None else round(rel, 2), "valor_usd": round(v.get("Value.Traded") or 0), "semana": v.get("Perf.W"),
                "velas": (D.get("acciones_velas") or {}).get(t)}
    return None


def acciones(D):
    """Acciones ordinarias del S&P 500 (las que TradingView marca con el índice SP:SPX)."""
    en_spx = lambda v: any(i.get("proname") == "SP:SPX" for i in (v.get("indexes") or []))
    comun = lambda v: v.get("typespecs") in (None, ["common"]) or "common" in (v.get("typespecs") or [])
    return [dict(v, ticker=t.split(":")[1]) for t, v in D.get("acciones", {}).items() if comun(v) and en_spx(v)]


def movers(D, extra=None):
    """5 que más suben y 5 que más bajan del S&P 500 con más de MIN_VALOR dólares negociados."""
    nom = dict(NOMBRES, **(extra or {}))
    L = sorted([(v["change"], v["ticker"], v.get("description")) for v in acciones(D)
                if v.get("change") is not None and (v.get("Value.Traded") or 0) >= MIN_VALOR])
    f = lambda x: {"ticker": x[1], "nombre": nom.get(x[1], nombre_en(x[2])), "nombre_en": nombre_en(x[2]), "cambio": round(x[0], 2)}
    return [f(x) for x in L[::-1][:5]], [f(x) for x in L[:5]]


def grandes(D, n=7, extra=None):
    """Las n mayores del S&P 500 por capitalización, con su variación del día (las «7 grandes» del mercado)."""
    nom = dict(NOMBRES, **(extra or {}))
    L = sorted(acciones(D), key=lambda v: -(v.get("market_cap_basic") or 0))
    vistos, out = set(), []
    for v in L:
        n_ = nom.get(v["ticker"], nombre_en(v.get("description")))
        if n_ in vistos: continue  # GOOGL y GOOG
        vistos.add(n_); out.append({"ticker": v["ticker"], "nombre": n_, "cambio": round(v.get("change") or 0, 2)})
        if len(out) == n: break
    return out


def contexto(D, fecha):
    """Cambio del día de la sesión de Nueva York (o su última sesión anterior, p. ej. el Golfo un viernes) de cada símbolo de contexto."""
    out = {}
    for sym, V in D.get("ctx_velas", {}).items():
        rows = [(fecha_vela(v["t"]), v["c"]) for v in V]
        idx = [i for i, (d, _) in enumerate(rows) if d <= fecha]
        if not idx or idx[-1] == 0: continue
        i = idx[-1]
        ch = rows[i][1] - rows[i - 1][1] if sym in ("TVC:US10Y", "TVC:US02Y") else rows[i][1] / rows[i - 1][1] * 100 - 100
        out[sym] = {"fecha": rows[i][0].isoformat(), "close": rows[i][1], "change": round(ch, 3 if sym.endswith("10Y") else 2), "mismo_dia": rows[i][0] == fecha}
    return out


def calc(D, extra=None):
    R, A = {}, {}
    for k in CLAVES:
        if f"{k}_diario" in D: R[k], A[k] = calc_indice(D, k)
    R["mejores"], R["peores"] = movers(D, extra)
    R["grandes"] = grandes(D, extra=extra)
    R["fecha"] = R["spx"]["fecha"]
    R["contexto"] = contexto(D, dt.date.fromisoformat(R["fecha"]))
    R["sectores"] = sectores(D)
    R["macro"] = macro(D, dt.date.fromisoformat(R["fecha"]))
    R["dow_aportes"] = dow_aportes(D, R)
    R["candidatas"] = candidatas(D, extra)
    R["ndx_grandes"] = grandes_ndx(D, extra)
    return R, A


def grandes_ndx(D, extra=None, n=8):
    """Las n mayores del Nasdaq 100 por capitalización con su cambio (comportamiento de las grandes tecnológicas)."""
    nom = dict(NOMBRES, **(extra or {}))
    en = lambda v: any(i.get("proname") == "NASDAQ:NDX" for i in (v.get("indexes") or []))
    L = sorted((dict(v, ticker=t.split(":")[1]) for t, v in D.get("acciones", {}).items() if en(v) and v.get("change") is not None),
               key=lambda v: -(v.get("market_cap_basic") or 0))
    vistos, out = set(), []
    for v in L:
        n_ = nom.get(v["ticker"], nombre_en(v.get("description")))
        if n_ in vistos: continue
        vistos.add(n_); out.append({"ticker": v["ticker"], "nombre": n_, "cambio": round(v["change"], 2)})
        if len(out) == n: break
    return out


if __name__ == "__main__":
    r, _ = calc(json.load(open(sys.argv[1])))
    print(json.dumps(r, ensure_ascii=False, indent=1))
