# Video diario largo (8-10 min) en árabe de Wall Street para Nabd Wall Street, según el manual de producción de Daniel (10-nov-2026):
# 8 secciones (introducción, los grandes índices, sectores, cinco acciones, macro, análisis técnico con escenarios, agenda y despedida con Telegram),
# ticker inferior con cotizaciones y titulares, y subtítulos árabes frase a frase. 1080p, logo Nabd.
# Voz: Azure ar-SA-HamedNeural si VOZ_DIR tiene sus wav (voz-Nabd.yml); si no, Piper ar_JO-kareem.
# Uso: AUD=<scratch> [VOZ_DIR=<wav de Azure>] python3 make_video.py <carpeta del día> [preview]
#   La carpeta del día tiene mercado.json y video.json (ver ejemplo-2026-11-09/). Escribe video-bolsa-<fecha>-Nabd.mp4, times.json,
#   guion-<fecha>-Nabd.md (guion en tabla: tiempo, narración, visual, datos) y datos-<fecha>-Nabd.csv (datos usados, con fuente y hora).
import os, sys, json, re, csv, textwrap, numpy as np, datetime as dt
from zoneinfo import ZoneInfo
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun import *
from tecnico import calc, accion, INDICE, INDICE_CORTO, MESES, DIAS, TZ, fecha_ar
DIR = os.path.abspath(sys.argv[1]); PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
W, H, FPS = 1920, 1080, 30
AUD = os.environ.get("AUD", "aud")
MIN_S, MAX_S = 450, 630   # duración: entre 7:30 y 10:30 (objetivo 8-10 minutos)
M = json.load(open(f"{DIR}/mercado.json")); VJ = json.load(open(f"{DIR}/video.json"))
R, A = calc(M, VJ.get("nombres")); NYZ = ZoneInfo("America/New_York"); FECHA = dt.date.fromisoformat(R["fecha"]); FECHA_TXT = fecha_ar(FECHA)
OUT = f"{DIR}/video-bolsa-{R['fecha']}-Nabd.mp4"
SECS = ["المقدمة", "المؤشرات الرئيسية", "القطاعات", "أسهم اليوم", "الاقتصاد الكلي", "التحليل الفني", "ماذا ننتظر غدًا", "الختام"]; NS = len(SECS)
LG = load_logo(130); LGS = load_logo(95); LGB = load_logo(230)
NB = 126  # unos 6 meses de sesiones
TV_TXT = "TradingView"
NAVY = "#13294B"
corto = lambda d: f"{d.day} {MESES[d.month - 1]}"
fiso = lambda s: re.sub(r"(\d{4})-(\d{2})-(\d{2})", lambda m: corto(dt.date(int(m[1]), int(m[2]), int(m[3]))) + (f" {m[1]}" if int(m[1]) != FECHA.year else ""), s)
cc_ = lambda v: TEAL if (v or 0) >= 0 else NEG


def millones(v):
    if v is None: return "—"
    return f"{v / 1e9:,.2f} مليار" if v >= 1e9 else f"{v / 1e6:,.1f} مليون"


def T(f, x, y, s, c=FG, fs=24, w="normal", ha="right", **k):
    return f.text(x, y, ar(s), color=c, fontsize=fs, weight=w, ha=ha, **k)


def base_fig(n, kicker, title, sub):
    f = fig(W, H)
    T(f, 0.94, 0.905, kicker, GOLD, 24, "bold")
    T(f, 0.94, 0.82, title, FG, 42 if len(title) <= 50 else 36, "bold")
    T(f, 0.105, 0.925, f"{n}/{NS} · {SECS[n - 1]}", MUTED, 19, "bold", ha="left")
    T(f, 0.105, 0.89, MARCA + " · " + PROGRAMA + " · " + FECHA_TXT, DIM, 16, "bold", ha="left")
    w = 0.88 / NS
    for i in range(NS):  # barra de progreso de derecha a izquierda
        f.patches.append(plt.Rectangle((0.94 - (i + 1) * w + 0.008, 0.975), w - 0.008, 0.008, transform=f.transFigure, color=GOLD if i < n else DIM, figure=f))
    T(f, 0.94, 0.172, "\n".join(textwrap.wrap(sub, 160)), MUTED, 14, linespacing=1.35)
    return f


def rect(f, x, y, w, h, c, a=1.0):
    f.patches.append(plt.Rectangle((x, y), w, h, transform=f.transFigure, color=c, alpha=a, figure=f))


def hbars(f, box, labels, vals, colors, fmt=pct, e=1.0, fs=19, extra=None):
    """Barras horizontales (etiquetas árabes a la derecha). extra: texto pequeño junto a cada valor."""
    ax = f.add_axes(box); clean(ax); y = np.arange(len(vals))[::-1]
    lim = max(abs(min(vals + [0])), abs(max(vals + [0]))) * 1.9 or 1
    ax.barh(y, [v * e for v in vals], color=colors, height=0.62)
    ax.set_yticks([]); ax.set_xticks([]); ax.axvline(0, color=DIM, lw=1.5)
    ax.set_xlim(-lim if min(vals) < 0 else -lim * 0.3, lim if max(vals) > 0 else lim * 0.3); ax.set_ylim(-0.7, len(vals) - 0.3)
    for i, (yy, v) in enumerate(zip(y, vals)):
        ax.text(1.01, yy, ar(labels[i]), transform=ax.get_yaxis_transform(), ha="left", va="center", color=FG, fontsize=fs, weight="bold")
        if e > 0.6:
            ax.text(v * e + (lim * 0.03 if v >= 0 else -lim * 0.03), yy, fmt(v), va="center",
                    ha="left" if v >= 0 else "right", color=FG, fontsize=fs - 2, weight="bold")
            if extra and extra[i]:
                ax.text(-0.03, yy, ar(extra[i]), transform=ax.get_yaxis_transform(), ha="right", va="center", color=MUTED, fontsize=fs - 4)
    return ax


