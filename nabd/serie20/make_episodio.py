# Episodio de la serie «عمالقة وول ستريت» (Nabd Wall Street): una empresa tras su informe de resultados, 1920x1080, máximo 4 minutos
# (Daniel, 13-nov-2026). 7 escenas: portada, resultados del trimestre, ingresos y margen (8 trimestres), balance y deuda/caja frente a la
# capitalización, flujo de caja, frente a las estimaciones de los analistas y la guía, y cierre. Todas las cifras de pantalla salen de
# datos.json (TradingView, rama datos-serie20-nabd); video.json pone la locución, los titulares y la guía de la empresa (con fuente).
# Uso: AUD=<scratch> [VOZ_DIR=<wav de Azure>] python3 make_episodio.py <carpeta del episodio> [preview]
#   La carpeta tiene video.json y datos.json. Escribe serie20-<ticker>-<fecha>-Nabd.mp4, times.json y guion-<...>-Nabd.md.
import os, sys, json, textwrap, datetime as dt, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from comun import *

DIR = os.path.abspath(sys.argv[1]); PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
AUD = os.environ.get("AUD", "aud"); os.makedirs(AUD, exist_ok=True)
VJ = json.load(open(f"{DIR}/video.json")); S = json.load(open(f"{DIR}/datos.json")); V = VJ["voz"]; U = S["ultimo"]
SERIE = "عمالقة وول ستريت"; NAVY = "#13294B"; W, H = 1920, 1080
MIN_S, MAX_S = 120, 240   # máximo 4 minutos (Daniel, 13-nov-2026)
BASE = f"serie20-{VJ['ticker'].lower()}-{VJ['fecha_resultados']}"
OUT = f"{DIR}/{BASE}-Nabd.mp4"
MESES = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
fecha_ar = lambda s: (lambda d: f"{d.day} {MESES[d.month - 1]} {d.year}")(dt.date.fromisoformat(s))
LG = load_logo(130); LGB = load_logo(230)
SECS = ["المقدمة", "النتائج", "الإيرادات والهامش", "الميزانية", "التدفقات النقدية", "التوقعات", "الخلاصة"]
FUENTE_TV = f"TradingView (بيانات أساسية مأخوذة من تقارير الشركة)، {str(S.get('generado', ''))[:10]}"


