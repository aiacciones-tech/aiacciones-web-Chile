# Lección de la serie educativa «Charttechnik einfach erklärt» (Wall Street auf Deutsch): un concepto de análisis técnico por vídeo,
# explicado sobre el gráfico real de una acción de EE. UU. (Daniel, 18-nov-2026). 1920x1080, 4-8 minutos, voz Azure de-DE-ConradNeural.
# Las escenas las define video.json → "escenas" (lista); tipos: portada, esquema, puntos, grafico, fin. Velas: velas.json de la rama
# voz-ge-educativo (TradingView, educativo-GE.yml). Las zonas y marcas del gráfico las pone video.json; niveles.py ayuda a encontrarlas.
# Uso: AUD=<scratch> VELAS=<velas.json> [VOZ_DIR=<wav de Azure>] python3 make_leccion.py <carpeta de la lección> [preview]
#   Escribe <base>-GE.mp4, times.json y guion-<base>-GE.md.
import os, sys, json, textwrap, datetime as dt, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "diario"))
from comun import *

DIR = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ""; PREVIEW = len(sys.argv) > 2 and sys.argv[2] == "preview"
AUD = os.environ.get("AUD", "aud"); os.makedirs(AUD, exist_ok=True)
VJ = json.load(open(f"{DIR}/video.json")); VEL = json.load(open(os.environ.get("VELAS", f"{DIR}/velas.json")))
SERIE = "Charttechnik einfach erklärt"; NAVY = "#13294B"; W, H = 1920, 1080
MIN_S, MAX_S = 240, 540   # 4 a 9 minutos
BASE = VJ["base"]; OUT = f"{DIR}/{BASE}-GE.mp4"
ESC = VJ["escenas"]
MESES = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
MESES_L = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
fecha_v = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).date()
fecha_de = lambda d: f"{d.day}. {MESES_L[d.month - 1]} {d.year}"
SER = VEL["series"][VJ["simbolo"]]
# solo sesiones cerradas hasta "ultima_vela" (la vela del día en curso de velas.json puede ser intradía)
VELAS = [v for v in SER["velas"] if not VJ.get("ultima_vela") or fecha_v(v["t"]).isoformat() <= VJ["ultima_vela"]]; ULT = fecha_v(VELAS[-1]["t"])
FUENTE = f"Kursdaten: TradingView (Tageskerzen, Stand Schlusskurs {fecha_de(ULT)}). Gleitende Durchschnitte, Zonen und Markierungen berechnet bzw. eingezeichnet."
LG = load_logo(130); LGB = load_logo(230)
CAP = [e.get("capitulo") for e in ESC if e.get("capitulo")]
CAP_IDX = [sum(1 for x in ESC[:i + 1] if x.get("capitulo")) for i in range(len(ESC))]


def T(f, x, y, s, c=FG, fs=24, w="normal", ha="left", **k):
    return f.text(x, y, ar(s), color=col(c), fontsize=fs, weight=w, ha=ha, **k)


def rect(f, x, y, w, h, c, a=1.0):
    f.patches.append(plt.Rectangle((x, y), w, h, transform=f.transFigure, color=col(c), alpha=a, figure=f))


def base(i, kicker, title):
    f = fig(W, H)
    T(f, 0.06, 0.905, kicker, GOLD, 24, "bold")
    T(f, 0.06, 0.83, title, FG, 40 if len(title) <= 60 else 32, "bold")
    T(f, 0.895, 0.925, f"{SERIE} · Folge {VJ['folge']}", MUTED, 19, "bold", ha="right")
    T(f, 0.895, 0.89, f"{MARCA} · {VJ['tema']}", DIM, 16, "bold", ha="right")
    n = max(len(CAP), 1); w = 0.88 / n
    for k in range(n): rect(f, 0.06 + k * w, 0.975, w - 0.008, 0.008, GOLD if k < CAP_IDX[i] else DIM)
    return f


def fuente(f, s): T(f, 0.06, 0.135, "\n".join(textwrap.wrap(s, 175)), MUTED, 14, linespacing=1.35)