# ---------- 1. Introducción ----------
def s_title(t):
    f = fig(W, H); a = ease(t / 0.6); r = R["spx"]; cc = cc_(r["var_pct"])
    T(f, 0.94, 0.895, MARCA + " · " + PROGRAMA + " لوول ستريت", GOLD, 28, "bold", alpha=a)
    rect(f, 0, 0.71, 1.0, 0.135, GOLD, a)
    T(f, 0.94, 0.775, "جلسة " + FECHA_TXT, BG, 64, "bold", va="center", alpha=a)
    T(f, 0.94, 0.625, INDICE["spx"], MUTED, 30, "bold", alpha=a)
    f.text(0.94, 0.52, num(r["cierre"]), color=FG, fontsize=86, weight="bold", ha="right", alpha=a)
    f.text(0.94, 0.45, f"{pct(r['var_pct'])}   ({r['var_pts']:+,.2f})", color=cc, fontsize=36, weight="bold", ha="right", alpha=a)
    for i, k in enumerate(("ndx", "dji", "rut")):
        if k not in R: continue
        b = ease((t - 0.15 - i * 0.1) / 0.5); x_ = R[k]; y = 0.375 - i * 0.055
        T(f, 0.94, y, INDICE_CORTO[k], MUTED, 25, "bold", alpha=b)
        f.text(0.78, y, f"{num(x_['cierre'])}   {pct(x_['var_pct'])}", color=cc_(x_["var_pct"]), fontsize=26, weight="bold", ha="right", alpha=b)
    I = [v for v in M.get("spx_intradia", {}).get("velas", []) if dt.datetime.fromtimestamp(v["t"], NYZ).date() == FECHA]
    I = [v for v in I if dt.time(9, 30) <= dt.datetime.fromtimestamp(v["t"], NYZ).time() < dt.time(16, 0)]
    IC = np.array([v["c"] for v in I]); prev = r["anterior"]
    if len(IC) > 2:
        IC = np.append(IC, r["cierre"])
        ax = f.add_axes([0.06, 0.29, 0.48, 0.33]); clean(ax)
        n = max(2, int(len(IC) * ease(t))); x = np.arange(len(IC))
        ax.plot(x[:n], IC[:n], color=cc, lw=3.5); ax.axhline(prev, color=DIM, lw=1.5, ls="--")
        ax.fill_between(x[:n], IC[:n], prev, color=cc, alpha=0.12)
        pad = (max(IC.max(), prev) - min(IC.min(), prev)) * 0.15
        ax.set_xlim(0, len(IC) - 1); ax.set_ylim(min(IC.min(), prev) - pad, max(IC.max(), prev) + pad); ax.set_yticks([])
        hrs = [dt.datetime.fromtimestamp(v["t"], TZ) for v in I]; tk = [j for j, h in enumerate(hrs) if h.minute == 30]
        ax.set_xticks(tk, [hrs[j].strftime("%H:%M") for j in tk]); ax.tick_params(labelsize=15)
        T(f, 0.54, 0.635, "حركة إس آند بي 500 خلال الجلسة (كل 5 دقائق، بتوقيت مكة المكرمة)", MUTED, 18)
        T(f, 0.06, 0.245, "الخط المتقطع: الإغلاق السابق " + num(prev), MUTED, 16, ha="left")
    if VJ.get("titular"): T(f, 0.94, 0.18, VJ["titular"], BLUE, 29, "bold", alpha=ease((t - 0.3) / 0.5))
    return with_logo(to_arr(f), LG, x=60, y=40)


# ---------- 2. Los grandes índices ----------
def s_indices(t):
    J = VJ.get("indices", {})
    f = base_fig(2, "المؤشرات الرئيسية: الإغلاق والأداء", J.get("titulo", "أداء المؤشرات الأمريكية"),
                 J.get("fuente", f"الأسعار: {TV_TXT} (إغلاق {R['fecha']} في نيويورك). التغير الأسبوعي والمسافة عن القمة والمتوسطات والاتجاه: محسوبة. "
                       "الاتجاه وصف لموقع السعر من متوسطات 20 و50 و200 جلسة، وليس توقعًا."))
    cols = [(0.70, "الإغلاق"), (0.575, "اليوم"), (0.465, "الأسبوع"), (0.34, "عن أعلى مستوى"), (0.215, "عن متوسط 200"), (0.095, "الاتجاه")]
    T(f, 0.94, 0.70, "المؤشر", MUTED, 20, "bold")
    for x, h in cols: T(f, x, 0.70, h, MUTED, 20, "bold", ha="center")
    rect(f, 0.05, 0.685, 0.90, 0.003, GOLD)
    for i, k in enumerate(("spx", "ndx", "dji", "rut")):
        if k not in R: continue
        b = ease((t - i * 0.12) / 0.4)
        if b <= 0: continue
        r = R[k]; y = 0.605 - i * 0.1
        if i % 2 == 0: rect(f, 0.05, y - 0.04, 0.90, 0.088, NAVY, 0.55 * b)
        T(f, 0.94, y, INDICE_CORTO[k], GOLD if k != "rut" else FG, 27, "bold", va="center", alpha=b)
        vals = [(num(r["cierre"]), FG), (pct(r["var_pct"]), cc_(r["var_pct"])),
                ("—" if r.get("semana_pct") is None else pct(r["semana_pct"]), cc_(r.get("semana_pct"))),
                (pct(r["dist_max_hist_pct"]), cc_(r["dist_max_hist_pct"]) if r["dist_max_hist_pct"] < -0.05 else TEAL),
                (pct(r["dist_sma200_pct"], 1), cc_(r["dist_sma200_pct"]))]
        for (x, _), (v, c) in zip(cols, vals): f.text(x, y + 0.008, v, color=c, fontsize=26, weight="bold", ha="center", va="center", alpha=b)
        T(f, cols[3][0], y - 0.03, ("قمة تاريخية " if r["max_hist_es_historico"] else "أعلى منذ " + r["historia_desde"][:4] + " · ") + fiso(r["max_hist_fecha"]),
          MUTED, 13, ha="center", va="center", alpha=b)
        tc = TEAL if r["tendencia"].startswith("صاعد") else (GOLD if r["tendencia"] == "عرضي" else NEG)
        T(f, cols[5][0], y, r["tendencia"], tc, 21, "bold", ha="center", va="center", alpha=b)
    if J.get("nota"): T(f, 0.94, 0.215, J["nota"], BLUE, 22, "bold", alpha=ease((t - 0.5) / 0.4))
    return to_arr(f)


