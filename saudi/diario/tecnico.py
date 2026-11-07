"""Indicadores de TASI (Tadawul All Share, TADAWUL:TASI) y de Nomu (TADAWUL:NOMUC) a partir de datos/mercado-<fecha>.json.
Lo usan make_video.py, make_short.py y gen_meta.py, y sirve para escribir el guion.
uso: python3 tecnico.py <mercado.json>  -> imprime JSON con cierre, medias, RSI, estocástico, niveles, volumen, valores y contexto."""
import json, sys, datetime as dt, numpy as np

TZ = dt.timezone(dt.timedelta(hours=3))  # hora de Riad (sin horario de verano)
INDICE = {"tasi": "مؤشر السوق الرئيسية (تاسي)", "nomu": "مؤشر السوق الموازية (نمو)"}
INDICE_CORTO = {"tasi": "تاسي", "nomu": "نمو"}
MESES = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
DIAS = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
# Nombres en árabe de las cotizadas de Tadawul por código (el video.json del día puede añadir más en "nombres").
NOMBRES = {"2222": "أرامكو السعودية", "1120": "مصرف الراجحي", "1180": "البنك الأهلي السعودي", "7010": "إس تي سي", "2010": "سابك",
           "1211": "معادن", "1150": "مصرف الإنماء", "1010": "بنك الرياض", "1060": "البنك السعودي الأول", "1050": "البنك السعودي الفرنسي",
           "1080": "البنك العربي الوطني", "1140": "بنك البلاد", "1020": "بنك الجزيرة", "1030": "البنك السعودي للاستثمار", "2082": "أكوا",
           "5110": "الكهرباء السعودية", "2280": "المراعي", "4013": "سليمان الحبيب", "4002": "المواساة", "7020": "اتحاد اتصالات (موبايلي)",
           "7030": "زين السعودية", "7203": "علم", "2020": "سابك للمغذيات الزراعية", "1111": "مجموعة تداول", "4300": "دار الأركان",
           "4250": "جبل عمر", "4280": "المملكة القابضة", "8010": "التعاونية", "8210": "بوبا العربية", "2380": "بترو رابغ", "2310": "سبكيم العالمية",
           "2350": "كيان السعودية", "2290": "ينساب", "2330": "المتقدمة", "3020": "أسمنت اليمامة", "3030": "أسمنت السعودية", "3040": "أسمنت القصيم",
           "3010": "أسمنت العربية", "3050": "أسمنت الجنوب", "4190": "جرير", "4003": "إكسترا", "4164": "النهدي", "4263": "سال", "4030": "البحري",
           "4031": "الخدمات الأرضية", "1321": "أنابيب الشرق", "2081": "الخريف", "2223": "لوبريف", "4142": "كابلات الرياض", "1810": "سيرا",
           "2030": "المصافي", "4321": "المراكز العربية", "4322": "رتال", "4323": "سمو", "4220": "إعمار المدينة الاقتصادية", "4100": "مكة للإنشاء",
           "4150": "التعمير", "4090": "طيبة", "2050": "صافولا", "6004": "كاترينج", "2270": "سدافكو", "6002": "هرفي", "6010": "نادك",
           "1830": "لجام للرياضة", "4161": "بن داود", "4001": "أسواق العثيم", "4160": "ثمار", "7202": "سلوشنز", "7204": "توبي", "2083": "مرافق",
           "1182": "أملاك العالمية", "1183": "سهل", "4081": "النايفات", "4082": "مرنة", "4084": "دراية", "2382": "أديس", "5111": "إيه سي سي",
           "4009": "السعودي الألماني الصحية", "4004": "دله الصحية", "4005": "رعاية", "4007": "الحمادي", "4017": "فقيه الطبية", "4015": "جمجوم فارما",
           "2070": "الدوائية", "8230": "الراجحي تكافل", "8030": "ميدغلف", "8020": "ملاذ للتأمين", "8070": "الدرع العربي", "8250": "جي آي جي",
           "8012": "جزيرة تكافل", "2381": "الحفر العربية", "2370": "مسك", "1301": "أسلاك", "1302": "بوان", "1303": "الصناعات الكهربائية",
           "1304": "اليمامة للحديد", "1320": "أنابيب السعودية", "2160": "أميانتيت", "2200": "أنابيب", "2210": "نماء للكيماويات", "2250": "المجموعة السعودية",
           "2060": "التصنيع", "2001": "كيمانول", "2170": "اللجين", "2240": "الزامل للصناعة", "2300": "صناعة الورق", "2360": "الفخارية",
           "4020": "العقارية", "4320": "الأندلس", "4340": "الراجحي ريت", "4140": "صادرات", "4200": "الدريس", "4260": "بدجت السعودية",
           "4261": "ذيب", "4262": "لومي", "4310": "مدينة المعرفة", "4071": "العربية", "4072": "إم بي سي", "4210": "الأبحاث والإعلام",
           "1820": "بان", "6012": "ريدان", "6013": "التطويرية الغذائية", "6014": "الآمار", "6015": "أمريكانا", "6040": "تبوك الزراعية",
           "6050": "الأسماك", "6060": "الشرقية للتنمية", "6070": "الجوف", "6090": "جازادكو", "2100": "وفرة", "2281": "تنمية", "2282": "نقي",
           "2283": "المطاحن الأولى", "2284": "المطاحن الحديثة", "2285": "المطاحن العربية", "2286": "المطاحن الرابعة", "2287": "إنتاج",
           "1201": "تكوين", "1202": "مبكو", "1210": "بي سي آي", "1212": "أسترا الصناعية", "1213": "نسيج", "1214": "الحسن شاكر", "2040": "الخزف",
           "2090": "جبسكو", "2110": "الكابلات السعودية", "2130": "صدق", "2140": "أيان", "2150": "زجاج", "2180": "فيبكو", "2190": "سيسكو القابضة",
           "2220": "معدنية", "2230": "الكيميائية", "2320": "البابطين", "2340": "العبداللطيف", "3002": "أسمنت نجران", "3003": "أسمنت المدينة",
           "3004": "أسمنت الشمالية", "3005": "أم القرى", "3007": "الواحة", "3008": "الكثيري", "3060": "أسمنت ينبع", "3080": "أسمنت الشرقية",
           "3090": "أسمنت تبوك", "3091": "أسمنت الجوف", "3092": "أسمنت الرياض", "4006": "المزرعة", "4008": "ساكو", "4011": "لازوردي",
           "4012": "الأصيل", "4014": "دار المعدات", "4016": "أفالون فارما", "4018": "الموسى", "4019": "اس ام سي للرعاية الصحية", "4040": "سابتكو",
           "4050": "ساسكو", "4051": "باعظيم", "4061": "أنعام القابضة", "4070": "تهامة", "4080": "سناد القابضة", "4083": "تسهيل", "4110": "باتك",
           "4130": "الباحة", "4170": "شمس", "4180": "فتيحي", "4191": "أبو معطي", "4192": "السيف غاليري", "4193": "نايس ون", "4194": "محطة البناء",
           "4240": "سينومي ريتيل", "4270": "طباعة وتغليف", "4290": "الخليج للتدريب", "4291": "الوطنية للتعليم", "4292": "عطاء", "4330": "الرياض ريت",
           "7040": "عذيب", "7200": "إم آي إس", "7201": "بحر العرب", "8040": "متكاملة", "8050": "سلامة", "8060": "ولاء", "8100": "سايكو",
           "8120": "إتحاد الخليج الأهلية", "8150": "أسيج", "8160": "التأمين العربية", "8170": "الاتحاد", "8180": "الصقر للتأمين", "8190": "المتحدة للتأمين",
           "8200": "الإعادة السعودية", "8240": "تشب", "8260": "الخليجية العامة", "8270": "بروج للتأمين", "8280": "العالمية", "8300": "الوطنية",
           "8310": "أمانة للتأمين", "8311": "عناية", "8313": "رسن", "1831": "مهارة", "1832": "صدر", "1833": "الموارد", "1834": "سماسكو",
           "1835": "تمكين", "2080": "الغاز", "2084": "مياهنا", "4141": "العمران", "4143": "تالكو", "4144": "رؤوم", "4145": "العبيكان للزجاج",
           "4146": "جاز", "4147": "سي جي إس", "4148": "الوسائل الصناعية", "4325": "مسار", "4324": "بنان", "4326": "الماجدية", "4327": "الرمز",
           "6016": "برغرايززر", "6017": "جاهز", "6018": "الأندية للرياضة", "6019": "المسار الشامل", "1322": "أماك", "1323": "يو سي آي سي",
           "2083b": "", "4021": "المركز الكندي الطبي", "4022": "الرعاية المتقدمة", "4264": "طيران ناس", "4265": "شري", "7211": "عزم"}
