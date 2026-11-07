"""Indicadores del índice QE General de la Bolsa de Qatar (QSE:GNRI) a partir de datos/mercado-<fecha>.json.
Lo usan make_video.py, make_short.py y gen_meta.py, y sirve para escribir el guion.
uso: python3 tecnico.py <mercado.json>  -> imprime JSON con cierre, medias, RSI, estocástico, niveles, volumen y valores."""
import json, sys, datetime as dt, numpy as np

TZ = dt.timezone(dt.timedelta(hours=3))  # hora de Doha (sin horario de verano)
INDICE = {"qe": "مؤشر بورصة قطر العام (QE)"}
INDICE_CORTO = {"qe": "مؤشر قطر"}
MERCADO = {"QSE": "بورصة قطر"}
MESES = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
DIAS = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
# Nombres en árabe de las cotizadas de la QSE (el video.json del día puede añadir más en "nombres").
NOMBRES = {"QNBK": "بنك قطر الوطني", "QIBK": "مصرف قطر الإسلامي", "CBQK": "البنك التجاري", "QIIK": "بنك قطر الدولي الإسلامي", "MARK": "مصرف الريان",
           "DUBK": "بنك دخان", "DHBK": "بنك الدوحة", "ABQK": "البنك الأهلي", "QFBQ": "بنك لشا", "IQCD": "صناعات قطر",
           "QAMC": "قطر لصناعة الألمنيوم", "MPHC": "مسيعيد للبتروكيماويات", "ORDS": "Ooredoo", "VFQS": "فودافون قطر", "QFLS": "قطر للوقود (وقود)",
           "QGTS": "ناقلات", "QNNS": "الملاحة", "GWCS": "الخليج للمخازن", "GISS": "الخليج الدولية للخدمات", "QEWS": "نبراس للطاقة",
           "BRES": "بروة العقارية", "ERES": "إزدان القابضة", "UDCD": "المتحدة للتنمية", "MRDS": "مزايا العقارية", "IGRD": "استثمار القابضة",
           "BLDN": "بلدنا", "QIMD": "قطر للصناعات التحويلية", "QATI": "قطر للتأمين", "FALH": "الفالح التعليمية", "IHGS": "إنماء القابضة",
           "QNCD": "قطر الوطنية للإسمنت", "QIGD": "مجموعة المستثمرين القطريين", "QISI": "قطر الإسلامية للتأمين", "BEMA": "بيمه للتأمين",
           "TQES": "تكنو كيو", "MCCS": "مناعي", "MEZA": "ميزة", "QGMD": "القطرية الألمانية للمستلزمات الطبية", "WDAM": "ودام الغذائية",
           "AKHI": "الخليج للتأمين التكافلي", "MFMS": "مساندة", "QLMI": "كيو إل إم", "DBIS": "دلالة", "MKDM": "مقدام القابضة", "AHCS": "أعمال",
           "SIIS": "السلام العالمية", "ZHCD": "زاد القابضة", "MCGS": "الرعاية الطبية", "MERS": "الميرة", "MHAR": "المحار القابضة",
           "QGRI": "القطرية العامة للتأمين", "DOHI": "الدوحة للتأمين", "NLCS": "الإجارة القابضة", "QCFS": "قطر للسينما", "QOIS": "قطر وعمان للاستثمار"}
MIN_VALOR = 1e6  # solo valores con más de 1 millón de riales negociados en la sesión (evita saltos de valores sin liquidez)


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
    # volumen: el de la vela del índice si lo hay; si no (QE no lo trae), la suma de las acciones del mercado (calculado)
    ex = "QSE"; acc = [v for v in D.get("acciones", {}).values() if v.get("exchange") == ex]
    if not np.isnan(vol[-1]) and np.isfinite(vol[-11:-1]).all():
        vr = vol[-1] / vol[-11:-1].mean() * 100 - 100; vfuente = "índice"
    else:
        hoy = sum(v["volume"] or 0 for v in acc); med = sum(v["average_volume_10d_calc"] or 0 for v in acc)
        vr = hoy / med * 100 - 100 if med else None; vfuente = "suma de acciones"
    sem = [i for i, d in enumerate(dates) if d <= dates[-1] - dt.timedelta(days=(dates[-1].weekday() + 1) % 7 + 1)]  # semana de la QSE: domingo a jueves
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
                valor_negociado_qar=round(sum(v.get("Value.Traded") or 0 for v in acc)),
                suben=sum(1 for v in acc if (v.get("change") or 0) > 0), bajan=sum(1 for v in acc if (v.get("change") or 0) < 0),
                sin_cambio=sum(1 for v in acc if v.get("change") == 0), niveles=niveles), \
        dict(dates=dates, o=o, hi=hi, lo=lo, c=c, S50=S50, S200=S200, RSI=RSI, K=K, D=Dl)


def movers(D, extra=None):
    nom = dict(NOMBRES, **(extra or {}))
    L = sorted([(v["change"], k.split(":")[1], v["exchange"]) for k, v in D.get("acciones", {}).items()
                if v.get("change") is not None and (v.get("Value.Traded") or 0) >= MIN_VALOR])
    f = lambda x: {"ticker": x[1], "mercado": x[2], "nombre": nom.get(x[1], x[1]), "cambio": round(x[0], 2)}
    return [f(x) for x in L[::-1][:5]], [f(x) for x in L[:5]]


def calc(D, extra=None):
    R = {k: calc_indice(D, k) for k in ("qe",)}
    A = {k: R[k][1] for k in R}; R = {k: R[k][0] for k in R}
    R["mejores"], R["peores"] = movers(D, extra)
    R["fecha"] = R["qe"]["fecha"]
    R["contexto"] = {k: {"close": v.get("close"), "change": None if v.get("change") is None else round(v["change"], 2)} for k, v in D.get("tv", {}).items()}
    return R, A


if __name__ == "__main__":
    r, _ = calc(json.load(open(sys.argv[1])))
    print(json.dumps(r, ensure_ascii=False, indent=1))