def s_grandes(t):
    J = VJ.get("grandes", {}); e = ease(t / 0.8)
    f = base_fig(2, "كبار التكنولوجيا ومكونات داو جونز", J.get("titulo", "من حرّك المؤشرات اليوم؟"),
                 J.get("fuente", f"التغير: {TV_TXT}. مساهمة كل سهم في داو جونز بالنقاط = تغيره بالدولار ÷ قاسم المؤشر (محسوب من بيانات اليوم)."))
    G = R.get("ndx_grandes") or []
    T(f, 0.94, 0.725, "أكبر شركات ناسداك 100 (بالقيمة السوقية)", GOLD, 22, "bold")
    if G: hbars(f, [0.60, 0.25, 0.17, 0.45], [g["nombre"] for g in G], [g["cambio"] for g in G], [cc_(g["cambio"]) for g in G], e=e, fs=18)
    DA = R.get("dow_aportes")
    T(f, 0.47, 0.725, "داو جونز: أكبر المساهمين (نقاط)", GOLD, 22, "bold")
    if DA:
        L = DA["valores"][:4] + DA["valores"][-3:]
        hbars(f, [0.12, 0.25, 0.19, 0.45], [x["nombre"] for x in L], [x["puntos"] for x in L], [cc_(x["puntos"]) for x in L],
              fmt=lambda v: f"{v:+,.0f}", e=e, fs=18)
    elif J.get("dow_txt"):
        T(f, 0.47, 0.6, "\n".join(textwrap.wrap(J["dow_txt"], 45)), FG, 22, va="top", linespacing=1.4)
    return to_arr(f)


def s_news(t):
    N_ = VJ["noticias"]; f = base_fig(2, "لماذا تحركت السوق؟", N_["titulo"], N_["fuente"]); pal = [GOLD, TEAL, BLUE, NEG, FG]
    for i, (tag, txt) in enumerate(N_["items"][:5]):
        b = ease((t - i * 0.15) / 0.4)
        if b <= 0: continue
        y = 0.68 - i * 0.105; cc = pal[i % 5]
        rect(f, 0.945, y - 0.035, 0.006, 0.08, cc, b)
        T(f, 0.93, y + 0.012, tag, cc, 26, "bold", alpha=b)
        T(f, 0.93, y - 0.03, txt, FG, 23 if len(txt) <= 100 else 20, alpha=b)
    return to_arr(f)


# ---------- 3. Sectores ----------
def s_sectores(t):
    J = VJ.get("sectores", {}); S = R.get("sectores") or []; e = ease(t / 0.8)
    f = base_fig(3, "تحليل القطاعات: صناديق SPDR القطاعية", J.get("titulo", "أداء القطاعات"),
                 J.get("fuente", f"التغير اليومي والأسبوعي لصناديق XLK وXLF وXLE وXLV وXLY وXLI: {TV_TXT} (إغلاق {R['fecha']})."))
    if S:
        cols = [(TEAL if s["cambio"] >= 0 else NEG) if (i < 2 or i >= len(S) - 2) else DIM for i, s in enumerate(S)]
        hbars(f, [0.14, 0.25, 0.22, 0.46], [f"{s['nombre']} {s['simbolo']}" for s in S], [s["cambio"] for s in S], cols, e=e, fs=19,
              extra=[("5 أيام " + pct(s["semana"], 1)) if s.get("semana") is not None else "" for s in S])
        T(f, 0.36, 0.725, "التغير اليومي (وآخر 5 أيام)", MUTED, 18)
    for i, it in enumerate(J.get("items", [])[:4]):
        b = ease((t - 0.3 - i * 0.12) / 0.4)
        if b <= 0: continue
        a_, b_, c_ = (it + ["fg"])[:3]; y = 0.68 - i * 0.15
        T(f, 0.94, y, a_, col(c_), 25, "bold", alpha=b)
        T(f, 0.94, y - 0.03, "\n".join(textwrap.wrap(b_, 44)[:3]), MUTED, 19, va="top", linespacing=1.3, alpha=b)
    return to_arr(f)


# ---------- 4. Cinco acciones ----------
def s_accion(i, t):
    J = VJ["acciones"][i]; a = accion(M, J["ticker"], VJ.get("nombres")); e = ease(t / 0.8)
    f = base_fig(4, f"أسهم اليوم · {i + 1}/5", f"{a['nombre']} ({a['ticker']})",
                 J.get("fuente", f"السعر والحجم: {TV_TXT} (إغلاق {R['fecha']}). الحجم مقابل متوسط 10 جلسات: محسوب. الخبر: المصادر المذكورة."))
    cc = cc_(a["cambio"])
    T(f, 0.94, 0.735, a["nombre_en"], MUTED, 22, "bold")
    f.text(0.94, 0.655, num(a["cierre"]) + " $", color=FG, fontsize=60, weight="bold", ha="right")
    f.text(0.94, 0.6, f"{pct(a['cambio'])}   ({a['cambio_abs']:+,.2f})", color=cc, fontsize=32, weight="bold", ha="right")
    fil = [("حجم التداول", millones(a["volumen"]) + " سهم"), ("مقابل متوسط 10 جلسات", f"×{a['vol_rel']:.1f}" if a.get("vol_rel") else "—"),
           ("قيمة التداول", millones(a["valor_usd"]) + " دولار")]
    for j, (l, v) in enumerate(fil):
        y = 0.545 - j * 0.036; T(f, 0.94, y, l, MUTED, 18); T(f, 0.76, y, v, FG, 19, "bold")
    b = ease((t - 0.25) / 0.4); y = 0.425
    T(f, 0.94, y, "الخبر", GOLD, 20, "bold", alpha=b); L1 = textwrap.wrap(J["noticia"], 46)
    T(f, 0.94, y - 0.03, "\n".join(L1), FG, 19, va="top", linespacing=1.3, alpha=b); y -= 0.065 + 0.033 * len(L1)
    c2 = ease((t - 0.45) / 0.4)
    T(f, 0.94, y, "القراءة", BLUE, 20, "bold", alpha=c2)
    T(f, 0.94, y - 0.03, "\n".join(textwrap.wrap(J["lectura"], 50)[:2]), MUTED, 18, va="top", linespacing=1.3, alpha=c2)
    V = [v for v in (a.get("velas") or []) if fecha_vela_(v["t"]) <= FECHA][-60:]
    if len(V) > 10:
        o, hi, lo, c, vol = (np.array([v[k] if v.get(k) is not None else np.nan for v in V], float) for k in "ohlcv")
        n = len(V); m = max(2, int(n * e)); span = np.nanmax(hi) - np.nanmin(lo)
        ax = f.add_axes([0.05, 0.36, 0.42, 0.38]); clean(ax)
        for j in range(m):
            k = TEAL if c[j] >= o[j] else NEG
            ax.vlines(j, lo[j], hi[j], color=k, lw=1.3); ax.add_patch(plt.Rectangle((j - 0.35, min(o[j], c[j])), 0.7, max(abs(c[j] - o[j]), span * 0.003), color=k))
        ax.set_xlim(-1, n); ax.set_ylim(np.nanmin(lo) - span * 0.05, np.nanmax(hi) + span * 0.05); ax.yaxis.tick_right(); ax.tick_params(axis="y", labelsize=14)
        dd = [fecha_vela_(v["t"]) for v in V]; tk = [j for j in range(3, n) if dd[j].month != dd[j - 1].month]
        ax.set_xticks(tk, [ar(MESES[dd[j].month - 1]) for j in tk]); ax.tick_params(axis="x", labelsize=15)
        ax2 = f.add_axes([0.05, 0.24, 0.42, 0.10]); clean(ax2); ax2.patch.set_alpha(0); ax2.set_zorder(-1)
        ax2.bar(np.arange(m), np.nan_to_num(vol[:m]), color=[TEAL if c[j] >= o[j] else NEG for j in range(m)], alpha=0.75, width=0.7)
        ax2.set_xlim(-1, n); ax2.set_xticks([]); ax2.set_yticks([])
        T(f, 0.47, 0.75, "شموع يومية لآخر 3 أشهر وحجم التداول", MUTED, 17)
    return to_arr(f)


