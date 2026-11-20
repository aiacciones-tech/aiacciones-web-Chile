# Lección de la serie educativa semanal «التحليل الفني ببساطة» (Qatar AI Stocks): un concepto de análisis técnico por vídeo,
# explicado sobre el gráfico real de una acción de la Bolsa de Qatar (Daniel, 20-nov-2026). 1920x1080, ~6 minutos, voz Piper ar_JO-kareem
# (la del canal), subtítulos en árabe (quemados y .srt). Copia de saudi/educativo/make_leccion.py con la marca de Qatar.
# Diseño de derecha a izquierda (textos alineados a la derecha); el eje del tiempo del gráfico va de izquierda a derecha.
# Escenas en video.json → "escenas"; tipos: portada, esquema, puntos, grafico, fin. Velas: velas.json de la rama datos-educativo-qatar.
# Uso: AUD=<scratch> VELAS=<velas.json> python3 make_leccion.py <carpeta de la lección> [preview]
#   Escribe <base>-qatar.mp4, subtitulos-<base>-qatar.srt, times.json y guion-<base>-qatar.md.
import os, sys, json, datetime as dt, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from comun_leccion import *
import campana
from tecnico import MESES

DIR = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ""; PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
AUD = os.environ.get("AUD", "aud"); os.makedirs(AUD, exist_ok=True)
VJ = json.load(open(f"{DIR}/video.json")); VEL = json.load(open(os.environ.get("VELAS", f"{DIR}/velas.json")))
W, H = 1920, 1080
MIN_S, MAX_S = 300, 450   # ~6 minutos (5 a 7,5)
BASE = VJ["base"]; OUT = f"{DIR}/{BASE}-qatar.mp4"
CTA = campana.activa()
ESC = [dict(e) for e in VJ["escenas"]]
if CTA:  # campaña de comentarios y suscripción (campana.py, hasta el 22-nov-2026): al final de la locución de la escena final
    ESC[-1]["voz"] = ESC[-1]["voz"] + " " + campana.VOZ
fecha_v = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).date()
fecha_ar = lambda d: f"{d.day} {MESES[d.month - 1]} {d.year}"
SER = VEL["series"][VJ["simbolo"]]
# solo sesiones cerradas hasta "ultima_vela" (la vela del día en curso puede ser intradía)
VELAS = [v for v in SER["velas"] if not VJ.get("ultima_vela") or fecha_v(v["t"]).isoformat() <= VJ["ultima_vela"]]; ULT = fecha_v(VELAS[-1]["t"])
FUENTE_DATOS = SER.get("fuente", "TradingView")
FUENTE = f"بيانات الأسعار: {FUENTE_DATOS} (شموع يومية، {VJ['simbolo']}، حتى {fecha_ar(ULT)}). المناطق والعلامات محسوبة ومرسومة من القناة."
DEC = VJ.get("decimales", 2)
LG = load_logo(120); LGB = load_logo(230)
CAP = [e.get("capitulo") for e in ESC if e.get("capitulo")]
CAP_IDX = [sum(1 for x in ESC[:i + 1] if x.get("capitulo")) for i in range(len(ESC))]
XR = 0.94