# ---------- escenas ----------
def s_portada(i, e, t):
    f = fig(W, H); a = ease(t / 0.6)
    T(f, 0.06, 0.88, f"{MARCA} · Serie «{SERIE}»", GOLD, 30, "bold", alpha=a)
    rect(f, 0, 0.62, 1.0, 0.2, GOLD, a)
    T(f, 0.06, 0.765, f"Folge {VJ['folge']}", BG, 34, "bold", va="center", alpha=a)
    T(f, 0.06, 0.675, VJ["tema"], BG, 76 if len(VJ["tema"]) <= 30 else 60, "bold", va="center", alpha=a)
    T(f, 0.06, 0.52, f"Erklärt am Chart von {VJ['nombre']} ({VJ['ticker']})", FG, 40, "bold", alpha=ease((t - 0.15) / 0.5))
    if e.get("sub"): T(f, 0.06, 0.45, e["sub"], MUTED, 28, alpha=ease((t - 0.25) / 0.5))
    T(f, 0.06, 0.30, "Bildung, keine Anlageberatung", BLUE, 26, "bold", alpha=ease((t - 0.35) / 0.5))
    return with_logo(to_arr(f), LGB, x=W - 340, y=40)


def s_puntos(i, e, t):
    f = base(i, e["kicker"], e["titulo"]); P = e["puntos"][:5]; hh = min(0.12, 0.52 / len(P))
    for k, (tit, txt) in enumerate(P):
        b = ease((t - k * 0.1) / 0.4); y = 0.68 - (k + 1) * hh
        rect(f, 0.06, y, 0.88, hh - 0.014, NAVY, b); rect(f, 0.06, y, 0.005, hh - 0.014, e.get("colores", [GOLD] * 5)[k], b)
        T(f, 0.08, y + (hh - 0.014) / 2, f"{k + 1}", GOLD, 34, "bold", va="center", alpha=b)
        T(f, 0.12, y + (hh - 0.014) / 2, tit, FG, 26, "bold", va="center", alpha=b)
        T(f, 0.40, y + (hh - 0.014) / 2, "\n".join(textwrap.wrap(txt, 78)), MUTED, 21, va="center", alpha=b, linespacing=1.3)
    if e.get("fuente"): fuente(f, e["fuente"])
    return to_arr(f)


def _zigzag(modo):
    """Recorrido de precio esquemático (no son datos reales)."""
    if modo == "sr":
        pts = [(0, 40), (8, 78), (15, 32), (24, 80), (31, 30), (40, 79), (47, 33), (55, 70)]
    elif modo == "rollentausch":
        pts = [(0, 30), (8, 58), (14, 36), (22, 60), (28, 40), (36, 82), (42, 62), (48, 61), (56, 92)]
    elif modo == "trendkanal":   # Aufwärtstrend: höhere Hochs und höhere Tiefs
        pts = [(0, 23), (7, 47), (12, 32), (20, 57), (26, 43), (34, 67.5), (40, 54), (48, 78.5), (53, 64), (56, 71)]
    else:  # fehlausbruch
        pts = [(0, 40), (8, 76), (15, 35), (24, 79), (30, 50), (37, 86), (41, 72), (48, 45), (56, 38)]
    x = np.arange(0, 57); y = np.interp(x, [p[0] for p in pts], [p[1] for p in pts])
    rng = np.random.default_rng(7); return x, y + rng.normal(0, 1.4, len(x))


