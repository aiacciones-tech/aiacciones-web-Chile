# Episodio de la serie «عمالقة وول ستريت» (Nabd Wall Street): una empresa tras su informe de resultados, 1920x1080, máximo 4 minutos
# (Daniel, 13-nov-2026). 7 escenas: portada, resultados del trimestre, ingresos y margen (8 trimestres), balance y deuda/caja frente a la
# capitalización, flujo de caja de 12 meses, frente a las expectativas y la guía, y cierre. Los gráficos salen de sec.json (SEC XBRL, rama
# datos-serie20-nabd); lo que aún no está en XBRL (el trimestre recién publicado) lo añade video.json desde el comunicado (EX-99.1).
# Uso: AUD=<scratch> [VOZ_DIR=<wav de Azure>] python3 make_episodio.py <carpeta del episodio> [preview]
#   La carpeta tiene video.json y sec.json. Escribe serie20-<ticker>-<fecha>-Nabd.mp4, times.json y guion-<...>-Nabd.md.
import os, sys, json, textwrap, datetime as dt, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from comun import *

DIR = os.path.abspath(sys.argv[1]); PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
AUD = os.environ.get("AUD", "aud"); os.makedirs(AUD, exist_ok=True)
VJ = json.load(open(f"{DIR}/video.json")); S = json.load(open(f"{DIR}/sec.json")); V = VJ["voz"]
SERIE = "عمالقة وول ستريت"; NAVY = "#13294B"; W, H = 1920, 1080
MIN_S, MAX_S = 120, 240   # máximo 4 minutos (Daniel, 13-nov-2026)
BASE = f"serie20-{VJ['ticker'].lower()}-{VJ['fecha_resultados']}"
OUT = f"{DIR}/{BASE}-Nabd.mp4"
MESES = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
fecha_ar = lambda s: (lambda d: f"{d.day} {MESES[d.month - 1]} {d.year}")(dt.date.fromisoformat(s))
LG = load_logo(130); LGB = load_logo(230)
SECS = ["المقدمة", "النتائج", "الإيرادات والهامش", "الميزانية", "التدفقات النقدية", "التوقعات", "الخلاصة"]


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


# Trimestres: XBRL + el trimestre nuevo del comunicado si aún no está
TRI = [dict(t) for t in S.get("trimestres", [])]
for n in VJ.get("trimestres_nuevos", []):
    TRI = [t for t in TRI if t["fin"] != n["fin"]] + [dict(n, _comunicado=True)]
TRI = sorted(TRI, key=lambda t: t["fin"])[-8:]
BAL = dict((S.get("balance") or [{}])[-1]); BAL.update(VJ.get("balance_nuevo") or {})
CAP = VJ.get("cap_mercado") or S.get("cap_mercado")


def lbl_tri(fin):
    d = dt.date.fromisoformat(fin); return f"{MESES[d.month - 1][:5]}\n{d.year}"


def s_portada(t):
    f = fig(W, H); a = ease(t / 0.6)
    T(f, 0.94, 0.88, MARCA + " · سلسلة " + SERIE, GOLD, 30, "bold", alpha=a)
    rect(f, 0, 0.66, 1.0, 0.17, GOLD, a)
    T(f, 0.94, 0.745, VJ["ar"], BG, 88, "bold", va="center", alpha=a)
    f.text(0.06, 0.745, VJ["ticker"], color=BG, fontsize=64, weight="bold", ha="left", va="center", alpha=a)
    T(f, 0.94, 0.55, VJ["trimestre"], FG, 42, "bold", alpha=ease((t - 0.15) / 0.5))
    T(f, 0.94, 0.48, f"إعلان النتائج: {fecha_ar(VJ['fecha_resultados'])} · {VJ['sector']}", MUTED, 28, alpha=ease((t - 0.25) / 0.5))
    if VJ.get("titular"): T(f, 0.94, 0.33, VJ["titular"], BLUE, 34, "bold", alpha=ease((t - 0.35) / 0.5))
    return with_logo(to_arr(f), LGB, x=110, y=40)


