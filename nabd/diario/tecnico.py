"""Indicadores de Wall Street (S&P 500 como índice principal; Nasdaq Composite, Dow Jones y Russell 2000 como acompañantes)
a partir de datos/mercado-<fecha>.json. Lo usan make_video.py, make_short.py y gen_meta.py, y sirve para escribir el guion.
uso: python3 tecnico.py <mercado.json>  -> imprime JSON con cierres, medias, RSI, estocástico, niveles, volumen, valores y contexto."""
import json, re, sys, datetime as dt, numpy as np
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")
RIAD = dt.timezone(dt.timedelta(hours=3))  # hora del Golfo (Riad, Kuwait, Doha, Manama); Dubái y Mascate son una hora más
TZ = RIAD
CLAVES = ("spx", "ndq", "dji", "rut")
INDICE = {"spx": "مؤشر إس آند بي 500", "ndq": "مؤشر ناسداك المركب", "dji": "مؤشر داو جونز الصناعي", "rut": "مؤشر راسل 2000"}
INDICE_CORTO = {"spx": "إس آند بي 500", "ndq": "ناسداك", "dji": "داو جونز", "rut": "راسل 2000"}
SIMBOLO = {"spx": "SP:SPX", "ndq": "NASDAQ:IXIC", "dji": "DJ:DJI", "rut": "TVC:RUT"}
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
           "INTU": "إنتويت", "PYPL": "باي بال", "SCHW": "تشارلز شواب", "COIN": "كوينبيس", "HOOD": "روبن هود", "SPGI": "إس آند بي غلوبال"}
MIN_VALOR = 50e6  # solo valores con más de 50 millones de dólares negociados en la sesión


def fecha_ar(d, dia=True):
    return (DIAS[d.weekday()] + " " if dia else "") + f"{d.day} {MESES[d.month - 1]} {d.year}"


def fecha_vela(t):
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).date()


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
             volumen_vs_media10_pct=None if vr is None else round(float(vr), 1), niveles=niveles)
    if k == "spx":
        acc = acciones(D)
        r.update(suben=sum(1 for v in acc if (v.get("change") or 0) > 0), bajan=sum(1 for v in acc if (v.get("change") or 0) < 0),
                 sin_cambio=sum(1 for v in acc if v.get("change") == 0), valor_negociado_usd=round(sum(v.get("Value.Traded") or 0 for v in acc)))
    return r, dict(dates=dates, o=o, hi=hi, lo=lo, c=c, S50=S50, S200=S200, RSI=RSI, K=K, D=Dl)


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
    return R, A


if __name__ == "__main__":
    r, _ = calc(json.load(open(sys.argv[1])))
    print(json.dumps(r, ensure_ascii=False, indent=1))