MIN_VALOR = 1e6  # solo valores con más de 1 millón de riyales negociados en la sesión (evita saltos de valores sin liquidez)


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
    acc = acciones(D, k)
    if not np.isnan(vol[-1]) and np.isfinite(vol[-11:-1]).all():
        vr = vol[-1] / vol[-11:-1].mean() * 100 - 100; vfuente = "índice"
    else:
        hoy = sum(v["volume"] or 0 for v in acc); med = sum(v["average_volume_10d_calc"] or 0 for v in acc)
        vr = hoy / med * 100 - 100 if med else None; vfuente = "suma de acciones"
    sem = [i for i, d in enumerate(dates) if d <= dates[-1] - dt.timedelta(days=(dates[-1].weekday() + 1) % 7 + 1)]  # semana de Tadawul: domingo a jueves
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
                valor_negociado_sar=round(sum(v.get("Value.Traded") or 0 for v in acc)),
                suben=sum(1 for v in acc if (v.get("change") or 0) > 0), bajan=sum(1 for v in acc if (v.get("change") or 0) < 0),
                sin_cambio=sum(1 for v in acc if v.get("change") == 0), niveles=niveles), \
        dict(dates=dates, o=o, hi=hi, lo=lo, c=c, S50=S50, S200=S200, RSI=RSI, K=K, D=Dl)