def s_resultados(t):
    f = base(2, "نتائج الربع", VJ.get("titulo_resultados", "أهم أرقام " + VJ["trimestre"]))
    K = VJ["kpis"][:4]
    for i, (lab, big, sub, c) in enumerate(K):
        b = ease((t - i * 0.12) / 0.4); x0 = 0.94 - (i + 1) * 0.215 + 0.01
        rect(f, x0, 0.36, 0.2, 0.36, NAVY, b); rect(f, x0, 0.715, 0.2, 0.006, GOLD, b)
        T(f, x0 + 0.185, 0.655, lab, MUTED, 24, "bold", alpha=b)
        T(f, x0 + 0.185, 0.53, big, col(c) if c else FG, 40 if len(big) <= 14 else 32, "bold", alpha=b)
        T(f, x0 + 0.185, 0.42, sub, FG, 20, alpha=b, va="center")
    fuente(f, VJ.get("fuente_kpis", "بيان النتائج المودع لدى SEC (8-K، المرفق 99.1). التغيرات محسوبة."))
    return to_arr(f)


def s_ingresos(t):
    f = base(3, "الإيرادات وهامش صافي الربح", VJ.get("titulo_ingresos", "آخر ثمانية أرباع"))
    X = [x for x in TRI if x.get("ingresos")]; ee = ease(t)
    if X:
        ax = f.add_axes([0.08, 0.27, 0.84, 0.46]); clean(ax); i = np.arange(len(X)); v = [x["ingresos"] / 1e9 for x in X]
        ax.bar(i, [y * ee for y in v], color=[GOLD if j == len(X) - 1 else BLUE for j in range(len(X))], width=0.6)
        ax.set_xticks(i, [lbl_tri(x["fin"]) for x in X]); ax.set_yticks([]); ax.set_ylim(0, max(v) * 1.35); ax.tick_params(labelsize=15)
        if t > 0.5:
            for j, y in zip(i, v): ax.text(j, y * ee + max(v) * 0.03, f"{y:,.1f}", ha="center", color=FG, fontsize=17, weight="bold")
        mg = [(j, x["beneficio_neto"] / x["ingresos"] * 100) for j, x in zip(i, X) if x.get("beneficio_neto") is not None]
        if mg and t > 0.4:
            a2 = ax.twinx(); clean(a2); a2.set_yticks([])
            a2.plot([m[0] for m in mg], [m[1] for m in mg], color=TEAL, lw=3, marker="o", ms=9)
            lo, hi = min(m[1] for m in mg), max(m[1] for m in mg); a2.set_ylim(lo - (hi - lo + 5) * 2.2, hi + (hi - lo + 5) * 0.4)
            for j, m in mg: a2.text(j, m + (hi - lo + 5) * 0.12, f"{m:.0f}%", ha="center", color=TEAL, fontsize=15, weight="bold")
        T(f, 0.92, 0.745, "الأعمدة: الإيرادات الفصلية (مليار $) · الخط الأخضر: هامش صافي الربح (محسوب)", MUTED, 18)
    nota = "SEC EDGAR XBRL (10-Q و 10-K)" + ("، والربع الأخير من بيان النتائج (8-K)" if any(x.get("_comunicado") for x in X) else "") + \
           ". الربع الرابع وبعض التدفقات محسوبة من الأرقام المتراكمة. الهامش = صافي الربح ÷ الإيرادات (محسوب)."
    fuente(f, nota)
    return to_arr(f)


def s_balance(t):
    f = base(4, "الميزانية العمومية", VJ.get("titulo_balance", "النقد والديون وحقوق المساهمين"))
    caja = (BAL.get("caja") or 0) + (BAL.get("inversiones_cp") or 0)
    deuda = sum(BAL.get(k) or 0 for k in ("deuda_lp", "deuda_cp", "papel_comercial"))
    items = [("النقد والاستثمارات قصيرة الأجل", mm(caja) if caja else "—", BLUE),
             ("الديون (طويلة وقصيرة الأجل)", mm(deuda) if deuda else "—", NEG),
             ("حقوق المساهمين", mm(BAL.get("patrimonio")), TEAL)]
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
    fuente(f, f"SEC EDGAR XBRL، الميزانية في {BAL.get('fin', '—')}" + (" (أو بيان النتائج)" if VJ.get("balance_nuevo") else "") +
           f". القيمة السوقية: TradingView ({str(S.get('cap_fecha', ''))[:10]}). النسب محسوبة وليست حكمًا شرعيًا ولا توصية.")
    return to_arr(f)