def fecha_vela_(t): return dt.datetime.fromtimestamp(t, dt.timezone.utc).date()


# ---------- 5. Macro ----------
def s_macro(t):
    J = VJ.get("macro", {}); X = R.get("macro") or []
    f = base_fig(5, "المؤشرات الاقتصادية والأسواق", J.get("titulo", "السندات والدولار والتقلب والنفط والذهب"),
                 J.get("fuente", f"{TV_TXT}: عائد السندات لعشر سنوات (TVC:US10Y، التغير بنقاط الأساس)، DXY، VIX، النفط الأمريكي WTI (TVC:USOIL) والذهب. "
                       f"آخر إغلاق حتى {R['fecha']}؛ الخط: آخر 15 جلسة."))
    w = 0.88 / max(len(X), 1)
    for i, x in enumerate(X):
        b = ease((t - i * 0.1) / 0.4)
        if b <= 0: continue
        x1 = 0.94 - i * w; x0 = x1 - w + 0.012; up = x["cambio_pct"] >= 0; cc = TEAL if up else NEG
        rect(f, x0, 0.42, w - 0.012, 0.32, NAVY, 0.6 * b)
        T(f, x1 - 0.01, 0.705, x["nombre"], GOLD, 20, "bold", alpha=b)
        val = (f"{x['cierre']:.3f}%" if x["unidad"] == "%" else num(x["cierre"]))
        f.text(x1 - 0.01, 0.635, val, color=FG, fontsize=36, weight="bold", ha="right", alpha=b)
        ch = f"{x['cambio_pb']:+.1f} نقطة أساس" if x.get("cambio_pb") is not None else pct(x["cambio_pct"])
        T(f, x1 - 0.01, 0.59, ch, cc, 20, "bold", alpha=b)
        if not x["mismo_dia"]: T(f, x1 - 0.01, 0.56, "آخر إغلاق " + fiso(x["fecha"]), MUTED, 13, alpha=b)
        ax = f.add_axes([x0 + 0.01, 0.44, w - 0.035, 0.1]); clean(ax); s = np.array(x["serie"])
        ax.plot(np.arange(len(s)), s, color=cc, lw=2.5, alpha=b); ax.fill_between(np.arange(len(s)), s, s.min(), color=cc, alpha=0.12 * b)
        ax.set_xticks([]); ax.set_yticks([])
        txt = (J.get("items") or {}).get(x["simbolo"])
        if txt: T(f, x1 - 0.01, 0.40, "\n".join(textwrap.wrap(txt, 30)[:3]), MUTED, 16, va="top", linespacing=1.3, alpha=b)
    if J.get("golfo"):
        c2 = ease((t - 0.5) / 0.4); rect(f, 0.06, 0.235, 0.88, 0.07, GOLD, 0.15 * c2)
        T(f, 0.93, 0.27, "النفط واقتصادات الخليج: " + J["golfo"], GOLD, 20 if len(J["golfo"]) < 110 else 17, "bold", va="center", alpha=c2)
    return to_arr(f)