def s_esquema(i, e, t):
    f = base(i, e["kicker"], e["titulo"]); modo = e.get("modo", "sr")
    ax = f.add_axes([0.06, 0.25, 0.56, 0.52]); clean(ax); ax.set_xticks([]); ax.set_yticks([])
    x, y = _zigzag(modo); n = max(2, int(len(x) * min(1, ease(t * 1.2)))); ax.set_xlim(-1, 58); ax.set_ylim(15, 100)
    za = ease((t - 0.3) / 0.4)
    if modo == "sr":
        ax.axhspan(76, 82, color=NEG, alpha=0.25 * za); ax.axhspan(28, 34, color=TEAL, alpha=0.25 * za)
        ax.text(57, 84, "Widerstand", color=NEG, fontsize=22, weight="bold", ha="right", alpha=za)
        ax.text(57, 22, "Unterstützung", color=TEAL, fontsize=22, weight="bold", ha="right", alpha=za)
    elif modo == "rollentausch":
        ax.axhspan(57, 63, color=GOLD, alpha=0.28 * za)
        ax.text(1, 65, "erst Widerstand …", color=NEG, fontsize=20, weight="bold", alpha=za)
        ax.text(57, 50, "… dann Unterstützung", color=TEAL, fontsize=20, weight="bold", ha="right", alpha=ease((t - 0.6) / 0.3))
    elif modo == "trendkanal":
        lo_ = lambda xx: 22 + (63 - 22) / 53 * xx   # Trendlinie durch die Tiefs (0, 22) und (53, 63)
        ax.plot([0, 57], [lo_(0), lo_(57)], color=TEAL, lw=3, alpha=za)
        ax.text(57, lo_(57) - 16, "Trendlinie (Tiefs)", color=TEAL, fontsize=20, weight="bold", ha="right", alpha=za)
        b2 = ease((t - 0.6) / 0.3)
        ax.plot([0, 57], [lo_(0) + 20.5, lo_(57) + 20.5], color=GOLD, lw=2.6, ls="--", alpha=b2)
        ax.fill_between([0, 57], [lo_(0), lo_(57)], [lo_(0) + 20.5, lo_(57) + 20.5], color=GOLD, alpha=0.08 * b2, lw=0)
        ax.text(57, lo_(57) + 26, "Parallele (Hochs): Trendkanal", color=GOLD, fontsize=20, weight="bold", ha="right", alpha=b2)
    else:
        ax.axhspan(76, 81, color=NEG, alpha=0.25 * za)
        ax.text(1, 84, "Widerstand", color=NEG, fontsize=20, weight="bold", alpha=za)
        ax.annotate("Fehlausbruch", (37, 86), (44, 95), color=GOLD, fontsize=20, weight="bold", alpha=ease((t - 0.6) / 0.3),
                    arrowprops=dict(arrowstyle="->", color=GOLD, lw=2, alpha=ease((t - 0.6) / 0.3)))
    ax.plot(x[:n], y[:n], color=FG, lw=3.2)
    T(f, 0.06, 0.215, "Schematische Darstellung, keine echten Kursdaten", MUTED, 16, "bold")
    for k, s in enumerate(e.get("notas", [])[:4]):
        b = ease((t - 0.2 - k * 0.12) / 0.4); yy = 0.70 - k * 0.135
        rect(f, 0.65, yy - 0.05, 0.29, 0.115, NAVY, b); rect(f, 0.65, yy - 0.05, 0.004, 0.115, GOLD, b)
        T(f, 0.665, yy + 0.008, "\n".join(textwrap.wrap(s, 30)), FG, 21, "bold", va="center", alpha=b, linespacing=1.3)
    return to_arr(f)


def _serie(e):
    """Velas cerradas del símbolo de la escena ("simbolo" en la escena para otra acción de velas.json; por defecto el de la lección)."""
    s = e.get("simbolo", VJ["simbolo"])
    return VELAS if s == VJ["simbolo"] else [v for v in VEL["series"][s]["velas"] if fecha_v(v["t"]) <= ULT]


def _rango(e, con_previas=False):
    d0 = dt.date.fromisoformat(e["desde"]) if e.get("desde") else None; d1 = dt.date.fromisoformat(e["hasta"]) if e.get("hasta") else ULT
    S = _serie(e); idx = [k for k, v in enumerate(S) if (d0 is None or fecha_v(v["t"]) >= d0) and fecha_v(v["t"]) <= d1]
    return (S, idx[0], idx[-1] + 1) if con_previas else S[idx[0]:idx[-1] + 1]


COL_MA = {20: BLUE, 50: GOLD, 200: "#C084FC"}   # GD 20 azul, GD 50 dorada, GD 200 violeta


def medias(e):
    """Medias móviles simples de cierre (berechnet) para el rango de la escena, con las sesiones previas para que empiecen completas."""
    S, a, b = _rango(e, True); c = np.array([v["c"] for v in S], float); out = {}
    for m in e.get("medias", []):
        ma = np.full(len(c), np.nan)
        if len(c) >= m: cs = np.cumsum(np.insert(c, 0, 0)); ma[m - 1:] = (cs[m:] - cs[:-m]) / m
        out[m] = ma[a:b]
    return out