def s_flujo(t):
    f = base(5, "التدفقات النقدية · آخر 12 شهرًا (محسوب)", VJ.get("titulo_flujo", "من أين يأتي النقد وأين يذهب"))
    U = TRI[-4:]
    tot = lambda k: sum(x[k] for x in U) if U and all(x.get(k) is not None for x in U) else None
    fo, cx, dv, rc = tot("flujo_operativo"), tot("capex"), tot("dividendos"), tot("recompras")
    fl = fo - cx if fo is not None and cx is not None else None
    L = [(l, v, c) for l, v, c in [("التدفق النقدي التشغيلي", fo, TEAL), ("الإنفاق الرأسمالي", cx, NEG), ("التدفق النقدي الحر", fl, GOLD),
                                   ("التوزيعات النقدية", dv, BLUE), ("إعادة شراء الأسهم", rc, BLUE)] if v is not None]
    if L:
        ax = f.add_axes([0.08, 0.27, 0.62, 0.48]); clean(ax); y = np.arange(len(L))[::-1]; ee = ease(t); mx = max(abs(v) for _, v, _ in L)
        ax.barh(y, [abs(v) * ee for _, v, _ in L], color=[c for _, _, c in L], height=0.6); ax.set_xlim(mx * 1.3, 0)
        ax.set_yticks([]); ax.set_xticks([])
        for yy, (l, v, c) in zip(y, L):
            ax.text(-0.01, yy, ar(l), transform=ax.get_yaxis_transform(), ha="left", va="center", color=FG, fontsize=22, weight="bold")
            if t > 0.5: ax.text(abs(v) * ee + mx * 0.02, yy, ar(mm(v)), ha="right", va="center", color=FG, fontsize=18, weight="bold")
    else:
        T(f, 0.94, 0.5, "لا تتوفر بيانات التدفقات النقدية الفصلية الكاملة في XBRL", MUTED, 28)
    fuente(f, "SEC EDGAR XBRL: مجموع آخر أربعة أرباع (محسوب). التدفق النقدي الحر = التدفق التشغيلي ناقص الإنفاق الرأسمالي (محسوب).")
    return to_arr(f)


def s_expectativas(t):
    E = VJ["expectativas"]
    f = base(6, "مقارنةً بالتوقعات وتوجيهات الإدارة", E.get("titulo", "ماذا قالت الأرقام والإدارة"))
    for i, (tit, txt) in enumerate(E["items"][:4]):
        b = ease((t - i * 0.1) / 0.4); y = 0.62 - i * 0.12
        rect(f, 0.06, y, 0.88, 0.1, NAVY, b); rect(f, 0.935, y, 0.005, 0.1, GOLD, b)
        T(f, 0.92, y + 0.05, tit, FG, 26, "bold", va="center", alpha=b)
        T(f, 0.62, y + 0.05, txt, MUTED, 20, va="center", alpha=b)
    fuente(f, E["fuente"])
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
    """Antes de renderizar: los datos que se muestran existen y el guion no inventa (las cifras de pantalla vienen de sec.json o del comunicado)."""
    err = []
    for k in ("ticker", "ar", "trimestre", "fecha_resultados", "sector", "kpis", "expectativas", "claves", "voz", "fuente_kpis"):
        if not VJ.get(k): err.append(f"falta {k} en video.json")
    for n, _ in ESC:
        if not V.get(n): err.append(f"falta la locución {n}")
    if len(VJ.get("kpis", [])) < 3: err.append("kpis: 3 o 4")
    if not [x for x in TRI if x.get("ingresos")]: err.append("sin ingresos trimestrales (sec.json ni trimestres_nuevos)")
    if not S.get("evento"): err.append("sec.json sin evento de resultados")
    elif S["evento"]["fecha"] != VJ["fecha_resultados"]: err.append(f"fecha_resultados {VJ['fecha_resultados']} distinta del evento SEC {S['evento']['fecha']}")
    for x in VJ.get("trimestres_nuevos", []):
        if not x.get("fuente"): err.append(f"trimestres_nuevos {x.get('fin')}: falta la fuente")
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