# ---------- 6. Técnico ----------
def s_tech(k, t):
    TJ = VJ["tecnico"][k]; r = R[k]; a_ = A[k]; vr = r["volumen_vs_media10_pct"]
    f = base_fig(6, "التحليل الفني · " + INDICE[k], TJ["titulo"],
                 f"شموع يومية لآخر 6 أشهر من {TV_TXT} ({r['sesiones']} جلسة منذ {r['historia_desde'][:4]}). المتوسطات المتحركة 20 و50 و200 جلسة و RSI 14 "
                 "والدعوم والمقاومات (قمم وقيعان حديثة) وحجم التداول مقابل متوسط 10 جلسات: محسوبة. هذه بيانات وليست إشارات شراء أو بيع.")
    dates, o, hi, lo, c, vol = (a_[x] for x in ("dates", "o", "hi", "lo", "c", "vol"))
    n = len(c); idx = np.arange(n - NB, n); x = np.arange(NB); m = max(2, int(NB * ease(t / 0.8)))
    hay_vol = np.isfinite(vol[idx]).sum() > NB * 0.8
    ax = f.add_axes([0.05, 0.44 if hay_vol else 0.36, 0.56, 0.31 if hay_vol else 0.39]); clean(ax)
    span = hi[idx].max() - lo[idx].min()
    for j in range(m):
        i = idx[j]; cc = TEAL if c[i] >= o[i] else NEG
        ax.vlines(j, lo[i], hi[i], color=cc, lw=1.2); ax.add_patch(plt.Rectangle((j - 0.35, min(o[i], c[i])), 0.7, max(abs(c[i] - o[i]), span * 0.002), color=cc))
    for S_, col_, lab in ((a_["S20"], FG, "متوسط 20"), (a_["S50"], BLUE, "متوسط 50"), (a_["S200"], GOLD, "متوسط 200")):
        ax.plot(x[:m], S_[idx][:m], color=col_, lw=2.2, label=ar(lab), alpha=0.9)
    al = ease((t - 0.6) / 0.4); LEV = [l for l in r["niveles"] if lo[idx].min() - span * 0.25 <= l["valor"] <= hi[idx].max() + span * 0.25]
    for l in LEV: ax.axhline(l["valor"], color=NEG if l["tipo"] == "res" else TEAL, lw=1.1, ls="--", alpha=al)
    vals = [l["valor"] for l in LEV]
    ax.set_xlim(-1, NB); ax.set_ylim(min(lo[idx].min(), np.nanmin(a_["S200"][idx]), *vals) - span * 0.05, max(hi[idx].max(), np.nanmax(a_["S200"][idx]), *vals) + span * 0.05)
    tk = [j for j in range(4, NB) if dates[idx[j]].month != dates[idx[j - 1]].month]
    ax.set_xticks(tk, [ar(MESES[dates[idx[j]].month - 1]) for j in tk]); ax.tick_params(labelsize=15)
    ax.yaxis.tick_right(); ax.tick_params(axis="y", labelsize=14)
    ax.legend(frameon=False, labelcolor=FG, fontsize=16, loc=TJ.get("leyenda", "upper left"), ncol=3)
    if hay_vol:
        axv = f.add_axes([0.05, 0.345, 0.56, 0.075]); clean(axv); axv.patch.set_alpha(0); axv.set_zorder(-1)
        axv.bar(x[:m], vol[idx][:m], color=[TEAL if c[i] >= o[i] else NEG for i in idx[:m]], alpha=0.7, width=0.7)
        axv.set_xlim(-1, NB); axv.set_xticks([]); axv.set_yticks([]); axv.text(1.0, 1.0, ar("الحجم"), transform=axv.transAxes, color=MUTED, fontsize=13, ha="right", va="top")
    ax2 = f.add_axes([0.05, 0.215, 0.56, 0.11]); clean(ax2)
    ax2.axhspan(70, 100, color=NEG, alpha=0.08); ax2.axhspan(0, 30, color=TEAL, alpha=0.08)
    for lv in (30, 70): ax2.axhline(lv, color=DIM, lw=0.8, ls=":")
    ax2.plot(x[:m], a_["RSI"][idx][:m], color=BLUE, lw=2.2, label="RSI 14")
    ax2.set_xlim(-1, NB); ax2.set_ylim(0, 100); ax2.set_xticks([]); ax2.yaxis.tick_right(); ax2.set_yticks([30, 70])
    ax2.legend(frameon=False, labelcolor=FG, fontsize=14, loc="upper left")
    filas = [("الإغلاق", num(r["cierre"]), FG),
             ("متوسط 20 جلسة", f"{num(r['sma20'])}  ({pct(r['dist_sma20_pct'], 1)})", FG),
             ("متوسط 50 جلسة", f"{num(r['sma50'])}  ({pct(r['dist_sma50_pct'], 1)})", BLUE),
             ("متوسط 200 جلسة", f"{num(r['sma200'])}  ({pct(r['dist_sma200_pct'], 1)})", GOLD),
             ("RSI 14", num(r["rsi14"], 1) + "  · " + TJ["rsi_txt"], BLUE),
             ("حجم التداول", ("—" if vr is None else f"{pct(vr, 0)}") + " عن متوسط 10 جلسات", MUTED),
             ("الاتجاه (محسوب)", r["tendencia"], GOLD)]
    res = [l for l in r["niveles"] if l["tipo"] == "res"]; sop = [l for l in r["niveles"] if l["tipo"] == "sop"]
    if res: filas.append(("أقرب مقاومة", f"{num(min(res, key=lambda l: l['valor'])['valor'])}  (قمة {fiso(min(res, key=lambda l: l['valor'])['fecha'])})", NEG))
    if sop: filas.append(("أقرب دعم", f"{num(max(sop, key=lambda l: l['valor'])['valor'])}  (قاع {fiso(max(sop, key=lambda l: l['valor'])['fecha'])})", TEAL))
    for i, (lab, val, cc) in enumerate(filas):
        b = ease((t - 0.3 - i * 0.05) / 0.4)
        if b <= 0: continue
        y = 0.725 - i * 0.058
        T(f, 0.94, y, lab, MUTED, 19, alpha=b)
        T(f, 0.665, y, val, cc, 20, "bold", ha="left", alpha=b)
    return to_arr(f)


def s_esc(k, t):
    r = R[k]; E = r["escenarios"]; a_ = A[k]; TJ = VJ["tecnico"][k]
    f = base_fig(6, "ثلاثة سيناريوهات · " + INDICE[k], TJ.get("esc_titulo", "المستويات التي يراقبها المتداولون"),
                 "المستويات محسوبة من بيانات الإغلاق العامة (قمم وقيعان آخر 5 و30 جلسة و52 أسبوعًا، ومتوسطات 20 و50 و200 جلسة). "
                 "سيناريوهات مشروطة لوصف ما قد يعنيه كل مستوى، وليست توقعات ولا توصيات بالشراء أو البيع.")
    et = lambda l: f"{num(l['valor'])} ({fiso(l['et'])})"
    up, dn, ne = E["alcista"], E["bajista"], E["neutral"]
    cards = [("السيناريو الصاعد", TEAL, ("تأكيد استمرار الصعود يتطلب إغلاقًا فوق " + et(up[0]) + ((" ثم " + et(up[1])) if len(up) > 1 else "")) if up
              else "المؤشر عند أعلى مستوياته في الفترة: لا مقاومة سابقة فوقه، والمهم الثبات فوق " + num(r["cierre"])),
             ("السيناريو المحايد", GOLD, (f"التداول بين {num(ne[0]['valor'])} و{num(ne[1]['valor'])} يعني تماسكًا (نطاق {abs(ne[1]['valor'] / ne[0]['valor'] * 100 - 100):.1f}%)") if ne
              else "لا يوجد نطاق واضح بين دعم ومقاومة قريبين"),
             ("السيناريو الهابط", NEG, ("كسر " + et(dn[0]) + ((" يضع " + et(dn[1]) + " تحت المراقبة") if len(dn) > 1 else "")) if dn
              else "لا دعم سابق قريب دون السعر الحالي")]
    for i, (tt, cc, tx) in enumerate(cards):
        b = ease((t - i * 0.18) / 0.4)
        if b <= 0: continue
        y = 0.62 - i * 0.15
        rect(f, 0.50, y - 0.05, 0.44, 0.125, cc, 0.13 * b); rect(f, 0.935, y - 0.05, 0.005, 0.125, cc, b)
        T(f, 0.925, y + 0.035, tt, cc, 26, "bold", alpha=b)
        L_ = textwrap.wrap(tx, 50); fs_ = 20
        if len(L_) > 2: L_ = textwrap.wrap(tx, 58); fs_ = 18  # tres líneas pisan el título de la tarjeta
        T(f, 0.925, y - 0.01, "\n".join(L_), FG, fs_, va="center", linespacing=1.3, alpha=b)
    c = a_["c"][-60:]; n = len(c); ax = f.add_axes([0.05, 0.25, 0.40, 0.48]); clean(ax)
    ax.plot(np.arange(n), c, color=FG, lw=2.5)
    lv = [(l["valor"], TEAL) for l in up if abs(l["dist_pct"]) <= 7] + [(l["valor"], NEG) for l in dn if abs(l["dist_pct"]) <= 7]
    ult = None
    for v, cc in sorted(lv):
        ax.axhline(v, color=cc, lw=1.4, ls="--")
        if ult is None or abs(v / ult - 1) > 0.006: ax.text(n + 0.5, v, num(v, 0), color=cc, fontsize=15, va="center", weight="bold"); ult = v
    lo_ = min([c.min()] + [v for v, _ in lv]); hi_ = max([c.max()] + [v for v, _ in lv]); sp = hi_ - lo_
    ax.set_ylim(lo_ - sp * 0.06, hi_ + sp * 0.06); ax.set_xlim(0, n + 6); ax.set_xticks([]); ax.set_yticks([])
    ax.scatter([n - 1], [c[-1]], color=GOLD, s=80, zorder=5)
    T(f, 0.45, 0.75, "إغلاقات آخر 60 جلسة والمستويات", MUTED, 17)
    return to_arr(f)