def s_grafico(i, e, t):
    f = base(i, e["kicker"], e["titulo"]); V = _rango(e); n = len(V)
    vol = e.get("volumen", True)
    ax = f.add_axes([0.06, 0.325 if vol else 0.24, 0.80, 0.445 if vol else 0.53]); clean(ax)
    rev = n if not e.get("animar_velas") else max(2, int(n * ease(t * 1.15)))
    o = np.array([v["o"] for v in V]); hi = np.array([v["h"] for v in V]); lo = np.array([v["l"] for v in V]); c = np.array([v["c"] for v in V])
    up = c >= o; xs = np.arange(n); wd = 0.65 if n < 160 else 0.75
    ymin, ymax = lo.min(), hi.max(); pad = (ymax - ymin) * 0.08
    for z in e.get("zonas", []): ymin = min(ymin, z["de"]); ymax = max(ymax, z["a"])
    for ma in medias(e).values(): ymin = min(ymin, np.nanmin(ma)); ymax = max(ymax, np.nanmax(ma))
    ax.set_ylim(ymin - pad * 2.0, ymax + pad * 1.8); ax.set_xlim(-1, n + (n * 0.25))
    ax.vlines(xs[:rev], lo[:rev], hi[:rev], color=[TEAL if u else NEG for u in up[:rev]], lw=1.1 if n > 160 else 1.6)
    ax.bar(xs[:rev], np.maximum(np.abs(c - o), (ymax - ymin) * 0.002)[:rev], bottom=np.minimum(o, c)[:rev], width=wd,
           color=[TEAL if u else NEG for u in up[:rev]])
    za = ease((t - 0.25) / 0.35)
    etq = []
    for k, (m, ma) in enumerate(medias(e).items()):
        a = ease((t - 0.2 - k * 0.15) / 0.35); r = max(2, int(rev * a)) if e.get("animar_velas") else max(2, int(n * a))
        ax.plot(xs[:r], ma[:r], color=col(COL_MA.get(m, FG)), lw=3 if m == 200 else 2.4, alpha=0.95 * min(1, a * 3))
        if a > 0.95 and not np.isnan(ma[-1]): etq.append([ma[-1], m])
    gap = (ymax - ymin) * 0.06; etq.sort()   # etiquetas GD sin solaparse, a la derecha de la etiqueta del precio
    for k in range(1, len(etq)): etq[k][0] = max(etq[k][0], etq[k - 1][0] + gap)
    for y, m in etq: ax.text(n + n * 0.085, y, f"GD {m}", color=col(COL_MA.get(m, FG)), fontsize=15, weight="bold", va="center")
    for k, z in enumerate(e.get("zonas", [])):
        a = ease((t - 0.25 - k * 0.12) / 0.35); cc = col(z.get("color", "gold"))
        ax.axhspan(z["de"], z["a"], color=cc, alpha=0.22 * a, lw=0)
        ax.axhline((z["de"] + z["a"]) / 2, color=cc, lw=1.4, ls="--", alpha=0.8 * a)
        ax.text(n + n * 0.245, (z["de"] + z["a"]) / 2, f"{z['texto']}\n{num(z['de'], 0)}–{num(z['a'], 0)} $", color=cc, fontsize=17, weight="bold",
                ha="right", va="center", alpha=a, linespacing=1.15,
                bbox=dict(boxstyle="round,pad=0.25", fc=BG, ec="none", alpha=0.85 * a))
    idx = {fecha_v(v["t"]).isoformat(): j for j, v in enumerate(V)}
    for k, L in enumerate(e.get("lineas", [])):
        # línea de tendencia entre dos puntos [fecha, precio] (eingezeichnet), prolongada en discontinua hasta "hasta" (fecha) o el final;
        # "paralela": [fecha, precio] dibuja la paralela por ese punto y sombrea el canal
        a = ease((t - 0.3 - k * 0.15) / 0.35)
        if a <= 0: continue
        # índices sobre toda la serie (los anclajes pueden quedar antes del rango visible), relativos al inicio del rango
        S_, a0, _ = _rango(e, True); gi = {fecha_v(v["t"]).isoformat(): jj - a0 for jj, v in enumerate(S_)}
        (f1, p1), (f2, p2) = L["de"], L["a"]; j1, j2 = gi[f1], gi[f2]; m_ = (p2 - p1) / (j2 - j1)
        j3 = gi.get(L.get("hasta"), n - 1); cc = col(L.get("color", "gold"))
        y = lambda j, b=p1: b + m_ * (j - j1)
        k1, k2 = max(j1, 0), max(j2, 0)
        if j2 > 0: ax.plot([k1, k2], [y(k1), y(k2)], color=cc, lw=3, alpha=a, solid_capstyle="round")
        if j3 > k2: ax.plot([k2, j3], [y(k2), y(j3)], color=cc, lw=2.4, ls="--" if j2 >= 0 else "-", alpha=a)
        for jj, pp in ((j1, p1), (j2, p2)):
            if jj >= 0: ax.plot([jj], [pp], "o", color=cc, ms=9, alpha=a)
        if L.get("paralela"):
            fp, pp = L["paralela"]; b2 = pp - m_ * (gi[fp] - j1)
            ax.plot([k1, j3], [y(k1, b2), y(j3, b2)], color=cc, lw=2.4, ls=(0, (6, 4)), alpha=a)
            ax.fill_between([k1, j3], [y(k1), y(j3)], [y(k1, b2), y(j3, b2)], color=cc, alpha=0.08 * a, lw=0)
        if L.get("texto"):
            jt = L.get("texto_en", j3); jt = gi.get(jt, jt) if isinstance(jt, str) else jt
            ax.text(jt, y(jt) + (ymax - ymin) * L.get("texto_dy", 0.05), L["texto"], color=cc, fontsize=16, weight="bold", ha="center", va="center", alpha=a,
                    bbox=dict(boxstyle="round,pad=0.2", fc=BG, ec="none", alpha=0.8 * a))
    for k, m in enumerate(e.get("marcas", [])):
        j = idx.get(m["fecha"])
        if j is None: continue
        a = ease((t - 0.45 - k * 0.07) / 0.3); arriba = m.get("tipo") == "techo"
        yv = hi[j] if arriba else lo[j]; off = (ymax - ymin) * (0.07 if arriba else -0.07)
        ax.plot([j], [yv + off * 0.35], marker="v" if arriba else "^", color=GOLD, ms=15, alpha=a)
        if m.get("texto"): ax.text(j, yv + off * 1.25, m["texto"], color=GOLD, fontsize=15, weight="bold", ha="center", va="center", alpha=a)
    if e.get("ultimo", True) and rev == n:
        ax.axhline(c[-1], color=FG, lw=0.8, alpha=0.5 * za)
        ax.text(n + 0.5, c[-1], f" {num(c[-1])} $", color=BG, fontsize=15, weight="bold", va="center",
                bbox=dict(boxstyle="square,pad=0.25", fc=FG, ec="none", alpha=za), alpha=za)
    ax.yaxis.tick_left(); ax.tick_params(labelsize=15)
    ax.set_yticks(ax.get_yticks()[1:-1]); ax.set_yticklabels([num(y, 0) for y in ax.get_yticks()])
    ax.grid(axis="y", color=DIM, lw=0.6, alpha=0.6)
    tk, prev = [], None
    for j, v in enumerate(V):
        d = fecha_v(v["t"])
        if d.month != prev: tk.append((j, MESES[d.month - 1] + (f"\n{d.year}" if d.month == 1 or not tk else ""))); prev = d.month
    step = 1 if len(tk) <= 8 else 2
    ax.set_xticks([p[0] for p in tk[::step]], [p[1] for p in tk[::step]] if not vol else [])
    if vol:
        av = f.add_axes([0.06, 0.235, 0.80, 0.08]); clean(av)
        vv = np.array([v["v"] or 0 for v in V]) / 1e6
        av.bar(xs[:rev], vv[:rev], color=[TEAL if u else NEG for u in up[:rev]], width=wd, alpha=0.55)
        av.set_xlim(ax.get_xlim()); av.set_yticks([]); av.set_ylim(0, vv.max() * 1.1)
        av.set_xticks([p[0] for p in tk[::step]], [p[1] for p in tk[::step]]); av.tick_params(labelsize=15)
        T(f, 0.86, 0.318, "Handelsvolumen", MUTED, 14, ha="right")
    T(f, 0.06, 0.785, f"{e.get('nombre', VJ['nombre'])} ({e.get('ticker', VJ['ticker'])}) · Tageskerzen · US-Dollar" +
      ("".join(f" · GD {m}" for m in e.get("medias", [])) + " (gleitende Durchschnitte, berechnet)" if e.get("medias") else ""), MUTED, 18, "bold")
    if e.get("nota"):
        b = ease((t - 0.5) / 0.4); T(f, 0.94, 0.785, e["nota"], GOLD, 20, "bold", ha="right", alpha=b)
    fuente(f, FUENTE)
    return to_arr(f)