def T(f, x, y, s, c=FG, fs=24, w="normal", ha="right", ancho=None, **k):
    return f.text(x, y, ar(s, ancho), color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def rect(f, x, y, w, h, c, a=1.0):
    f.patches.append(plt.Rectangle((x, y), w, h, transform=f.transFigure, color=col(c), alpha=a, figure=f))


def base(i, kicker, title):
    f = fig(W, H)
    T(f, XR, 0.905, kicker, GOLD, 26, "bold")
    T(f, XR, 0.825, title, FG, 42 if len(title) <= 55 else 34, "bold")
    T(f, 0.105, 0.925, f"{SERIE} · الحلقة {VJ['folge']}", MUTED, 20, "bold", ha="left")
    T(f, 0.105, 0.885, VJ["tema"], DIM if False else MUTED, 17, ha="left")
    n = max(len(CAP), 1); w = 0.88 / n
    for k in range(n):  # barra de progreso de derecha a izquierda
        rect(f, XR - (k + 1) * w + 0.008, 0.975, w - 0.008, 0.008, GOLD if k < CAP_IDX[i] else DIM)
    return f


def fuente(f, s): T(f, XR, 0.13, s, MUTED, 14, ancho=200, linespacing=1.35)


# ---------- escenas ----------
def s_portada(i, e, t):
    f = fig(W, H); a = ease(t / 0.6)
    T(f, XR, 0.88, f"{MARCA} · سلسلة {SERIE}", GOLD, 30, "bold", alpha=a)
    rect(f, 0, 0.62, 1.0, 0.2, GOLD, a)
    T(f, XR, 0.765, f"الحلقة {VJ['folge']}", BG, 34, "bold", va="center", alpha=a)
    T(f, XR, 0.672, VJ["tema"], BG, 70 if len(VJ["tema"]) <= 28 else 56, "bold", va="center", alpha=a)
    T(f, XR, 0.52, f"شرح على الرسم البياني الحقيقي لسهم {VJ['nombre']} ({VJ['ticker']})", FG, 40, "bold", alpha=ease((t - 0.15) / 0.5))
    if e.get("sub"): T(f, XR, 0.44, e["sub"], MUTED, 28, alpha=ease((t - 0.25) / 0.5))
    T(f, XR, 0.30, "محتوى تعليمي وليس توصية استثمارية", BLUE, 28, "bold", alpha=ease((t - 0.35) / 0.5))
    return with_logo(to_arr(f), LGB, x=80, y=40)


def s_puntos(i, e, t):
    f = base(i, e["kicker"], e["titulo"]); P = e["puntos"][:5]; hh = min(0.12, 0.6 / len(P))
    for k, (tit, txt) in enumerate(P):
        b = ease((t - k * 0.1) / 0.4); y = 0.68 - (k + 1) * hh; ym = y + (hh - 0.014) / 2
        rect(f, 0.06, y, 0.88, hh - 0.014, PANEL, b); rect(f, XR - 0.005, y, 0.005, hh - 0.014, e.get("colores", [GOLD] * 5)[k], b)
        T(f, 0.925, ym, f"{k + 1}", GOLD, 34, "bold", va="center", alpha=b)
        T(f, 0.895, ym, tit, FG, 26, "bold", va="center", alpha=b)
        T(f, 0.64, ym, txt, MUTED, 21, va="center", alpha=b, ancho=70, linespacing=1.3)
    if e.get("fuente"): fuente(f, e["fuente"])
    return to_arr(f)


def _zigzag(modo):
    """Recorrido de precio esquemático (no son datos reales)."""
    if modo == "sr":
        pts = [(0, 40), (8, 78), (15, 32), (24, 80), (31, 30), (40, 79), (47, 33), (55, 70)]
    elif modo == "rollentausch":
        pts = [(0, 30), (8, 58), (14, 36), (22, 60), (28, 40), (36, 82), (42, 62), (48, 61), (56, 92)]
    elif modo == "rollentausch_baja":
        pts = [(0, 70), (8, 42), (14, 64), (22, 40), (28, 60), (36, 18), (42, 38), (48, 39), (56, 8)]
    else:  # fehlausbruch
        pts = [(0, 40), (8, 76), (15, 35), (24, 79), (30, 50), (37, 86), (41, 72), (48, 45), (56, 38)]
    x = np.arange(0, 57); y = np.interp(x, [p[0] for p in pts], [p[1] for p in pts])
    rng = np.random.default_rng(7); return x, y + rng.normal(0, 1.4, len(x))


def s_esquema(i, e, t):
    f = base(i, e["kicker"], e["titulo"]); modo = e.get("modo", "sr")
    ax = f.add_axes([0.06, 0.25, 0.54, 0.52]); clean(ax); ax.set_xticks([]); ax.set_yticks([])
    x, y = _zigzag(modo); n = max(2, int(len(x) * min(1, ease(t * 1.2)))); ax.set_xlim(-1, 58)
    ax.set_ylim(0, 100) if modo == "rollentausch_baja" else ax.set_ylim(15, 100)
    za = ease((t - 0.3) / 0.4); lab = lambda xx, yy, s, c, ha="right", a=za: ax.text(xx, yy, ar(s), color=c, fontsize=22, weight="bold", ha=ha, alpha=a)
    if modo == "sr":
        ax.axhspan(76, 82, color=NEG, alpha=0.25 * za); ax.axhspan(28, 34, color=TEAL, alpha=0.25 * za)
        lab(57, 85, "مقاومة", NEG); lab(57, 20, "دعم", TEAL)
    elif modo == "rollentausch":
        ax.axhspan(57, 63, color=GOLD, alpha=0.28 * za)
        lab(1, 66, "مقاومة أولًا…", NEG, "left"); lab(57, 50, "…ثم دعم", TEAL, a=ease((t - 0.6) / 0.3))
    elif modo == "rollentausch_baja":
        ax.axhspan(37, 43, color=GOLD, alpha=0.28 * za)
        lab(1, 30, "دعم أولًا…", TEAL, "left"); lab(57, 47, "…ثم مقاومة", NEG, a=ease((t - 0.6) / 0.3))
    else:
        ax.axhspan(76, 81, color=NEG, alpha=0.25 * za)
        lab(1, 84, "مقاومة", NEG, "left")
        ax.annotate(ar("اختراق كاذب"), (37, 86), (46, 95), color=GOLD, fontsize=22, weight="bold", alpha=ease((t - 0.6) / 0.3),
                    arrowprops=dict(arrowstyle="->", color=GOLD, lw=2, alpha=ease((t - 0.6) / 0.3)))
    ax.plot(x[:n], y[:n], color=FG, lw=3.2)
    T(f, 0.60, 0.215, "رسم توضيحي، وليس بيانات أسعار حقيقية", MUTED, 17, "bold")
    for k, s in enumerate(e.get("notas", [])[:4]):
        b = ease((t - 0.2 - k * 0.12) / 0.4); yy = 0.70 - k * 0.135
        rect(f, 0.64, yy - 0.05, 0.30, 0.115, PANEL, b); rect(f, XR - 0.004, yy - 0.05, 0.004, 0.115, GOLD, b)
        T(f, 0.925, yy + 0.008, s, FG, 22, "bold", va="center", alpha=b, ancho=34, linespacing=1.15)
    return to_arr(f)


def _rango(e):
    d0 = dt.date.fromisoformat(e["desde"]) if e.get("desde") else None; d1 = dt.date.fromisoformat(e["hasta"]) if e.get("hasta") else ULT
    return [v for v in VELAS if (d0 is None or fecha_v(v["t"]) >= d0) and fecha_v(v["t"]) <= d1]


def sma(n, V):
    """Media móvil simple de n sesiones de cierre, calculada con todas las velas cerradas y recortada al rango V."""
    c = np.array([v["c"] for v in VELAS], float); m = np.full(len(c), np.nan)
    if len(c) >= n: m[n - 1:] = np.convolve(c, np.ones(n) / n, "valid")
    i0 = next(j for j, v in enumerate(VELAS) if v["t"] == V[0]["t"]); return m[i0:i0 + len(V)]


def rsi(V, n=14):
    """RSI de Wilder (14) con todas las velas cerradas, recortado al rango V."""
    c = np.array([v["c"] for v in VELAS], float); d = np.diff(c); g = np.maximum(d, 0); p = np.maximum(-d, 0)
    ag, ap = g[:n].mean(), p[:n].mean(); out = np.full(len(c), np.nan)
    for j in range(n, len(c)):
        if j > n: ag = (ag * (n - 1) + g[j - 1]) / n; ap = (ap * (n - 1) + p[j - 1]) / n
        out[j] = 100 - 100 / (1 + ag / ap) if ap else 100
    i0 = next(j for j, v in enumerate(VELAS) if v["t"] == V[0]["t"]); return out[i0:i0 + len(V)]


def s_grafico(i, e, t):
    f = base(i, e["kicker"], e["titulo"]); V = _rango(e); n = len(V)
    vol = e.get("volumen", True) or e.get("rsi")
    ax = f.add_axes([0.06, 0.325 if vol else 0.24, 0.80, 0.445 if vol else 0.53]); clean(ax)
    rev = n if not e.get("animar_velas") else max(2, int(n * ease(t * 1.15)))
    o = np.array([v["o"] for v in V]); hi = np.array([v["h"] for v in V]); lo = np.array([v["l"] for v in V]); c = np.array([v["c"] for v in V])
    up = c >= o; xs = np.arange(n); wd = 0.65 if n < 160 else 0.75
    ymin, ymax = lo.min(), hi.max()
    for z in e.get("zonas", []): ymin = min(ymin, z["de"]); ymax = max(ymax, z["a"])
    pad = (ymax - ymin) * 0.08
    ax.set_ylim(ymin - pad * 2.0, ymax + pad * 1.8); ax.set_xlim(-1, n + (n * 0.25))
    ax.vlines(xs[:rev], lo[:rev], hi[:rev], color=[TEAL if u else NEG for u in up[:rev]], lw=1.1 if n > 160 else 1.6)
    ax.bar(xs[:rev], np.maximum(np.abs(c - o), (ymax - ymin) * 0.002)[:rev], bottom=np.minimum(o, c)[:rev], width=wd,
           color=[TEAL if u else NEG for u in up[:rev]])
    za = ease((t - 0.25) / 0.35)
    for k, L in enumerate(e.get("lineas", [])):  # medias móviles simples calculadas de todas las velas (no solo del rango)
        sm = sma(L["sma"], V); a = ease((t - 0.2 - k * 0.12) / 0.35); cc = col(L.get("color", "blue")); ok = ~np.isnan(sm)
        ax.plot(xs[:rev][ok[:rev]], sm[:rev][ok[:rev]], color=cc, lw=2.6, alpha=a)
        if L.get("texto") and ok[-1] and rev == n:
            ax.text(n + 0.5, sm[-1], " " + ar(L["texto"]), color=cc, fontsize=17, weight="bold", ha="left", va="center", alpha=a)
    for k, z in enumerate(e.get("zonas", [])):
        a = ease((t - 0.25 - k * 0.12) / 0.35); cc = col(z.get("color", "gold"))
        ax.axhspan(z["de"], z["a"], color=cc, alpha=0.22 * a, lw=0)
        ax.axhline((z["de"] + z["a"]) / 2, color=cc, lw=1.4, ls="--", alpha=0.8 * a)
        ax.text(n + n * 0.245, (z["de"] + z["a"]) / 2, ar(z["texto"]) + f"\n{num(z['de'], DEC)}–{num(z['a'], DEC)}", color=cc, fontsize=18, weight="bold",
                ha="right", va="center", alpha=a, linespacing=1.15, bbox=dict(boxstyle="round,pad=0.25", fc=BG, ec="none", alpha=0.85 * a))
    idx = {fecha_v(v["t"]).isoformat(): j for j, v in enumerate(V)}
    for k, m in enumerate(e.get("marcas", [])):
        j = idx.get(m["fecha"])
        if j is None: continue
        a = ease((t - 0.45 - k * 0.07) / 0.3); arriba = m.get("tipo") == "techo"
        yv = hi[j] if arriba else lo[j]; off = (ymax - ymin) * (0.07 if arriba else -0.07)
        ax.plot([j], [yv + off * 0.35], marker="v" if arriba else "^", color=GOLD, ms=15, alpha=a)
        if m.get("texto"): ax.text(j, yv + off * 1.3, ar(m["texto"]), color=GOLD, fontsize=16, weight="bold", ha="center", va="center", alpha=a)
    if e.get("ultimo", True) and rev == n:
        ax.axhline(c[-1], color=FG, lw=0.8, alpha=0.5 * za)
        ax.text(n + 0.5, c[-1], f" {num(c[-1])} ", color=BG, fontsize=15, weight="bold", va="center",
                bbox=dict(boxstyle="square,pad=0.25", fc=FG, ec="none", alpha=za), alpha=za)
    ax.yaxis.tick_left(); ax.tick_params(labelsize=15)
    ydec = 0 if (ymax - ymin) > 8 else 1
    ax.set_yticks(ax.get_yticks()[1:-1]); ax.set_yticklabels([num(y, ydec) for y in ax.get_yticks()])
    ax.grid(axis="y", color=DIM, lw=0.6, alpha=0.6)
    tk, prev = [], None
    for j, v in enumerate(V):
        d = fecha_v(v["t"])
        if d.month != prev: tk.append((j, ar(MESES[d.month - 1]) + (f"\n{d.year}" if d.month == 1 or not tk else ""))); prev = d.month
    step = 1 if len(tk) <= 9 else 2
    ax.set_xticks([p[0] for p in tk[::step]], [p[1] for p in tk[::step]] if not vol else [])
    if e.get("rsi"):  # panel RSI(14) de Wilder en lugar del volumen, con 30 y 70
        av = f.add_axes([0.06, 0.205, 0.80, 0.11]); clean(av); r = rsi(V)
        av.axhspan(70, 100, color=NEG, alpha=0.10, lw=0); av.axhspan(0, 30, color=TEAL, alpha=0.10, lw=0)
        for y_ in (30, 70): av.axhline(y_, color=MUTED, lw=0.8, ls="--")
        av.plot(xs[:rev], r[:rev], color=BLUE, lw=2.2); av.set_xlim(ax.get_xlim()); av.set_ylim(0, 100); av.set_yticks([30, 70]); av.tick_params(labelsize=13)
        av.set_xticks([p[0] for p in tk[::step]], [p[1] for p in tk[::step]]); av.tick_params(axis="x", labelsize=15)
        T(f, 0.86, 0.318, f"مؤشر القوة النسبية (14): {num(r[-1], 1)}", BLUE, 15, "bold")
    elif vol:
        av = f.add_axes([0.06, 0.235, 0.80, 0.08]); clean(av)
        vv = np.array([v["v"] or 0 for v in V]) / 1e6
        av.bar(xs[:rev], vv[:rev], color=[TEAL if u else NEG for u in up[:rev]], width=wd, alpha=0.55)
        av.set_xlim(ax.get_xlim()); av.set_yticks([]); av.set_ylim(0, vv.max() * 1.1)
        av.set_xticks([p[0] for p in tk[::step]], [p[1] for p in tk[::step]]); av.tick_params(labelsize=15)
        T(f, 0.86, 0.318, "حجم التداول", MUTED, 15)
    T(f, XR, 0.785, f"{VJ['nombre']} ({VJ['ticker']}) · شموع يومية · بالريال القطري", MUTED, 19, "bold")
    if e.get("nota"):
        b = ease((t - 0.5) / 0.4); T(f, 0.06, 0.785, e["nota"], GOLD, 21, "bold", ha="left", alpha=b)
    fuente(f, FUENTE)
    return to_arr(f)


def s_fin(i, e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, XR, 0.86, f"الحلقة {VJ['folge']}: {VJ['tema']}", FG, 44, "bold", alpha=a)
    T(f, XR, 0.795, "الخلاصة", GOLD, 32, "bold", alpha=a)
    for k, c in enumerate(e["claves"][:4]):
        T(f, XR, 0.725 - k * 0.062, "• " + c, FG, 26, alpha=ease((t - 0.1 - k * 0.1) / 0.4))
    b = ease((t - 0.3) / 0.5)
    if e.get("siguiente"): T(f, XR, 0.45, "الحلقة القادمة: " + e["siguiente"], GOLD, 28, "bold", alpha=b)
    if CTA: T(f, XR, 0.395, f"💬 {campana.TITULO}: {campana.LINEA1} 🔔 {campana.LINEA2}".replace("💬 ", "").replace("🔔 ", "· "), BLUE, 23, "bold", alpha=b)
    else: T(f, XR, 0.395, f"اشترك في القناة ليصلك كل جديد · كل {DIA} حلقة جديدة", BLUE, 25, "bold", alpha=b)
    aviso = ("تنبيه مهم: هذا المحتوى تعليمي وإعلامي فقط، ولا يُعد توصية استثمارية ولا دعوة لشراء أو بيع أي ورقة مالية. "
             f"سهم {VJ['nombre']} مجرد مثال. التحليل الفني يصف حركة السعر في الماضي ولا يتنبأ بالمستقبل، والمناطق المرسومة ليست أسعارًا مستهدفة. "
             f"بيانات الأسعار من {FUENTE_DATOS}، والمناطق من حساب القناة. لا نملك مراكز في السهم المذكور. الاستثمار في الأسهم ينطوي على مخاطر قد تصل إلى خسارة رأس المال. "
             "النص والصوت (صوت اصطناعي) والرسوم من إعداد أدوات الذكاء الاصطناعي.")
    T(f, XR, 0.32, aviso, MUTED, 16, ancho=150, linespacing=1.6, alpha=a, va="top")
    return with_logo(to_arr(f), LGB, x=80, y=70)


TIPOS = {"portada": s_portada, "puntos": s_puntos, "esquema": s_esquema, "grafico": s_grafico, "fin": s_fin}
BIG = {"portada", "fin"}
SUB = {}


def overlay(marcas, leads):
    pie = tira_texto(f"{MARCA} · سلسلة {SERIE} · محتوى تعليمي وليس توصية استثمارية", GOLD, 18, 46); band = np.array(BANDA, np.float32)

    def sub(s):
        if s not in SUB: SUB[s] = [tira_texto(l, FG, 30, 56, "bold") for l in (partir(sub_pantalla(s), 72) or [s])]
        return SUB[s]

    def ov(fr, j, ts, tg):
        fr = fr.copy(); bh = 46
        fr[H - bh:] = (fr[H - bh:].astype(np.float32) * 0.1 + band * 0.9).astype(np.uint8); fr[H - bh - 2:H - bh] = (0xE8, 0xC4, 0x6A)
        pegar(fr, pie, (W - pie.shape[1]) // 2, H - bh)
        for a, b, s in marcas[j]:
            if a + leads[j] <= ts < b + leads[j] + 0.25:
                ls = sub(s); lh = 56; h = lh * len(ls); y0 = H - bh - 16 - h; wmax = max(l.shape[1] for l in ls); x0 = max((W - wmax) // 2 - 24, 0)
                fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48] = (fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48].astype(np.float32) * 0.28 + np.array(SUBF, np.float32) * 0.72).astype(np.uint8)
                for k, l in enumerate(ls): pegar(fr, l, (W - l.shape[1]) // 2, y0 + k * lh)
                break
        return fr
    return ov


def frame(i, t):
    e = ESC[i]; a = TIPOS[e["tipo"]](i, e, t)
    return a if e["tipo"] in BIG else with_logo(a, LG, x=40, y=30)


def control():
    err = []
    for k in ("base", "folge", "simbolo", "ticker", "nombre", "tema", "escenas", "info", "miniatura", "short"):
        if not VJ.get(k): err.append(f"falta {k} en video.json")
    for k, e in enumerate(ESC):
        if e.get("tipo") not in TIPOS: err.append(f"escena {k}: tipo desconocido {e.get('tipo')}")
        if not e.get("voz"): err.append(f"escena {k} ({e.get('id')}): sin locución")
        if e.get("tipo") == "grafico":
            V = _rango(e)
            if len(V) < 20: err.append(f"escena {k}: menos de 20 velas en el rango")
            fechas = {fecha_v(v["t"]).isoformat() for v in V}
            for m in e.get("marcas", []):
                if m["fecha"] not in fechas: err.append(f"escena {k}: marca {m['fecha']} sin vela")
    if VJ.get("ultima_vela") and VJ["ultima_vela"] != ULT.isoformat(): err.append(f"velas.json acaba el {ULT}, video.json espera {VJ['ultima_vela']}")
    for p in ("توصية بالشراء", "اشترِ", "بِع ", "سعر مستهدف", "رخيص", "سيرتفع", "سينخفض", "سيصل"):
        for e in ESC:
            if p in e.get("voz", "") and "ليس" not in e["voz"]: err.append(f"escena {e.get('id')}: revisa «{p}» (las zonas van como condiciones)")
    if err: sys.exit("CONTROL DE CALIDAD:\n- " + "\n- ".join(err))


if __name__ == "__main__":
    control()
    if PREVIEW:
        ov = overlay([[(0, 99, frases(e["voz"])[0])] for e in ESC], [0] * len(ESC))
        for j, e in enumerate(ESC): Image.fromarray(ov(frame(j, 1.0), j, 1.0, 3.0)).save(os.path.join(AUD, f"prev_{j:02d}_{e.get('id', e['tipo'])}.png"))
        print("palabras", sum(len(e["voz"].split()) for e in ESC)); sys.exit()
    VV = [voz_frases(e["voz"], AUD) for e in ESC]; sr = VV[0][1]; motor = VV[0][3]
    if len({v[1] for v in VV}) > 1 or len({v[3] for v in VV}) > 1: sys.exit("voces mezcladas: " + str([v[3] for v in VV]))
    durs = [0.15 + len(a) / sr + 0.7 for a, _, _, _ in VV]; durs[-1] += 1.5
    print("voz", motor, "duración prevista", round(sum(durs), 1))
    if not MIN_S <= sum(durs) <= MAX_S: sys.exit(f"Duración {sum(durs):.0f} s fuera de {MIN_S}-{MAX_S} s")
    leads = [0.15] * len(ESC)
    times, t0 = render([lambda t, j=j: frame(j, t) for j in range(len(ESC))], durs, ([v[0] for v in VV], leads), sr, W, H, 30, OUT,
                       os.path.join(AUD, "lec-silent.mp4"), os.path.join(AUD, "lec.wav"), overlay=overlay([v[2] for v in VV], leads))
    json.dump([(e.get("id", str(j)), tt) for j, (e, tt) in enumerate(zip(ESC, times))] + [("_total", round(t0, 2)), ("_voz", motor)], open(f"{DIR}/times.json", "w"))
    srt = lambda x: f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round(x % 1 * 1000)) % 1000:03d}"
    with open(f"{DIR}/subtitulos-{BASE}-qatar.srt", "w") as g:
        k = 0
        for j, tt in enumerate(times):
            for a, b, x in VV[j][2]:
                k += 1; g.write(f"{k}\n{srt(tt + leads[j] + a)} --> {srt(tt + leads[j] + b + 0.25)}\n{sub_pantalla(x)}\n\n")
    with open(f"{DIR}/guion-{BASE}-qatar.md", "w") as g:
        g.write(f"# {SERIE} · الحلقة {VJ['folge']}: {VJ['tema']} ({VJ['nombre']}, {VJ['ticker']})\n\nVoz: {motor} · Duración {t0:.0f} s\n\n| Tiempo | Escena | Texto |\n|---|---|---|\n")
        for e, tt in zip(ESC, times): g.write(f"| {int(tt) // 60}:{int(tt) % 60:02d} | {e.get('id', e['tipo'])} | {e['voz']} |\n")
    print("listo", round(t0, 1), "s", OUT)