# ---------- 7. Agenda ----------
RIAD_Z = ZoneInfo("Asia/Riyadh")


def s_agenda(t):
    G = VJ["agenda"]; f = base_fig(7, "ماذا ننتظر في الجلسة المقبلة؟", G["titulo"], G["fuente"])
    for x, h in ((0.94, "اليوم"), (0.75, "الحدث"), (0.17, "نيويورك"), (0.07, "مكة")): T(f, x, 0.71, h, MUTED, 19, "bold", ha="right" if x > 0.5 else "center")
    rect(f, 0.05, 0.695, 0.90, 0.003, GOLD)
    for i, row in enumerate(G["filas"][:7]):
        b = ease((t - i * 0.1) / 0.4); y = 0.645 - i * 0.068
        if b <= 0: continue
        if len(row) >= 3 and re.match(r"\d{4}-\d{2}-\d{2}$", row[0]):
            d = dt.date.fromisoformat(row[0]); dia = DIAS[d.weekday()] + " " + corto(d); ny = row[2] if len(row) > 2 else ""
            mk = ""
            if re.match(r"\d{1,2}:\d{2}$", ny or ""):
                hh, mm = map(int, ny.split(":")); z = dt.datetime(d.year, d.month, d.day, hh, mm, tzinfo=NYZ).astimezone(RIAD_Z)
                mk = z.strftime("%H:%M") + (" (+1)" if z.date() > d else "")
        else:
            dia, ny, mk = row[0], "", ""
        T(f, 0.94, y, dia, GOLD, 23, "bold", alpha=b)
        T(f, 0.75, y, row[1], FG, 22 if len(row[1]) <= 60 else 19, alpha=b)
        f.text(0.17, y, ny or "—", color=FG, fontsize=21, weight="bold", ha="center", alpha=b)
        f.text(0.07, y, mk or "—", color=BLUE, fontsize=21, weight="bold", ha="center", alpha=b)
    return to_arr(f)


# ---------- 8. Despedida ----------
def s_fin(t):
    Fn = VJ["fin"]; f = fig(W, H); a = ease(t / 0.5); b = ease((t - 0.25) / 0.5)
    T(f, 0.94, 0.85, MARCA + " · " + FECHA_TXT, FG, 46, "bold", alpha=a)
    T(f, 0.94, 0.775, "\n".join(textwrap.wrap(Fn["titular"], 55)), GOLD, 30, "bold", alpha=a, linespacing=1.35, va="top")
    rect(f, 0.30, 0.47, 0.64, 0.19, BLUE, 0.14 * b); rect(f, 0.935, 0.47, 0.005, 0.19, BLUE, b)
    T(f, 0.92, 0.615, "انضموا مجانًا إلى قناتنا على تيليغرام", FG, 34, "bold", alpha=b)
    T(f, 0.92, 0.565, "تحليلات السوق الأمريكية وتحديثات خلال الجلسة · الرابط في وصف الفيديو", MUTED, 22, alpha=b)
    f.text(0.92, 0.495, TELEGRAM.replace("https://", ""), color=BLUE, fontsize=34, ha="right", weight="bold", alpha=b)
    f.text(0.94, 0.41, CANAL.replace("https://www.", ""), color=MUTED, fontsize=22, ha="right", weight="bold", alpha=a)
    aviso = ("إخلاء مسؤولية: محتوى تعليمي وإعلامي فقط، ولا يُعد توصية استثمارية أو دعوة لشراء أو بيع أي ورقة مالية أو استشارة مالية شخصية. "
             "استشر جهة مرخصة في بلدك قبل أي قرار استثماري. الأرقام من مصادر عامة مذكورة (" + Fn["fuentes"] + ")، والحسابات الخاصة موضحة بعبارة «محسوب». "
             "التحليل الفني والسيناريوهات تصف حركة الأسعار وليست توقعات. لا نملك مراكز في الأسهم المذكورة. الاستثمار ينطوي على مخاطر، والأداء السابق لا يضمن النتائج. "
             "النص والرسوم والصوت (صوت اصطناعي) من إعداد الذكاء الاصطناعي.")
    T(f, 0.94, 0.20, "\n".join(textwrap.wrap(aviso, 135)), MUTED, 15, linespacing=1.5, alpha=a)
    return with_logo(to_arr(f), LGB, x=110, y=70)


# ---------- Secuencia ----------
ESC = [("s_title", 1, s_title), ("s_indices", 2, s_indices), ("s_grandes", 2, s_grandes), ("s_news", 2, s_news), ("s_sectores", 3, s_sectores)]
ESC += [(f"s_accion_{i + 1}", 4, (lambda t, i=i: s_accion(i, t))) for i in range(len(VJ.get("acciones", [])))]
ESC += [("s_macro", 5, s_macro), ("s_tech_spx", 6, lambda t: s_tech("spx", t)), ("s_esc_spx", 6, lambda t: s_esc("spx", t)),
        ("s_tech_ndx", 6, lambda t: s_tech("ndx", t)), ("s_esc_ndx", 6, lambda t: s_esc("ndx", t)), ("s_agenda", 7, s_agenda), ("s_fin", 8, s_fin)]