def acciones(D, k):
    """Acciones del mercado principal (las que TradingView incluye en TASI) o de Nomu (el resto de Tadawul), solo ordinarias."""
    en_tasi = lambda v: any(i.get("proname") == "TADAWUL:TASI" for i in (v.get("indexes") or []))
    comun = lambda v: v.get("typespecs") in (None, ["common"]) or "common" in (v.get("typespecs") or [])
    return [dict(v, ticker=t.split(":")[1]) for t, v in D.get("acciones", {}).items() if comun(v) and en_tasi(v) == (k == "tasi")]


def movers(D, extra=None):
    """5 que más suben y 5 que más bajan del mercado principal (TASI) con más de MIN_VALOR riyales negociados."""
    nom = dict(NOMBRES, **(extra or {}))
    L = sorted([(v["change"], v["ticker"], v.get("description")) for v in acciones(D, "tasi")
                if v.get("change") is not None and (v.get("Value.Traded") or 0) >= MIN_VALOR])
    f = lambda x: {"ticker": x[1], "nombre": nom.get(x[1], x[2]), "nombre_en": x[2], "cambio": round(x[0], 2)}
    return [f(x) for x in L[::-1][:5]], [f(x) for x in L[:5]]


# Contexto: bolsas del Golfo y Asia el mismo día de la sesión; Wall Street, Europa, Brent y oro con su último cierre antes de que
# cierre Tadawul (el de la víspera), que es el que llega a la sesión saudí.
MISMO_DIA = {"ADX:FADGI", "DFM:DFMGI", "QSE:GNRI", "TVC:NI225", "TVC:HSI", "TVC:KOSPI", "SSE:000001", "TADAWUL:2222"}


def contexto(D, fecha):
    out = {}
    for sym, V in D.get("ctx_velas", {}).items():
        rows = [(dt.datetime.fromtimestamp(v["t"], dt.timezone.utc).date(), v["c"]) for v in V]
        idx = [i for i, (d, _) in enumerate(rows) if (d == fecha if sym in MISMO_DIA else d < fecha)]
        if not idx or idx[-1] == 0: continue
        i = idx[-1]; out[sym] = {"fecha": rows[i][0].isoformat(), "close": rows[i][1], "change": round(rows[i][1] / rows[i - 1][1] * 100 - 100, 2)}
    return out


def calc(D, extra=None):
    R = {k: calc_indice(D, k) for k in ("tasi", "nomu")}
    A = {k: R[k][1] for k in R}; R = {k: R[k][0] for k in R}
    R["mejores"], R["peores"] = movers(D, extra)
    R["fecha"] = R["tasi"]["fecha"]
    R["contexto"] = contexto(D, dt.date.fromisoformat(R["fecha"]))
    return R, A


if __name__ == "__main__":
    r, _ = calc(json.load(open(sys.argv[1])))
    print(json.dumps(r, ensure_ascii=False, indent=1))