def s_fin(i, e, t):
    f = fig(W, H); a = ease(t / 0.5)
    T(f, 0.06, 0.86, f"Folge {VJ['folge']}: {VJ['tema']}", FG, 44, "bold", alpha=a)
    T(f, 0.06, 0.80, "Das Wichtigste in Kürze", GOLD, 30, "bold", alpha=a)
    for k, c in enumerate(e["claves"][:4]):
        T(f, 0.06, 0.73 - k * 0.06, "• " + c, FG, 25, alpha=ease((t - 0.1 - k * 0.1) / 0.4))
    b = ease((t - 0.3) / 0.5)
    if e.get("siguiente"): T(f, 0.06, 0.47, "Nächste Folge: " + e["siguiente"], GOLD, 26, "bold", alpha=b)
    T(f, 0.06, 0.42, "Unser Telegram-Kanal: " + TELEGRAM.replace("https://", "") + " · Kanal abonnieren", BLUE, 24, "bold", alpha=b)
    aviso = ("Wichtiger Hinweis: Nur Information und Bildung. Keine Anlageberatung und keine Kauf- oder Verkaufsempfehlung für ein Wertpapier. "
             "Die genannten Aktien dienen nur als Beispiel. Charttechnik beschreibt vergangene Kursverläufe und sagt keine Kurse voraus. Kursdaten: TradingView; "
             "Linien und Zonen eigene Berechnung. Wir halten keine Positionen in den genannten Aktien. Aktien sind mit Risiken bis zum Totalverlust verbunden. "
             "Text, Stimme (synthetische Stimme) und Grafiken mit KI erstellt.")
    T(f, 0.06, 0.33, "\n".join(textwrap.wrap(aviso, 140)), MUTED, 15, linespacing=1.5, alpha=a, va="top")
    return with_logo(to_arr(f), LGB, x=W - 340, y=70)