BIG = {"s_title", "s_fin"}
VISUAL = {"s_title": "عنوان البرنامج والتاريخ، إغلاق إس آند بي 500 ومنحنى الجلسة، ناسداك 100 وداو جونز وراسل 2000",
          "s_indices": "جدول مقارن متحرك: الإغلاق، اليوم، الأسبوع، المسافة عن أعلى مستوى، متوسط 200، الاتجاه",
          "s_grandes": "أعمدة: كبار ناسداك 100، ومساهمة مكونات داو جونز بالنقاط", "s_news": "أهم الأخبار وأسباب الحركة مع المصادر",
          "s_sectores": "أعمدة الأداء اليومي لصناديق القطاعات الستة مع الأداء الأسبوعي", "s_macro": "خمس بطاقات مع خط آخر 15 جلسة، وفقرة النفط والخليج",
          "s_tech_spx": "شموع 6 أشهر ومتوسطات 20/50/200 والحجم و RSI 14 والدعوم والمقاومات", "s_esc_spx": "بطاقات السيناريوهات الثلاثة وخط آخر 60 جلسة",
          "s_tech_ndx": "شموع 6 أشهر ومتوسطات 20/50/200 والحجم و RSI 14 والدعوم والمقاومات", "s_esc_ndx": "بطاقات السيناريوهات الثلاثة وخط آخر 60 جلسة",
          "s_agenda": "جدول الأحداث بتوقيت نيويورك ومكة", "s_fin": "الشعار، دعوة تيليغرام، إخلاء المسؤولية"}


def texto_voz(nombre):
    if nombre.startswith("s_accion_"): return VJ["acciones"][int(nombre.split("_")[-1]) - 1]["voz"]
    return VJ["voz"][nombre]


def frame(nombre, fn, t):
    arr = fn(t); return arr if nombre in BIG else with_logo(arr, LGS, x=60, y=48)


# ---------- Control de calidad (manual, sección 8) ----------
def control():
    err, aviso = [], []
    hoy_ny = dt.datetime.now(NYZ).date()
    if FECHA > hoy_ny: err.append(f"la sesión {FECHA} es posterior a hoy en Nueva York")
    if VJ.get("fecha") and VJ["fecha"] != R["fecha"]: err.append(f"video.json es del {VJ['fecha']} y los datos del {R['fecha']}")
    for k in ("spx", "ndx", "dji", "rut"):
        if k not in R: err.append(f"faltan las velas de {k}"); continue
        if R[k]["fecha"] != R["fecha"]: err.append(f"{k}: última vela del {R[k]['fecha']}, la sesión es del {R['fecha']}")
        if R[k]["sesiones"] < 220: err.append(f"{k}: solo {R[k]['sesiones']} sesiones, no alcanza para la media de 200")
    if len(R.get("sectores") or []) < 6: err.append("faltan ETF sectoriales en los datos")
    if len(R.get("macro") or []) < 5: err.append("faltan indicadores macro en los datos")
    for x in R.get("macro") or []:
        if not x["mismo_dia"]: aviso.append(f"{x['simbolo']}: último dato del {x['fecha']} (se muestra la fecha en pantalla)")
    A5 = VJ.get("acciones", [])
    if len(A5) != 5: err.append(f"hacen falta 5 acciones y hay {len(A5)}")
    for a in A5:
        if not accion(M, a["ticker"]): err.append(f"{a['ticker']} no está en los datos del día")
        for c in ("noticia", "lectura", "voz"):
            if not a.get(c): err.append(f"{a.get('ticker')}: falta {c}")
    for nombre, _, _ in ESC:
        try:
            if not texto_voz(nombre).strip(): err.append(f"falta la locución de {nombre}")
        except (KeyError, IndexError): err.append(f"falta la locución de {nombre}")
    for row in VJ.get("agenda", {}).get("filas", []):
        if re.match(r"\d{4}-\d{2}-\d{2}$", row[0]) and dt.date.fromisoformat(row[0]) <= FECHA: err.append(f"agenda: {row[0]} no es posterior a la sesión")
    for x in aviso: print("aviso:", x)
    if err: sys.exit("CONTROL DE CALIDAD:\n- " + "\n- ".join(err))


# ---------- Ticker y subtítulos ----------
def ticker_tira():
    piezas = []
    for k in ("spx", "ndx", "dji", "rut"):
        if k in R: piezas.append([(INDICE_CORTO[k], FG), (num(R[k]["cierre"]), FG), (pct(R[k]["var_pct"]), cc_(R[k]["var_pct"]))])
    for x in R.get("macro") or []:
        piezas.append([(x["nombre"], FG),
                       (f"{x['cierre']:.3f}%" if x["unidad"] == "%" else num(x["cierre"]), FG), (pct(x["cambio_pct"]), cc_(x["cambio_pct"]))])
    for s in R.get("sectores") or []: piezas.append([(s["simbolo"], FG), (pct(s["cambio"]), cc_(s["cambio"]))])
    for h in VJ.get("ticker") or [n[0] + ": " + n[1] for n in VJ["noticias"]["items"]]: piezas.append([(h, GOLD)])
    sep = tira_texto("◆", GOLD, 14, 52); hueco = np.zeros((52, 26, 4), np.uint8)
    imgs = []
    for p in piezas:  # orden de lectura de derecha a izquierda: la primera pieza a la derecha
        partes = [tira_texto(s, c, 19, 52) for s, c in p]
        im = np.concatenate(sum([[x, np.zeros((52, 12, 4), np.uint8)] for x in partes[::-1]], [])[:-1], axis=1)
        imgs += [im, hueco, sep, hueco]
    return np.concatenate(imgs[::-1], axis=1)


SUB_CACHE = {}


def subtitulo(s):
    if s not in SUB_CACHE:
        lin = textwrap.wrap(s, 72) or [s]
        SUB_CACHE[s] = [tira_texto(l, FG, 27, 50, "bold") for l in lin]
    return SUB_CACHE[s]