def T(f, x, y, s, c=FG, fs=24, w="normal", ha="right", **k):
    return f.text(x, y, ar(s), color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def rect(f, x, y, w, h, c, a=1.0):
    f.patches.append(plt.Rectangle((x, y), w, h, transform=f.transFigure, color=col(c), alpha=a, figure=f))


def mm(v):
    """Dólares en miles de millones (مليار) o millones, con signo."""
    if v is None: return "—"
    a = abs(v); s = "-" if v < 0 else ""
    return f"{s}{a / 1e9:,.1f} مليار $" if a >= 1e9 else f"{s}{a / 1e6:,.0f} مليون $"


def base(n, kicker, title):
    f = fig(W, H)
    T(f, 0.94, 0.905, kicker, GOLD, 24, "bold")
    T(f, 0.94, 0.82, title, FG, 40 if len(title) <= 55 else 34, "bold")
    T(f, 0.105, 0.925, f"{SERIE} · {VJ['ar']} ({VJ['ticker']})", MUTED, 19, "bold", ha="left")
    T(f, 0.105, 0.89, MARCA + " · " + VJ["trimestre"], DIM, 16, "bold", ha="left")
    w = 0.88 / len(SECS)
    for i in range(len(SECS)): rect(f, 0.94 - (i + 1) * w + 0.008, 0.975, w - 0.008, 0.008, GOLD if i < n else DIM)
    return f


def fuente(f, s): T(f, 0.94, 0.17, "\n".join(textwrap.wrap(s, 170)), MUTED, 14, linespacing=1.35)


TRI = [t for t in S.get("trimestres", []) if t.get("ingresos")][-8:]
CAP = S.get("cap_mercado")


def lbl_tri(p):
    return f"ر{p[-1]}\n{p[:4]}" if p else ""   # trimestre del año fiscal de la empresa


def s_portada(t):
    f = fig(W, H); a = ease(t / 0.6)
    T(f, 0.94, 0.88, MARCA + " · سلسلة " + SERIE, GOLD, 30, "bold", alpha=a)
    rect(f, 0, 0.66, 1.0, 0.17, GOLD, a)
    T(f, 0.94, 0.745, VJ["ar"], BG, 88, "bold", va="center", alpha=a)
    f.text(0.20, 0.745, VJ["ticker"], color=BG, fontsize=64, weight="bold", ha="left", va="center", alpha=a)
    T(f, 0.94, 0.55, VJ["trimestre"], FG, 42, "bold", alpha=ease((t - 0.15) / 0.5))
    T(f, 0.94, 0.48, f"إعلان النتائج: {fecha_ar(VJ['fecha_resultados'])} · {VJ['sector']}", MUTED, 28, alpha=ease((t - 0.25) / 0.5))
    if VJ.get("titular"): T(f, 0.94, 0.33, VJ["titular"], BLUE, 34, "bold", alpha=ease((t - 0.35) / 0.5))
    return with_logo(to_arr(f), LGB, x=110, y=40)


def yoy(v): return "" if v is None else f"{v:+.1f}% على أساس سنوي"


def kpis():
    K = [("إجمالي الإيرادات (قبل مصروف الفوائد)" if VJ.get("sector_tipo") == "banco" else "الإيرادات", mm(U.get("total_revenue_fq")), yoy(U.get("total_revenue_yoy_growth_fq")), (U.get("total_revenue_yoy_growth_fq") or 0) >= 0),
         ("صافي الربح", mm(U.get("net_income_fq")), yoy(U.get("net_income_yoy_growth_fq")), (U.get("net_income_yoy_growth_fq") or 0) >= 0),
         ("ربحية السهم المخففة", "—" if U.get("earnings_per_share_diluted_fq") is None else f"{U['earnings_per_share_diluted_fq']:.2f} $",
          yoy(U.get("earnings_per_share_diluted_yoy_growth_fq")), (U.get("earnings_per_share_diluted_yoy_growth_fq") or 0) >= 0)]
    if U.get("free_cash_flow_fq") is not None and VJ.get("sector_tipo") != "banco":
        K.append(("التدفق النقدي الحر للربع", mm(U["free_cash_flow_fq"]), "التشغيلي − الرأسمالي", U["free_cash_flow_fq"] >= 0))
    elif U.get("oper_income_fq") is not None and U.get("total_revenue_fq"):
        K.append(("الهامش التشغيلي للربع", f"{U['oper_income_fq'] / U['total_revenue_fq'] * 100:.1f}%", "محسوب", True))
    return K


def s_resultados(t):
    f = base(2, "نتائج الربع", VJ.get("titulo_resultados", "أهم أرقام " + VJ["trimestre"]))
    K = kpis()
    for i, (lab, big, sub, up) in enumerate(K):
        b = ease((t - i * 0.12) / 0.4); x0 = 0.94 - (i + 1) * 0.215 + 0.01
        rect(f, x0, 0.36, 0.2, 0.36, NAVY, b); rect(f, x0, 0.715, 0.2, 0.006, GOLD, b)
        T(f, x0 + 0.185, 0.69, "\n".join(textwrap.wrap(lab, 20)), MUTED, 21, "bold", alpha=b, va="top", linespacing=1.3)
        T(f, x0 + 0.185, 0.53, big, FG, 36 if len(big) <= 14 else 30, "bold", alpha=b)
        T(f, x0 + 0.185, 0.43, sub, TEAL if up else NEG, 20, "bold", alpha=b, va="center")
    fuente(f, FUENTE_TV + ". التغير على أساس سنوي مقارنةً بالربع نفسه من العام السابق.")
    return to_arr(f)


def s_ingresos(t):
    f = base(3, "الإيرادات وهامش صافي الربح", VJ.get("titulo_ingresos", "آخر ثمانية أرباع"))
    X = [x for x in TRI if x.get("ingresos")]; ee = ease(t)
    if X:
        ax = f.add_axes([0.08, 0.25, 0.84, 0.36]); clean(ax); i = np.arange(len(X)); v = [x["ingresos"] / 1e9 for x in X]
        ax.bar(i, [y * ee for y in v], color=[GOLD if j == len(X) - 1 else BLUE for j in range(len(X))], width=0.6)
        ax.set_xticks(i, [ar(lbl_tri(x["periodo"])) for x in X]); ax.set_yticks([]); ax.set_ylim(0, max(v) * 1.2); ax.tick_params(labelsize=15)
        ax.set_xlim(-0.5, len(X) - 0.5)
        if t > 0.5:
            for j, y in zip(i, v): ax.text(j, y * ee + max(v) * 0.03, f"{y:,.1f}", ha="center", color=FG, fontsize=17, weight="bold")
        mg = [(j, x["beneficio_neto"] / x["ingresos"] * 100) for j, x in zip(i, X) if x.get("beneficio_neto") is not None]
        if mg and t > 0.4:  # el margen en su propia franja, encima de las barras
            a2 = f.add_axes([0.08, 0.63, 0.84, 0.09]); clean(a2); a2.set_yticks([]); a2.set_xticks([]); a2.set_xlim(-0.5, len(X) - 0.5)
            a2.plot([m[0] for m in mg], [m[1] for m in mg], color=TEAL, lw=3, marker="o", ms=9)
            lo, hi = min(m[1] for m in mg), max(m[1] for m in mg); r = (hi - lo) or 1; a2.set_ylim(lo - r * 0.3, hi + r * 0.9)
            for j, m in mg: a2.text(j, m + r * 0.25, f"{m:.0f}%", ha="center", color=TEAL, fontsize=15, weight="bold")
        T(f, 0.92, 0.745, ("الأعمدة: إجمالي الإيرادات قبل مصروف الفوائد (مليار $)" if VJ.get("sector_tipo") == "banco" else "الأعمدة: الإيرادات الفصلية (مليار $)") + " · الخط الأخضر: هامش صافي الربح (محسوب)", MUTED, 18)
    fuente(f, FUENTE_TV + ". الأرباع حسب السنة المالية للشركة (ر = ربع). الهامش = صافي الربح ÷ الإيرادات (محسوب).")
    return to_arr(f)


def s_balance(t):
    f = base(4, "الميزانية العمومية · نهاية الربع", VJ.get("titulo_balance", "النقد والديون وحقوق المساهمين"))
    caja, deuda = U.get("cash_n_short_term_invest_fq"), U.get("total_debt_fq")
    items = [("النقد والاستثمارات قصيرة الأجل", mm(caja), BLUE), ("إجمالي الديون", mm(deuda), NEG), ("حقوق المساهمين", mm(U.get("total_equity_fq")), TEAL)]
    for i, (lab, big, c) in enumerate(items):
        b = ease((t - i * 0.12) / 0.4); y = 0.62 - i * 0.135
        rect(f, 0.50, y, 0.44, 0.115, NAVY, b); rect(f, 0.935, y, 0.005, 0.115, c, b)
        T(f, 0.92, y + 0.075, lab, MUTED, 22, "bold", alpha=b); T(f, 0.92, y + 0.025, big, FG, 34, "bold", alpha=b)
    if CAP:
        b = ease((t - 0.4) / 0.4)
        T(f, 0.45, 0.70, "مقارنةً بالقيمة السوقية (محسوب)", GOLD, 26, "bold", alpha=b)
        T(f, 0.45, 0.645, f"القيمة السوقية: {mm(CAP)}", FG, 24, alpha=b)
        for j, (lab, v, c) in enumerate([("الديون ÷ القيمة السوقية", deuda / CAP * 100 if deuda else None, NEG),
                                          ("النقد ÷ القيمة السوقية", caja / CAP * 100 if caja else None, BLUE)]):
            y = 0.53 - j * 0.15
            T(f, 0.45, y, lab, MUTED, 22, "bold", alpha=b)
            f.text(0.06, y - 0.075, "—" if v is None else f"{v:.1f}%", color=c, fontsize=54, weight="bold", ha="left", alpha=b)
    fuente(f, FUENTE_TV + ". النسب محسوبة، وهي بيانات وليست حكمًا شرعيًا ولا توصية." +
           (" في البنوك تشمل الديون الودائع والاقتراض ولا تُقارن مباشرةً بالشركات الأخرى." if VJ.get("sector_tipo") == "banco" else ""))
    return to_arr(f)


def s_flujo(t):
    f = base(5, "التدفقات النقدية", VJ.get("titulo_flujo", "من أين يأتي النقد وأين يذهب"))
    L = [(l, v, c) for l, v, c in [("التدفق التشغيلي (12 شهرًا)", U.get("cash_f_operating_activities_ttm"), TEAL),
                                   ("الإنفاق الرأسمالي (12 شهرًا)", abs(U["capital_expenditures_ttm"]) if U.get("capital_expenditures_ttm") else None, NEG),
                                   ("التدفق الحر (12 شهرًا)", U.get("free_cash_flow_ttm"), GOLD)] if v is not None]
    for i, (lab, v, c) in enumerate(L):
        b = ease((t - i * 0.12) / 0.4); y = 0.62 - i * 0.135
        rect(f, 0.55, y, 0.39, 0.115, NAVY, b); rect(f, 0.935, y, 0.005, 0.115, c, b)
        T(f, 0.92, y + 0.075, lab, MUTED, 22, "bold", alpha=b); T(f, 0.92, y + 0.025, mm(v), FG, 34, "bold", alpha=b)
    X = [x for x in TRI if x.get("flujo_libre") is not None]
    if X:
        ax = f.add_axes([0.06, 0.30, 0.46, 0.40]); clean(ax); i = np.arange(len(X)); v = [x["flujo_libre"] / 1e9 for x in X]; ee = ease(t)
        ax.bar(i, [y * ee for y in v], color=[TEAL if y >= 0 else NEG for y in v], width=0.6); ax.axhline(0, color=DIM, lw=1)
        ax.set_xticks(i, [ar(lbl_tri(x["periodo"])) for x in X]); ax.set_yticks([]); ax.tick_params(labelsize=13)
        lo, hi = min(v + [0]), max(v + [0]); ax.set_ylim(lo - (hi - lo) * 0.15, hi + (hi - lo) * 0.25)
        if t > 0.5:
            for j, y in zip(i, v): ax.text(j, y * ee + (hi - lo) * (0.04 if y >= 0 else -0.1), f"{y:,.1f}", ha="center", color=FG, fontsize=14, weight="bold")
        T(f, 0.52, 0.72, "التدفق النقدي الحر في كل ربع (مليار $)", MUTED, 18)
    fuente(f, FUENTE_TV + ". التدفق النقدي الحر = التدفق التشغيلي ناقص الإنفاق الرأسمالي.")
    return to_arr(f)


def s_expectativas(t):
    E = VJ.get("expectativas") or {}
    f = base(6, "مقارنةً بتقديرات المحللين", E.get("titulo", "ماذا انتظر السوق وماذا تحقق"))
    filas = []
    if U.get("earnings_per_share_forecast_fq") is not None and U.get("eps_surprise_percent_fq") is not None:
        real = U["earnings_per_share_forecast_fq"] + (U.get("eps_surprise_fq") or 0); gaap = U.get("earnings_per_share_diluted_fq")
        lab = "ربحية السهم" if gaap and abs(real - gaap) <= 0.05 * abs(gaap) else "ربحية السهم المعدّلة"   # los analistas comparan con la cifra ajustada
        filas.append((lab, f"الفعلي {real:.2f} $ · التقدير {U['earnings_per_share_forecast_fq']:.2f} $ · الفارق {U['eps_surprise_percent_fq']:+.1f}%",
                      U["eps_surprise_percent_fq"] >= 0))
    rv = U.get("revenue_forecast_fq"); rr = rv + (U.get("revenue_surprise_fq") or 0) if rv else None
    if rv and U.get("revenue_surprise_percent_fq") is not None and abs(rr - U["total_revenue_fq"]) <= 0.05 * U["total_revenue_fq"]:
        filas.append(("الإيرادات", f"الفعلي {mm(rr)} · التقدير {mm(rv)} · الفارق {U['revenue_surprise_percent_fq']:+.1f}%", U["revenue_surprise_percent_fq"] >= 0))
    if U.get("earnings_per_share_forecast_next_fq") is not None:
        filas.append(("تقدير الربع المقبل", f"ربحية السهم {U['earnings_per_share_forecast_next_fq']:.2f} $" +
                      (f" · الإيرادات {mm(U['revenue_forecast_next_fq'])}" if U.get("revenue_forecast_next_fq") and len(filas) > 1 else ""), None))
    filas += [(a, b, None) for a, b in (E.get("items") or [])[:max(0, 4 - len(filas))]]
    for i, (tit, txt, up) in enumerate(filas[:4]):
        b = ease((t - i * 0.1) / 0.4); y = 0.62 - i * 0.12
        rect(f, 0.06, y, 0.88, 0.1, NAVY, b); rect(f, 0.935, y, 0.005, 0.1, GOLD if up is None else (TEAL if up else NEG), b)
        T(f, 0.92, y + 0.05, tit, FG, 26, "bold", va="center", alpha=b)
        T(f, 0.68, y + 0.05, txt, MUTED, 20, va="center", alpha=b)
    fuente(f, "تقديرات المحللين ونتيجة المقارنة: " + FUENTE_TV + "." + (" " + E["fuente"] if E.get("fuente") else ""))
    return to_arr(f)


def s_fin(t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, 0.94, 0.86, f"{VJ['ar']} · {VJ['trimestre']}", FG, 44, "bold", alpha=a)
    T(f, 0.94, 0.80, "الخلاصة", GOLD, 30, "bold", alpha=a)
    for i, c in enumerate(VJ["claves"][:3]):
        T(f, 0.94, 0.73 - i * 0.065, "• " + c, FG, 26, alpha=ease((t - 0.1 - i * 0.1) / 0.4))
    b = ease((t - 0.3) / 0.5)
    T(f, 0.94, 0.47, "اكتب لنا في التعليقات: أي شركة تريد أن نحللها بعد ذلك؟ · اشترك وفعّل الجرس", GOLD, 24, "bold", alpha=b)
    T(f, 0.94, 0.42, "قناتنا على تيليغرام: " + TELEGRAM.replace("https://", ""), BLUE, 24, "bold", alpha=b)
    aviso = ("إخلاء مسؤولية: محتوى تعليمي وإعلامي فقط، ولا يُعد توصية استثمارية أو دعوة لشراء أو بيع أي ورقة مالية أو استشارة مالية شخصية. "
             "الأرقام من إفصاحات الشركة لدى هيئة الأوراق المالية والبورصات الأمريكية (SEC) ومن المصادر المذكورة، والحسابات الخاصة موضحة بعبارة «محسوب». "
             "لا نصدر أسعارًا مستهدفة. لا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر، والأداء السابق لا يضمن النتائج. "
             "النص والرسوم والصوت (صوت اصطناعي) من إعداد الذكاء الاصطناعي.")
    T(f, 0.94, 0.33, "\n".join(textwrap.wrap(aviso, 135)), MUTED, 15, linespacing=1.5, alpha=a, va="top")
    return with_logo(to_arr(f), LGB, x=110, y=70)


ESC = [("e_portada", s_portada), ("e_resultados", s_resultados), ("e_ingresos", s_ingresos), ("e_balance", s_balance),
       ("e_flujo", s_flujo), ("e_expectativas", s_expectativas), ("e_fin", s_fin)]
BIG = {"e_portada", "e_fin"}
SUB = {}


def overlay(marcas, leads):
    pie = tira_texto(f"{MARCA} · سلسلة {SERIE} · {MARCA_EN}", GOLD, 18, 46); band = np.array([0x13, 0x29, 0x4B], np.float32)

    def sub(s):
        if s not in SUB: SUB[s] = [tira_texto(l, FG, 27, 50, "bold") for l in (textwrap.wrap(s, 72) or [s])]
        return SUB[s]

    def ov(fr, j, ts, tg):
        fr = fr.copy(); bh = 46
        fr[H - bh:] = (fr[H - bh:].astype(np.float32) * 0.1 + band * 0.9).astype(np.uint8); fr[H - bh - 2:H - bh] = (0xD4, 0xAF, 0x37)
        pegar(fr, pie, (W - pie.shape[1]) // 2, H - bh)
        for a, b, s in marcas[j]:
            if a + leads[j] <= ts < b + leads[j] + 0.25:
                ls = sub(s); h = 50 * len(ls); y0 = H - bh - 16 - h; wmax = max(l.shape[1] for l in ls); x0 = max((W - wmax) // 2 - 24, 0)
                fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48] = (fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48].astype(np.float32) * 0.28 + np.array([11, 26, 46], np.float32) * 0.72).astype(np.uint8)
                for i, l in enumerate(ls): pegar(fr, l, (W - l.shape[1]) // 2, y0 + i * 50)
                break
        return fr
    return ov


def frame(n, fn, t): return fn(t) if n in BIG else with_logo(fn(t), LG, x=60, y=40)


def control():
    """Antes de renderizar: el evento de resultados y las cifras existen, y video.json tiene todo lo que pide la pantalla."""
    err = []
    for k in ("ticker", "ar", "en", "trimestre", "fecha_resultados", "sector", "claves", "voz", "info", "miniatura"):
        if not VJ.get(k): err.append(f"falta {k} en video.json")
    for n, _ in ESC:
        if not V.get(n): err.append(f"falta la locución {n}")
    ev = S.get("evento")
    if not ev: err.append("datos.json sin evento de resultados desde el inicio de la serie")
    else:
        if ev["fecha"] != VJ["fecha_resultados"]: err.append(f"fecha_resultados {VJ['fecha_resultados']} distinta del evento {ev['fecha']}")
        if not ev.get("datos_listos"): err.append("TradingView aún no tiene las cifras del trimestre publicado (datos_listos=false): espera a mañana")
    if len(TRI) < 4: err.append("menos de 4 trimestres con ingresos")
    if not U.get("total_revenue_fq"): err.append("sin ingresos del trimestre")
    for a, b in (VJ.get("expectativas") or {}).get("items", []):
        if not (VJ.get("expectativas") or {}).get("fuente"): err.append("expectativas.items sin fuente"); break
    if err: sys.exit("CONTROL DE CALIDAD:\n- " + "\n- ".join(err))


if __name__ == "__main__":
    control()
    if PREVIEW:
        ov = overlay([[(0, 99, frases(V[n])[0])] for n, _ in ESC], [0] * len(ESC))
        for j, (n, fn) in enumerate(ESC): Image.fromarray(ov(frame(n, fn, 1.0), j, 1.0, 3.0)).save(os.path.join(AUD, f"prev_{n}.png"))
        sys.exit()
    VV = [voz_frases(V[n], AUD) for n, _ in ESC]; sr = VV[0][1]; motor = VV[0][3]
    if len({v[1] for v in VV}) > 1 or len({v[3] for v in VV}) > 1: sys.exit("voces mezcladas")
    durs = [0.15 + len(a) / sr + 0.6 for a, _, _, _ in VV]; durs[-1] += 1.5
    print("voz", motor, "duración prevista", round(sum(durs), 1))
    if not MIN_S <= sum(durs) <= MAX_S: sys.exit(f"Duración {sum(durs):.0f} s fuera de {MIN_S}-{MAX_S} s: acorta o alarga la locución")
    leads = [0.15] * len(ESC)
    times, t0 = render([lambda t, n=n, fn=fn: frame(n, fn, t) for n, fn in ESC], durs, ([v[0] for v in VV], leads), sr, W, H, 30, OUT,
                       os.path.join(AUD, "ep-silent.mp4"), os.path.join(AUD, "ep.wav"), overlay=overlay([v[2] for v in VV], leads))
    json.dump([(n, tt) for (n, _), tt in zip(ESC, times)] + [("_total", round(t0, 2)), ("_voz", motor)], open(f"{DIR}/times.json", "w"))
    with open(f"{DIR}/guion-{BASE}-Nabd.md", "w") as g:
        g.write(f"# {SERIE}: {VJ['en']} ({VJ['ticker']}) · {VJ['trimestre']}\n\nVoz: {motor} · duración {t0:.0f} s\n\n| tiempo | escena | narración |\n|---|---|---|\n")
        for (n, _), tt in zip(ESC, times): g.write(f"| {int(tt) // 60}:{int(tt) % 60:02d} | {n} | {V[n]} |\n")
    print("listo", round(t0, 1), "s", OUT)