TIPOS = {"portada": s_portada, "puntos": s_puntos, "esquema": s_esquema, "grafico": s_grafico, "fin": s_fin}
BIG = {"portada", "fin"}
SUB = {}


def overlay(marcas, leads):
    pie = tira_texto(f"{MARCA} · Serie «{SERIE}» · Keine Anlageberatung", GOLD, 18, 46); band = np.array([0x13, 0x29, 0x4B], np.float32)

    def sub(s):
        if s not in SUB: SUB[s] = [tira_texto(l, FG, 27, 50, "bold") for l in (textwrap.wrap(s, 80) or [s])]
        return SUB[s]

    def ov(fr, j, ts, tg):
        fr = fr.copy(); bh = 46
        fr[H - bh:] = (fr[H - bh:].astype(np.float32) * 0.1 + band * 0.9).astype(np.uint8); fr[H - bh - 2:H - bh] = (0xD4, 0xAF, 0x37)
        pegar(fr, pie, (W - pie.shape[1]) // 2, H - bh)
        for a, b, s in marcas[j]:
            if a + leads[j] <= ts < b + leads[j] + 0.25:
                ls = sub(s); h = 50 * len(ls); y0 = H - bh - 16 - h; wmax = max(l.shape[1] for l in ls); x0 = max((W - wmax) // 2 - 24, 0)
                fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48] = (fr[y0 - 8:y0 + h + 6, x0:x0 + wmax + 48].astype(np.float32) * 0.28 + np.array([11, 26, 46], np.float32) * 0.72).astype(np.uint8)
                for k, l in enumerate(ls): pegar(fr, l, (W - l.shape[1]) // 2, y0 + k * 50)
                break
        return fr
    return ov


def frame(i, t):
    e = ESC[i]; a = TIPOS[e["tipo"]](i, e, t)
    return a if e["tipo"] in BIG else with_logo(a, LG, x=W - 190, y=40)


def control():
    err = []
    for k in ("base", "folge", "simbolo", "ticker", "nombre", "tema", "escenas", "info", "miniatura"):
        if not VJ.get(k): err.append(f"falta {k} en video.json")
    for k, e in enumerate(ESC):
        if e.get("tipo") not in TIPOS: err.append(f"escena {k}: tipo desconocido {e.get('tipo')}")
        if not e.get("voz"): err.append(f"escena {k} ({e.get('id')}): sin locución")
        if e.get("tipo") == "grafico":
            V = _rango(e)
            if e.get("simbolo") and (e["simbolo"] not in VEL["series"] or not e.get("nombre")): err.append(f"escena {k}: simbolo sin velas o sin nombre")
            for m, ma in medias(e).items():
                if np.isnan(ma[0]): err.append(f"escena {k}: no hay sesiones previas suficientes para la GD {m}")
            if len(V) < 20: err.append(f"escena {k}: menos de 20 velas en el rango")
            fechas = {fecha_v(v["t"]).isoformat() for v in V}
            todas = {fecha_v(v["t"]).isoformat() for v in _serie(e)}
            for L in e.get("lineas", []):
                for fch in [L["de"][0], L["a"][0]] + ([L["paralela"][0]] if L.get("paralela") else []):
                    if fch not in todas: err.append(f"escena {k}: línea con fecha {fch} sin vela")
                if L.get("hasta") and L["hasta"] not in fechas: err.append(f"escena {k}: «hasta» {L['hasta']} fuera del rango")
            for m in e.get("marcas", []):
                if m["fecha"] not in fechas: err.append(f"escena {k}: marca {m['fecha']} sin vela")
    if VJ.get("ultima_vela") and VJ["ultima_vela"] != ULT.isoformat(): err.append(f"velas.json acaba el {ULT}, video.json espera {VJ['ultima_vela']}")
    if err: sys.exit("CONTROL DE CALIDAD:\n- " + "\n- ".join(err))


if __name__ == "__main__":
    control()
    if PREVIEW:
        ov = overlay([[(0, 99, frases(e["voz"])[0])] for e in ESC], [0] * len(ESC))
        for j, e in enumerate(ESC): Image.fromarray(ov(frame(j, 1.0), j, 1.0, 3.0)).save(os.path.join(AUD, f"prev_{j:02d}_{e.get('id', e['tipo'])}.png"))
        print("palabras", sum(len(e["voz"].split()) for e in ESC)); sys.exit()
    VV = [voz_frases(e["voz"], AUD) for e in ESC]; sr = VV[0][1]; motor = VV[0][3]
    if len({v[1] for v in VV}) > 1 or len({v[3] for v in VV}) > 1: sys.exit("voces mezcladas")
    durs = [0.15 + len(a) / sr + 0.7 for a, _, _, _ in VV]; durs[-1] += 1.5
    print("voz", motor, "duración prevista", round(sum(durs), 1))
    if not MIN_S <= sum(durs) <= MAX_S: sys.exit(f"Duración {sum(durs):.0f} s fuera de {MIN_S}-{MAX_S} s")
    leads = [0.15] * len(ESC)
    times, t0 = render([lambda t, j=j: frame(j, t) for j in range(len(ESC))], durs, ([v[0] for v in VV], leads), sr, W, H, 30, OUT,
                       os.path.join(AUD, "lec-silent.mp4"), os.path.join(AUD, "lec.wav"), overlay=overlay([v[2] for v in VV], leads))
    json.dump([(e.get("id", str(j)), tt) for j, (e, tt) in enumerate(zip(ESC, times))] + [("_total", round(t0, 2)), ("_voz", motor)], open(f"{DIR}/times.json", "w"))
    with open(f"{DIR}/guion-{BASE}-GE.md", "w") as g:
        g.write(f"# {SERIE} · Folge {VJ['folge']}: {VJ['tema']} ({VJ['nombre']}, {VJ['ticker']})\n\nStimme: {motor} · Dauer {t0:.0f} s\n\n| Zeit | Szene | Text |\n|---|---|---|\n")
        for e, tt in zip(ESC, times): g.write(f"| {int(tt) // 60}:{int(tt) % 60:02d} | {e.get('id', e['tipo'])} | {e['voz']} |\n")
    print("listo", round(t0, 1), "s", OUT)