def hacer_overlay(marcas, leads):
    TIRA = ticker_tira(); L = TIRA.shape[1]; band = np.array([0x13, 0x29, 0x4B], np.float32); gold = np.array([0xD4, 0xAF, 0x37], np.uint8)
    def ov(fr, j, ts, tg):
        fr = fr.copy()
        fr[H - 52:] = (fr[H - 52:].astype(np.float32) * 0.1 + band * 0.9).astype(np.uint8); fr[H - 54:H - 52] = gold
        off = int(tg * 85) % L
        for x in range(off - L, W, L): pegar(fr, TIRA, x, H - 52)
        for a, b, s in marcas[j]:
            if a + leads[j] <= ts < b + leads[j] + 0.25:
                ls = subtitulo(s); h = 50 * len(ls); y0 = H - 66 - h; wmax = max(l.shape[1] for l in ls)
                x0 = (W - wmax) // 2 - 24; fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48] = (fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48].astype(np.float32) * 0.28 + np.array([11, 26, 46], np.float32) * 0.72).astype(np.uint8)
                for i, l in enumerate(ls): pegar(fr, l, (W - l.shape[1]) // 2, y0 + i * 50)
                break
        return fr
    return ov


def guion_y_datos(times, durs, marcas, motor):
    """Guion en tabla (tiempo, narración, visual, datos) y tabla de datos usados (manual, secciones 7 y 10)."""
    mmss = lambda s: f"{int(s) // 60:02d}:{int(s) % 60:02d}"
    datos_escena = {"s_title": " · ".join(f"{INDICE_CORTO[k]} {num(R[k]['cierre'])} ({pct(R[k]['var_pct'])})" for k in ("spx", "ndx", "dji", "rut") if k in R),
                    "s_sectores": " · ".join(f"{s['simbolo']} {pct(s['cambio'])}" for s in R.get("sectores") or []),
                    "s_macro": " · ".join(f"{x['simbolo']} {x['cierre']} ({pct(x['cambio_pct'])})" for x in R.get("macro") or [])}
    for k in ("spx", "ndx"):
        r = R[k]; datos_escena[f"s_tech_{k}"] = f"cierre {num(r['cierre'])} · SMA20 {num(r['sma20'])} · SMA50 {num(r['sma50'])} · SMA200 {num(r['sma200'])} · RSI {r['rsi14']}"
        datos_escena[f"s_esc_{k}"] = json.dumps(r["escenarios"], ensure_ascii=False)
    L = [f"# Guion {MARCA} · {PROGRAMA} · {FECHA_TXT}", "", f"Voz: {motor}. Duración: {mmss(sum(durs))}.", "",
         "| Tiempo | Narración en árabe | Visual | Datos |", "|---|---|---|---|"]
    for (nombre, _, _), t0 in zip(ESC, times):
        vis = VISUAL.get(nombre, "بطاقة السهم: السعر والتغير والحجم والخبر والقراءة وشموع 3 أشهر")
        dat = datos_escena.get(nombre, "")
        if nombre.startswith("s_accion_"):
            a = accion(M, VJ["acciones"][int(nombre.split("_")[-1]) - 1]["ticker"]); dat = f"{a['ticker']} {a['cierre']} ({pct(a['cambio'])}) vol {a['volumen']} ×{a['vol_rel']}"
        L.append(f"| {mmss(t0)} | {texto_voz(nombre)} | {vis} | {dat} |")
    open(f"{DIR}/guion-{R['fecha']}-Nabd.md", "w").write("\n".join(L) + "\n")
    ref = f"cierre {R['fecha']} 16:00 Nueva York; descargado {M.get('generado', '')}"
    with open(f"{DIR}/datos-{R['fecha']}-Nabd.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["concepto", "valor", "fuente", "referencia"])
        for k in ("spx", "ndx", "dji", "rut"):
            r = R[k]
            for c in ("cierre", "var_pct", "var_pts", "semana_pct", "max_hist", "max_hist_fecha", "dist_max_hist_pct", "sma20", "sma50", "sma200", "rsi14", "volumen_vs_media10_pct", "tendencia"):
                w.writerow([f"{k}.{c}", r.get(c), "TradingView" if c in ("cierre", "var_pct", "var_pts") else "محسوب (TradingView)", ref])
            for e_, L_ in r["escenarios"].items():
                for l in L_: w.writerow([f"{k}.escenario.{e_}", l["valor"], "محسوب (TradingView)", l["et"]])
        for s in R.get("sectores") or []: w.writerow([f"sector.{s['simbolo']}", s["cambio"], "TradingView", ref])
        for x in R.get("macro") or []: w.writerow([f"macro.{x['simbolo']}", x["cierre"], "TradingView", f"cierre {x['fecha']}; cambio {x['cambio_pct']}%"])
        for a in VJ.get("acciones", []):
            d = accion(M, a["ticker"]); w.writerow([f"accion.{a['ticker']}", f"{d['cierre']} ({d['cambio']}%) vol {d['volumen']}", "TradingView; " + a.get("fuente", ""), ref])
        for n in VJ["noticias"]["items"]: w.writerow(["noticia", " ".join(n), VJ["noticias"]["fuente"], R["fecha"]])
        for row in VJ["agenda"]["filas"]: w.writerow(["agenda", " · ".join(row), VJ["agenda"]["fuente"], "hora de Nueva York"])


if __name__ == "__main__":
    os.makedirs(AUD, exist_ok=True)
    control()
    if PREVIEW:
        ov = hacer_overlay([[(0, 99, frases(texto_voz(n))[0])] for n, _, _ in ESC], [0] * len(ESC))
        for j, (nombre, _, fn) in enumerate(ESC): Image.fromarray(ov(frame(nombre, fn, 1.0), j, 1.0, 3.0 + j)).save(os.path.join(AUD, "prev_" + nombre + ".png"))
        sys.exit()
    V = [voz_frases(texto_voz(n), AUD) for n, _, _ in ESC]; sr = V[0][1]; motor = V[0][3]
    if len({v[1] for v in V}) > 1 or len({v[3] for v in V}) > 1: sys.exit("voces mezcladas")
    LEAD, TAIL = 0.15, 0.6
    durs = [LEAD + len(a) / sr + TAIL for a, _, _, _ in V]; durs[0] += 0.4; durs[-1] += 2.0
    print("voz", motor, "duración prevista", round(sum(durs), 1), [round(d, 1) for d in durs])
    if not MIN_S <= sum(durs) <= MAX_S: sys.exit(f"Duración {sum(durs):.0f} s fuera de {MIN_S}-{MAX_S} s: alarga o acorta la locución")
    leads = [LEAD + (0.4 if j == 0 else 0) for j in range(len(ESC))]
    times, t0 = render([lambda t, n=n, fn=fn: frame(n, fn, t) for n, _, fn in ESC], durs, ([v[0] for v in V], leads), sr, W, H, FPS, OUT,
                       os.path.join(AUD, "video-silent.mp4"), os.path.join(AUD, "full.wav"), overlay=hacer_overlay([v[2] for v in V], leads))
    json.dump([(n, tt) for (n, _, _), tt in zip(ESC, times)] + [("_total", round(t0, 2)), ("_voz", motor)], open(os.path.join(DIR, "times.json"), "w"))
    guion_y_datos(times, durs, [v[2] for v in V], motor)
    print("listo", round(t0, 1), "s", OUT)
